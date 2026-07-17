# Notifications, account, and updates

Use this reference for alert policy and high-consequence account/update surfaces. Keep actions read-only until user explicitly authorizes state changes.

## Notification routing

- Solo background: native desktop notification when OS permission allows.
- Solo foreground: in-app toast.
- Same emitting process already selected: terminal BEL/OSC alert is suppressed.
- Ordinary output does not create unread state.
- Server announcements remain persistent in-app.
- Auto-dismiss toasts cover brief feedback; persistent toasts cover crashes, `solo.yml` changes, auto-restart exhaustion, and announcements.

Sources: [toasts](https://soloterm.com/docs/notifications/in-app-toasts), [permissions](https://soloterm.com/docs/notifications/macos-permissions), [indicators](https://soloterm.com/docs/notifications/indicators).

## Effective levels and limits

Project and process levels combine using more restrictive value:

| Level | Delivers |
|---|---|
| All | Terminal BEL/OSC and important process alerts |
| Important | Crashes and auto-restart exhaustion; suppresses BEL/OSC |
| None | Suppresses both categories |

- Unread clears by selecting process, dismissing linked alert, row dismiss, or title-bar Clear all.
- Project dot persists until each child unread is handled.
- App/workspace badges cap at `99+`; app badge clears when Solo regains focus.
- Bell default is **Ping**. macOS can use system or `~/Library/Sounds`; None mutes. Windows uses standard notification sound.
- Terminal notification rate limit: 5 per 10 seconds per process reader.
- Crash auto-restart pauses after 10 restarts in 60 seconds and alerts only on exhaustion, not every retry.

Sources: [indicators](https://soloterm.com/docs/notifications/indicators), [bell](https://soloterm.com/docs/notifications/bell-sounds), [script notifications](https://soloterm.com/docs/notifications/triggering-from-scripts), [auto-restart alerts](https://soloterm.com/docs/notifications/auto-restart-notifications), [troubleshooting](https://soloterm.com/docs/troubleshooting/notifications).

## Notification diagnosis

Check in order:

1. Solo permission state.
2. OS app notification permission.
3. Focus/Do Not Disturb.
4. **Send test** result.
5. Foreground/background/same-process routing.
6. Effective project/process level.
7. Rate limiting.
8. OS banner/sound/Notification Center settings.

Avoid changing process-level settings when request is only OS permission diagnosis.

## Account and license facts

- Free tier: 4 projects and 20 total commands/agents/terminals; all features and updates included.
- Reaching limit opens license prompt. Unlicensed over-limit state blocks process starts.
- Deactivating while over free limits returns app to Free and stops running managed processes.
- Activation contacts `soloterm.com` with key, app version, device ID/name, platform, and OS version; signed token is stored locally.
- Licensed offline grace is 14 days after successful check-in.
- Move license by deactivating old device and activating new; project/settings data does not move.
- Never reveal license key or local HTTP/MCP bearer token.

Sources: [free tier](https://soloterm.com/docs/account/free-tier), [activation](https://soloterm.com/docs/account/activating-license), [errors/offline](https://soloterm.com/docs/account/license-errors), [moving license](https://soloterm.com/docs/account/moving-license).

## Team-license caution

- Team licensing is central billing plus claim-link distribution, not SSO/directory seat management.
- Claim links are first-come and raw URL is shown once; regeneration replaces old link.
- Auto-grow is optional and off by default; anyone holding link can add billed seats up to configured cap.
- Revocation invalidates member immediately and frees seat.
- v1 lacks domain gating, SSO, assigned-seat UI, and directory sync.

Do not generate/regenerate/share claim links, change auto-grow, revoke seats, or open billing without explicit authorization.

Source: [Team licenses](https://soloterm.com/docs/account/team-licenses).

## Updates and relaunch

- Check via app menu, Settings → Account, title badge, or `Cmd/Ctrl+Shift+U`.
- Signed updater downloads/stages update; applying requires relaunch. Staged update can wait.
- Quit/relaunch stops running commands, agents, and terminals. Solo confirms when any run and lists up to six names.
- Relaunch reloads projects; eligible trusted auto-start commands may start again.
- Never apply update, quit, or relaunch from an informational request.
- Read the installed Solo version and the current [changelog](https://soloterm.com/changelog) before version-sensitive advice.

Sources: [installing updates](https://soloterm.com/docs/updates/installing-updates), [safe restart](https://soloterm.com/docs/updates/restarting-safely), [changelog](https://soloterm.com/changelog).

## Recovery boundary

Do not delete app data as routine customization. Core state reset removes projects, command records, trust, and other local data; UI preferences may also remain in browser storage. Route corruption diagnosis to `$solo-troubleshoot` and require explicit confirmation before destructive reset.

Source: [Resetting settings and state](https://soloterm.com/docs/troubleshooting/resetting-settings).
