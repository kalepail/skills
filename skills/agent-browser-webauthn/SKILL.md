---
name: agent-browser-webauthn
description: Use agent-browser with Chrome DevTools Protocol virtual WebAuthn authenticators to test passkey, WebAuthn, Stellar smart account, wallet creation, wallet restore, and browser signing flows. Trigger when a task mentions passkeys, WebAuthn, virtual authenticators, Stellar Smart Account Kit browser tests, or agent-browser passkey automation.
---

# Agent Browser WebAuthn

Use this with `$agent-browser` when a browser test must create or authenticate a passkey. The bundled helper keeps a Chrome CDP WebAuthn virtual authenticator attached to the active `agent-browser` page while a child command drives the UI.

## Workflow

1. Start or reuse an `agent-browser` session.
2. Open the target page before attaching WebAuthn, so the helper can bind to the correct page target.
3. Set `WEBAUTHN_SKILL_DIR` to this skill folder, or replace it with the absolute path shown in this skill's source locator.
4. Wrap the interaction command with:

```bash
WEBAUTHN_SKILL_DIR="/path/to/agent-browser-webauthn"
node "$WEBAUTHN_SKILL_DIR/scripts/agent-browser-webauthn-helper.mjs" run \
  --session "$SESSION" -- \
  bash -lc 'agent-browser --session "$SESSION" find role button click --name "Create passkey wallet"'
```

5. Assert real app output after the passkey operation. For Stellar Smart Account Kit, assert a `C...` contract id or an explicit transaction/funding error. Do not treat a visible button click as success.
6. Close the session after smoke tests so virtual authenticators and IndexedDB state do not leak across runs.

## Important Details

- The helper uses `agent-browser get cdp-url`, `Target.attachToTarget`, `WebAuthn.enable`, and `WebAuthn.addVirtualAuthenticator`.
- Defaults are CTAP2, internal transport, resident keys enabled, user verification enabled, user verified, and automatic presence simulation enabled.
- Use a local or otherwise trusted CDP endpoint. Remote CDP URLs are rejected unless `--allow-remote-cdp true` is passed deliberately.
- Launch the site on `localhost` or HTTPS. WebAuthn requires a secure context; many passkey and smart-account SDKs also reject raw `127.0.0.1` for domain validation.
- If a session has stale passkey/IndexedDB state, close it and use a fresh session name.
- Do not put secrets in command arguments or page text assertions.

## Requirements

- `agent-browser` CLI.
- Node.js 22 or newer, for the built-in `WebSocket` client used by the helper.

## Script

- `scripts/agent-browser-webauthn-helper.mjs` - wrap any command while a virtual authenticator is attached to the session.
