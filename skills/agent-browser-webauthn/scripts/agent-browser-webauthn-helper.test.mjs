#!/usr/bin/env node

import { spawnSync } from "node:child_process";
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
