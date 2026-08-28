---
name: agent-browser-webauthn
description: Use agent-browser with Chrome DevTools Protocol virtual WebAuthn authenticators to test passkey, WebAuthn, Stellar smart account, wallet creation, wallet restore, and browser signing flows. Trigger when a task mentions passkeys, WebAuthn, virtual authenticators, Stellar Smart Account Kit browser tests, or agent-browser passkey automation. Do not use for browser flows without a passkey or WebAuthn ceremony—password logins and extension-wallet connects route to agent-browser alone.
---

# Agent Browser WebAuthn

Use this with `$agent-browser` when a browser test must create or authenticate a passkey. The bundled helper keeps one Chrome CDP WebAuthn virtual authenticator attached while one child command drives the whole UI flow.

## Workflow

1. Start a fresh `agent-browser` session for each full E2E.
2. Open the target page before attaching WebAuthn, so the helper can bind to the correct page target.
3. Set `WEBAUTHN_SKILL_DIR` to this skill folder, or replace it with the absolute path shown in this skill's source locator.
4. Wrap the entire create -> restore -> connect -> reject -> sign driver in one helper invocation. Cleanup removes the authenticator and its credentials when the child exits, so never split ceremonies across helper runs.

```bash
WEBAUTHN_SKILL_DIR="/path/to/agent-browser-webauthn"
SESSION="passkey-e2e-$(date +%s)"
ARTIFACT_DIR="$(mktemp -d)"
export SESSION WEBAUTHN_EVENTS_FILE="$ARTIFACT_DIR/webauthn.jsonl"
export WEBAUTHN_CONTROL_FILE="$ARTIFACT_DIR/webauthn-control.txt"
: >"$WEBAUTHN_CONTROL_FILE"

# Start headed first. Once this passes, omit --headed for the headless canary.
agent-browser --session "$SESSION" --headed open http://localhost:3000

node "$WEBAUTHN_SKILL_DIR/scripts/agent-browser-webauthn-helper.mjs" run \
  --session "$SESSION" --require-credential true --timeout-ms 300000 -- bash -lc '
    set -euo pipefail
    ab() { agent-browser --session "$SESSION" "$@"; }

    ab find role button click --name "Create passkey"
    ab wait --text "Connected"
    ab reload
    ab find role button click --name "Restore session"
    ab wait --text "Restored"
    ab find role button click --name "Connect passkey"
    ab wait --text "Connected"

    printf "uv:false\n" >"$WEBAUTHN_CONTROL_FILE"
    until grep -q "\"controlApplied\":\"uv:false\"" "$WEBAUTHN_EVENTS_FILE"; do sleep 0.2; done
    ab find role button click --name "Connect passkey"
    ab wait --text "rejected"
    printf "uv:true\n" >"$WEBAUTHN_CONTROL_FILE"
    until grep -q "\"controlApplied\":\"uv:true\"" "$WEBAUTHN_EVENTS_FILE"; do sleep 0.2; done
    ab find role button click --name "Sign"
    ab wait --text "Signed"
  '

grep -q '"event":"WebAuthn.credentialAdded"' "$WEBAUTHN_EVENTS_FILE"
grep -q '"event":"WebAuthn.credentialAsserted"' "$WEBAUTHN_EVENTS_FILE"
agent-browser --session "$SESSION" close
```

5. Adapt only the app URL, button names, and result text. Keep ceremony triggers as native `agent-browser click` or `find ... click` commands; never use evaluated DOM `.click()`.
6. Assert real app output after each operation. For Stellar Smart Account Kit, assert a `C...` contract id or an explicit transaction/funding error. Do not treat a visible button click as success.
7. Require both credential events and inspect the final `WebAuthn.getCredentials` diagnostic. `--require-credential true` fails clearly when no virtual credential was observed; without the flag the helper only warns and exits 0, so always pass it for credential flows.
8. Close the fresh session after smoke tests so virtual authenticators and IndexedDB state do not leak across runs.

## Important Details

- Open the target before starting the helper so it attaches before the first ceremony. A reload keeps the same target; after a tab or page target is replaced, reattach by stopping and re-running the whole flow from a fresh session with the helper attached to the new target before creating a credential.
- Headed and headless both work with this recipe. Start headed when diagnosing Chrome/WebAuthn behavior, then repeat headless after the headed flow passes.
- The helper explicitly uses `WebAuthn.enable({enableUI:false})` and the proven CTAP2 config: `protocol: ctap2`, `transport: internal`, `hasResidentKey: true`, `hasUserVerification: true`, `isUserVerified: true`, and `automaticPresenceSimulation: true`.
- Setup diagnostics include the target id and authenticator id. Credential events and redacted `WebAuthn.getCredentials` output go to stderr or `WEBAUTHN_EVENTS_FILE` as JSONL; private key material is never logged.
- Set `WEBAUTHN_CONTROL_FILE` to exercise rejection: write `uv:false` before the rejected ceremony and `uv:true` before the next successful ceremony, then wait for the matching `controlApplied` event in `WEBAUTHN_EVENTS_FILE` before the next click—the helper applies directives on a 500 ms poll, so elapsed time does not prove one applied.
- Setup, CDP calls, and the wrapped command have a 120-second timeout by default. Set `--timeout-ms` to a larger positive value for deliberately long flows.
- Use a local or otherwise trusted CDP endpoint. Remote CDP URLs are rejected unless `--allow-remote-cdp true` is passed deliberately.
- Launch the site on `localhost` or HTTPS. WebAuthn requires a secure context; many passkey and smart-account SDKs also reject raw `127.0.0.1` for domain validation.
- Always use a fresh session name for a full E2E. If a session has stale passkey/IndexedDB state, close it rather than trying to repair it in place.
- Do not put secrets in command arguments or page text assertions.

## Requirements

- `agent-browser` CLI.
- `$agent-browser` skill is recommended for current CLI workflow guidance but is not bundled automatically.
- Node.js 22 or newer, for the built-in `WebSocket` client used by the helper.

## Script

- `scripts/agent-browser-webauthn-helper.mjs` - wrap any command while a virtual authenticator is attached to the session.
- `scripts/agent-browser-webauthn-helper.test.mjs` - run dependency-free CLI safety checks after changing the helper.
