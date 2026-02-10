"""
Auto Portal Invite Handler - Minimal test version.
"""

from canvas_sdk.protocols import BaseProtocol


class AutoPortalInvite(BaseProtocol):
    """Sends portal invite when patient is created."""

    RESPONDS_TO = ["PATIENT_CREATED"]

    def compute(self):
        # Minimal - just return empty effects to confirm plugin loads
        return []
