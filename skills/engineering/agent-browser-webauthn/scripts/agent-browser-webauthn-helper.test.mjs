#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const helper = fileURLToPath(new URL("./agent-browser-webauthn-helper.mjs", import.meta.url));

function run(args) {
  return spawnSync(process.execPath, [helper, ...args], { encoding: "utf8" });
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const help = run(["help"]);
assert(help.status === 0, "help must succeed");
assert(help.stderr.includes("--timeout-ms"), "help must document timeout control");
assert(help.stderr.includes("--require-credential"), "help must document credential verification");
assert(help.stderr.includes("WEBAUTHN_EVENTS_FILE"), "help must document event diagnostics");
assert(help.stderr.includes("WEBAUTHN_CONTROL_FILE"), "help must document user-verification control");

const source = readFileSync(helper, "utf8");
assert(source.includes('"WebAuthn.enable", { enableUI: false }'), "automated WebAuthn mode must be explicit");
assert(source.includes("WebAuthn.credentialAdded"), "credential creation events must be reported");
assert(source.includes("WebAuthn.credentialAsserted"), "credential assertion events must be reported");
assert(source.includes("WebAuthn.getCredentials"), "final credentials must be diagnosed");
assert(source.includes("No virtual credential observed"), "missing virtual credentials must have a clear failure");

const invalidTimeout = run([
  "run",
  "--timeout-ms",
  "0",
  "--cdp-url",
  "ws://127.0.0.1:9",
  "--",
  "true"
]);
assert(invalidTimeout.status === 1, "invalid timeout must fail");
assert(invalidTimeout.stderr.includes("Expected a positive integer"), "invalid timeout must explain failure");

const remoteCDP = run(["run", "--cdp-url", "ws://browser.example.com/devtools", "--", "true"]);
assert(remoteCDP.status === 1, "remote CDP must fail by default");
assert(remoteCDP.stderr.includes("Refusing to attach to non-local CDP host"), "remote CDP must explain denial");

console.log("agent-browser-webauthn helper self-check passed");
