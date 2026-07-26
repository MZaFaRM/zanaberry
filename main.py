from core.states.default.state import DefaultState
from core.states.petting.state import PettingState
from core.states.temperature.state import ResourceIntensive
from core.states.tracking.state import MouseTrackingState
from engine import FaceEngine

if __name__ == "__main__":
    engine = FaceEngine(
        states=[
            DefaultState(),
            ResourceIntensive(),
            MouseTrackingState(),
            PettingState(),
        ]
    )

    engine.run()
