"""Auto Portal Invite - sends portal invite when patient is created."""

from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.effects import Effect, EffectType


class AutoPortalInvite(BaseProtocol):
    """Sends patient portal invite when a new patient is created."""

    RESPONDS_TO = ["PATIENT_CREATED"]

    def compute(self):
        try:
            context = getattr(self.event, 'context', {}) or {}
            patient = context.get("patient", {})
            patient_id = patient.get("id")

            if not patient_id:
                return []

            # Return effect to send portal invite
            return [
                Effect(
                    type=EffectType.PATIENT_PORTAL__SEND_INVITE,
                    payload={"patient_id": patient_id}
                )
            ]
        except:
            return []
