class Require:
    @staticmethod
    def that(condition: bool, message: str):
        if not condition:
            raise Exception(message)
