"""Portal Invite - sends portal invite on patient creation."""

import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.protocols import BaseProtocol


class PortalInvite(BaseProtocol):
    RESPONDS_TO = ["PATIENT_CREATED"]

    def compute(self):
        patient_key = self.target
        return [
            Effect(
                type=EffectType.PATIENT_PORTAL__SEND_INVITE,
                payload=json.dumps({"patient_key": patient_key}),
            )
        ]
