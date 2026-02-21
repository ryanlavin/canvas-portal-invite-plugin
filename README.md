# Canvas Portal Invite Plugin

Automatically sends patient portal invites when new patients are created in Canvas Medical.

## How it Works

1. A patient is created in Canvas (via intake form, manual entry, etc.)
2. Canvas fires a `PATIENT_CREATED` event
3. This plugin receives the event and:
   - Looks up the Patient and their associated CanvasUser
   - Checks that they're not already portal-registered
   - Checks that they have an email or phone number
   - Returns a `PATIENT_PORTAL__SEND_INVITE` effect
4. Canvas sends the portal invitation email/SMS

## Safety Guards

- **Idempotent**: Skips if patient is already portal-registered
- **Contact required**: Skips if no email or phone on file
- **Graceful failure**: Logs warnings and returns empty if patient/user not found

## Installation

```bash
canvas install portal_invite
```

Or from git:

```bash
canvas install --host https://your-instance.canvasmedical.com https://github.com/ryanlavin/canvas-portal-invite-plugin.git
```

## Requirements

- Canvas Medical SDK v0.94.0+
- Patient must have an email or phone configured
- Patient must have an associated CanvasUser record
