from engine import FaceEngine
from expressions.happy import Happy
from expressions.normal import Normal

if __name__ == "__main__":
    engine = FaceEngine()

    engine.register_expression("normal", Normal())
    engine.register_expression("happy", Happy())


    engine.run()
