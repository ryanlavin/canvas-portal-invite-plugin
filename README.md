# Canvas Portal Invite Plugin

Automatically sends patient portal invites when new patients are created in Canvas Medical.

## Features

- Listens for `PATIENT_CREATED` events
- Automatically triggers `PATIENT_PORTAL__SEND_INVITE` effect
- No configuration required

## Installation

```bash
canvas install --host https://your-instance.canvasmedical.com https://github.com/ryanlavin/canvas-portal-invite-plugin.git
```

## Requirements

- Canvas Medical SDK v0.94.0+
- Patient must have an email or phone configured for portal access

## How it Works

When a patient is created in Canvas:
1. The plugin receives the `PATIENT_CREATED` event
2. It extracts the patient ID from the event context
3. It returns a `PATIENT_PORTAL__SEND_INVITE` effect
4. Canvas sends the portal invite email/SMS to the patient
