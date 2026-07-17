#!/usr/bin/env node

import { execFile, spawn } from "node:child_process";
import { appendFileSync, readFileSync } from "node:fs";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const DEFAULT_TIMEOUT_MS = 120_000;

const DEFAULT_AUTHENTICATOR_OPTIONS = {
  protocol: "ctap2",
  transport: "internal",
  hasResidentKey: true,
  hasUserVerification: true,
  isUserVerified: true,
  automaticPresenceSimulation: true
};

function printUsage() {
  console.error(`
Usage:
  node scripts/agent-browser-webauthn-helper.mjs run [options] -- <command> [args...]

Options:
  --session <name>           Existing agent-browser session name
  --cdp-url <ws-url>         Explicit CDP WebSocket URL; overrides --session lookup
  --url <page-url>           Page URL to bind within the browser session
  --transport <type>         internal | usb | nfc | ble | cable
  --protocol <type>          ctap2 | u2f
  --resident-key <bool>      true | false
  --user-verification <bool> true | false
  --verified <bool>          true | false
  --presence <bool>          true | false
  --require-credential <bool> Fail when no virtual credential is observed; default false
  --allow-remote-cdp <bool>  true | false; default false
  --timeout-ms <number>      Positive integer; default 120000

Environment:
  WEBAUTHN_EVENTS_FILE       Optional JSONL diagnostics file
  WEBAUTHN_CONTROL_FILE      Optional file accepting uv:false and uv:true
`);
}

function parseArgs(argv) {
  const normalized = argv[0] === "--" ? argv.slice(1) : argv;
  const command = normalized[0];
  if (!command) {
    printUsage();
    process.exit(1);
  }

  const separator = normalized.indexOf("--");
  const optionTokens = separator === -1 ? normalized.slice(1) : normalized.slice(1, separator);
  const childCommand = separator === -1 ? [] : normalized.slice(separator + 1);
  const args = { _: [] };

  for (let i = 0; i < optionTokens.length; i += 1) {
    const token = optionTokens[i];
    if (!token.startsWith("--")) {
      args._.push(token);
      continue;
    }

    const key = token.slice(2);
    const next = optionTokens[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }

    args[key] = next;
    i += 1;
  }

  return { command, args, childCommand };
}

function parseBoolean(value, fallback) {
  if (value === undefined) return fallback;
  if (typeof value === "boolean") return value;

  const normalized = String(value).toLowerCase();
  if (["true", "1", "yes", "on"].includes(normalized)) return true;
  if (["false", "0", "no", "off"].includes(normalized)) return false;
  throw new Error(`Expected a boolean value, received "${value}"`);
}

function parsePositiveInteger(value, fallback) {
  if (value === undefined) return fallback;
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed <= 0) {
    throw new Error(`Expected a positive integer, received "${value}"`);
  }
  return parsed;
}

function logDiagnostic(record) {
  const line = JSON.stringify({ at: new Date().toISOString(), ...record });
  const file = process.env.WEBAUTHN_EVENTS_FILE;
  if (file) {
    try {
      appendFileSync(file, `${line}\n`);
      return;
    } catch {
      // Fall through to stderr so diagnostics are never lost silently.
    }
  }
  console.error(line);
}

function redactCredential(credential) {
  return {
    credentialIdPrefix: String(credential.credentialId ?? "").slice(0, 16),
    rpId: credential.rpId,
    signCount: credential.signCount,
    isResidentCredential: credential.isResidentCredential,
    backupEligibility: credential.backupEligibility
  };
}

async function runAgentBrowser(args, timeoutMs) {
  const { stdout } = await execFileAsync("agent-browser", args, { encoding: "utf8", timeout: timeoutMs });
  return stdout.trim();
}

function getLastNonEmptyLine(output) {
  return output
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .at(-1);
}

async function resolveCDPUrl(args, timeoutMs) {
  if (args["cdp-url"] && args["cdp-url"] !== true) return args["cdp-url"];

  const session = args.session;
  if (!session || session === true) throw new Error("Provide --session or --cdp-url");

  const output = await runAgentBrowser(["--session", session, "get", "cdp-url"], timeoutMs);
  const cdpUrl = getLastNonEmptyLine(output);
  if (!cdpUrl) throw new Error(`Unable to resolve CDP URL for session "${session}"`);
  return cdpUrl;
}

function assertTrustedCDPUrl(cdpUrl, allowRemote) {
  if (allowRemote) return;

  let parsed;
  try {
    parsed = new URL(cdpUrl);
  } catch {
    throw new Error(`Invalid CDP URL: ${cdpUrl}`);
  }

  const hostname = parsed.hostname.toLowerCase();
  const isLocalhost = hostname === "localhost" || hostname === "127.0.0.1" || hostname === "::1" || hostname === "[::1]";
  if (!isLocalhost) {
    throw new Error(
      `Refusing to attach to non-local CDP host "${parsed.host}". ` +
        "Use --allow-remote-cdp true only for trusted remote browser sessions."
    );
  }
}

