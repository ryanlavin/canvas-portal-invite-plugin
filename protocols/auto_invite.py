"""
Auto Portal Invite Handler

Automatically sets up portal user email and sends invite when patient is created.
"""

from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.data import Patient


class AutoPortalInvite(BaseProtocol):
    """
    When a patient is created:
    1. Gets the patient's email from their contact points
    2. Sets it as the portal contact
    3. Sends a portal invite
    """

    RESPONDS_TO = ["PATIENT_CREATED"]

    def compute(self):
        try:
            context = getattr(self.event, 'context', {}) or {}
            patient_data = context.get("patient", {})
            patient_id = patient_data.get("id")

            if not patient_id:
                return []

            # Try to get email from the patient's telecom/contact points
            email = None
            telecom = patient_data.get("telecom", [])
            for contact in telecom:
                if contact.get("system") == "email":
                    email = contact.get("value")
                    break

            # If no email in context, try to fetch from SDK data model
            if not email:
                try:
                    patient = Patient.objects.get(id=patient_id)
                    for contact_point in patient.patient_contactpoint_set.all():
                        if contact_point.system == "email":
                            email = contact_point.value
                            break
                except:
                    pass

            if not email:
                # No email available, can't send portal invite
                return []

            effects = []

            # Try to update the portal user with the email
            # Using UPDATE_USER effect to set portal contact
            try:
                effects.append(
                    Effect(
                        type=EffectType.UPDATE_USER,
                        payload={
                            "patient_id": patient_id,
                            "portal_email": email,
                        }
                    )
                )
            except:
                pass

            # Send the portal invite
            effects.append(
                Effect(
                    type=EffectType.PATIENT_PORTAL__SEND_INVITE,
                    payload={"patient_id": patient_id}
                )
            )

            return effects

        except:
            return []
