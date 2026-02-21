"""
Portal Invite — Automatically sends patient portal invitations
when a new patient is created in Canvas.

Listens for PATIENT_CREATED events, looks up the associated
CanvasUser, and returns a SendInviteEffect to trigger the
portal invitation email.
"""

from typing import List

from canvas_sdk.effects import Effect
from canvas_sdk.effects.send_invite import SendInviteEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Patient
from logger import log


class PortalInvite(BaseHandler):
    """
    Sends a patient portal invite automatically when a patient is created.

    The patient must have:
    - An associated CanvasUser record (created automatically by Canvas)
    - An email or phone number for the invite to be delivered

    If the user is already registered for the portal, the invite is skipped.
    """

    RESPONDS_TO = [EventType.Name(EventType.PATIENT_CREATED)]

    def compute(self) -> List[Effect]:
        patient_id = self.target

        try:
            patient = Patient.objects.select_related("user").get(id=patient_id)
        except Patient.DoesNotExist:
            log.warning(f"[PortalInvite] Patient {patient_id} not found — skipping invite")
            return []

        user = getattr(patient, "user", None)
        if user is None:
            log.warning(
                f"[PortalInvite] Patient {patient_id} has no CanvasUser — "
                "portal invite cannot be sent yet"
            )
            return []

        # Skip if already registered
        if user.is_portal_registered:
            log.info(
                f"[PortalInvite] Patient {patient_id} (user {user.dbid}) "
                "is already portal-registered — skipping"
            )
            return []

        # Check that the user has contact info for the invite
        if not user.email and not user.phone_number:
            log.warning(
                f"[PortalInvite] User {user.dbid} has no email or phone — "
                "cannot deliver portal invite"
            )
            return []

        log.info(
            f"[PortalInvite] Sending portal invite for patient {patient_id} "
            f"(user dbid={user.dbid}, email={user.email or 'none'})"
        )

        return [SendInviteEffect(user_dbid=user.dbid).apply()]
