from core.states.default.state import DefaultState
from engine import FaceEngine

if __name__ == "__main__":
    engine = FaceEngine(states=[DefaultState()])

    engine.run()