async function resolveCurrentUrl(args, timeoutMs) {
  if (args.url && args.url !== true) return args.url;
  if (!args.session || args.session === true) return null;
  const output = await runAgentBrowser(["--session", args.session, "get", "url"], timeoutMs);
  return getLastNonEmptyLine(output) ?? null;
}

function createCDPConnection(browserWsUrl, timeoutMs, onEvent) {
  const socket = new WebSocket(browserWsUrl);
  let nextId = 0;
  const pending = new Map();

  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.method && !message.id) {
      onEvent?.(message);
      return;
    }
    if (!message.id || !pending.has(message.id)) return;
    const { resolve, reject, timer } = pending.get(message.id);
    pending.delete(message.id);
    clearTimeout(timer);
    if (message.error) reject(new Error(JSON.stringify(message.error)));
    else resolve(message.result);
  };

  let rejectReady;
  let readyTimer;
  const ready = new Promise((resolve, reject) => {
    rejectReady = reject;
    readyTimer = setTimeout(
      () => reject(new Error(`CDP WebSocket connection timed out after ${timeoutMs}ms`)),
      timeoutMs
    );
    socket.onopen = () => {
      clearTimeout(readyTimer);
      resolve();
    };
    socket.onerror = (event) => {
      clearTimeout(readyTimer);
      reject(new Error(`WebSocket error: ${event.type}`));
    };
  });

  socket.onclose = () => {
    clearTimeout(readyTimer);
    rejectReady(new Error("CDP WebSocket closed before connection was ready"));
    for (const { reject, timer } of pending.values()) {
      clearTimeout(timer);
      reject(new Error("CDP WebSocket closed before response"));
    }
    pending.clear();
  };

  const send = (method, params = {}, sessionId) =>
    new Promise((resolve, reject) => {
      const id = ++nextId;
      if (socket.readyState !== WebSocket.OPEN) {
        reject(new Error("CDP WebSocket is not open"));
        return;
      }
      const timer = setTimeout(() => {
        pending.delete(id);
        reject(new Error(`CDP method ${method} timed out after ${timeoutMs}ms`));
      }, timeoutMs);
      pending.set(id, { resolve, reject, timer });
      const payload = { id, method, params };
      if (sessionId) payload.sessionId = sessionId;
      socket.send(JSON.stringify(payload));
    });

  const close = () => {
    if (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING) socket.close();
  };

  return { ready, send, close };
}

async function attachToPage(send, preferredUrl) {
  const { targetInfos } = await send("Target.getTargets");
  const pages = targetInfos.filter((target) => target.type === "page");
  const pageTarget =
    (preferredUrl ? pages.find((target) => target.url === preferredUrl) : null) ??
    pages.find((target) => target.url && target.url !== "about:blank") ??
    pages.at(-1);

  if (!pageTarget) throw new Error("Unable to find a page target in the remote browser");

  const { sessionId } = await send("Target.attachToTarget", {
    targetId: pageTarget.targetId,
    flatten: true
  });

  return { sessionId, pageUrl: pageTarget.url, targetId: pageTarget.targetId };
}

async function runChildCommand(command, args, timeoutMs) {
  return new Promise((resolve, reject) => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    const child = spawn(command, args, { stdio: "inherit", env: process.env, signal: controller.signal });
    child.on("error", (error) => {
      clearTimeout(timer);
      if (error.name === "AbortError") reject(new Error(`Child command timed out after ${timeoutMs}ms`));
      else reject(error);
    });
    child.on("exit", (code, signal) => {
      clearTimeout(timer);
      if (signal) reject(new Error(`Child command exited via signal ${signal}`));
      else resolve(code ?? 0);
    });
  });
}

