"""Portal Invite - minimal test version."""

from canvas_sdk.protocols import BaseProtocol


class PortalInvite(BaseProtocol):
    RESPONDS_TO = ["PATIENT_CREATED"]

    def compute(self):
        # Minimal - just return empty effects to confirm plugin loads
        return []
