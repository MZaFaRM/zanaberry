from engine import FaceEngine
from expressions.curious import Curious
from expressions.happy import Happy
from expressions.normal import Normal

if __name__ == "__main__":
    engine = FaceEngine()

    engine.register_expression("normal", Normal())
    engine.register_expression("happy", Happy(), chance=0.25, duration_ms=1500)
    engine.register_expression("curious", Curious(), chance=0.1, duration_ms=1500)


    engine.run()