async function commandRun(args, childCommand) {
  if (childCommand.length === 0) throw new Error("run requires a child command after --");

  const timeoutMs = parsePositiveInteger(args["timeout-ms"], DEFAULT_TIMEOUT_MS);
  const requireCredential = parseBoolean(args["require-credential"], false);
  const cdpUrl = await resolveCDPUrl(args, timeoutMs);
  assertTrustedCDPUrl(cdpUrl, parseBoolean(args["allow-remote-cdp"], false));
  const preferredUrl = await resolveCurrentUrl(args, timeoutMs);
  let credentialAddedCount = 0;
  let credentialAssertedCount = 0;
  const connection = createCDPConnection(cdpUrl, timeoutMs, (message) => {
    if (message.method !== "WebAuthn.credentialAdded" && message.method !== "WebAuthn.credentialAsserted") return;
    if (message.method === "WebAuthn.credentialAdded") credentialAddedCount += 1;
    else credentialAssertedCount += 1;
    const params = { ...message.params };
    if (params.credential) params.credential = redactCredential(params.credential);
    logDiagnostic({ event: message.method, params });
  });
  let sessionId;
  let authenticatorId;
  let controlTimer;
  let credentialFailure = false;
  let exitCode = 0;
  try {
    await connection.ready;
    const page = await attachToPage(connection.send, preferredUrl);
    sessionId = page.sessionId;
    const authenticatorOptions = {
      protocol: args.protocol || DEFAULT_AUTHENTICATOR_OPTIONS.protocol,
      transport: args.transport || DEFAULT_AUTHENTICATOR_OPTIONS.transport,
      hasResidentKey: parseBoolean(args["resident-key"], DEFAULT_AUTHENTICATOR_OPTIONS.hasResidentKey),
      hasUserVerification: parseBoolean(args["user-verification"], DEFAULT_AUTHENTICATOR_OPTIONS.hasUserVerification),
      isUserVerified: parseBoolean(args.verified, DEFAULT_AUTHENTICATOR_OPTIONS.isUserVerified),
      automaticPresenceSimulation: parseBoolean(args.presence, DEFAULT_AUTHENTICATOR_OPTIONS.automaticPresenceSimulation)
    };

    await connection.send("WebAuthn.enable", { enableUI: false }, sessionId);
    ({ authenticatorId } = await connection.send(
      "WebAuthn.addVirtualAuthenticator",
      { options: authenticatorOptions },
      sessionId
    ));

    logDiagnostic({
      setup: {
          session: typeof args.session === "string" ? args.session : null,
          pageUrl: page.pageUrl,
          targetId: page.targetId,
          authenticatorId,
          options: authenticatorOptions,
          enableUI: false
      }
    });

    const controlFile = process.env.WEBAUTHN_CONTROL_FILE;
    if (controlFile) {
      let lastDirective = "";
      controlTimer = setInterval(() => {
        let directive;
        try {
          directive = readFileSync(controlFile, "utf8").trim().split("\n").at(-1);
        } catch {
          return;
        }
        if (!directive || directive === lastDirective) return;
        lastDirective = directive;
        if (directive !== "uv:false" && directive !== "uv:true") return;
        connection
          .send(
            "WebAuthn.setUserVerified",
            { authenticatorId, isUserVerified: directive === "uv:true" },
            sessionId
          )
          .then(() => logDiagnostic({ controlApplied: directive }))
          .catch((error) => logDiagnostic({ controlError: String(error) }));
      }, 500);
    }

    exitCode = await runChildCommand(childCommand[0], childCommand.slice(1), timeoutMs);
  } finally {
    if (controlTimer) clearInterval(controlTimer);
    if (authenticatorId && sessionId) {
      try {
        const { credentials } = await connection.send("WebAuthn.getCredentials", { authenticatorId }, sessionId);
        logDiagnostic({
          finalCredentials: credentials.map(redactCredential),
          credentialAddedCount,
          credentialAssertedCount
        });
        if (credentials.length === 0) {
          const message = credentialAddedCount
            ? "No virtual credential remains; keep every ceremony in one helper invocation."
            : "No virtual credential observed; run the entire create-to-sign flow in one helper invocation.";
          console.error(`${requireCredential ? "Failure" : "Warning"}: ${message}`);
          credentialFailure = requireCredential;
        }
      } catch (error) {
        logDiagnostic({ getCredentialsError: String(error) });
        console.error(
          `${requireCredential ? "Failure" : "Warning"}: No virtual credential observed because WebAuthn.getCredentials failed.`
        );
        credentialFailure = requireCredential;
      }
      try {
        await connection.send("WebAuthn.removeVirtualAuthenticator", { authenticatorId }, sessionId);
      } catch (error) {
        console.error(`Cleanup warning: ${error instanceof Error ? error.message : String(error)}`);
      }
    }

    if (sessionId) {
      try {
        await connection.send("WebAuthn.disable", {}, sessionId);
      } catch (error) {
        console.error(`Cleanup warning: ${error instanceof Error ? error.message : String(error)}`);
      }
    }

    connection.close();
  }

  if (exitCode === 0 && credentialFailure) exitCode = 1;
  process.exitCode = exitCode;
}

const { command, args, childCommand } = parseArgs(process.argv.slice(2));

try {
  switch (command) {
    case "run":
      await commandRun(args, childCommand);
      break;
    case "help":
    case "--help":
    case "-h":
      printUsage();
      break;
    default:
      throw new Error(`Unknown command "${command}"`);
  }
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
}
