

class UserMemoryNotFound(Exception):
    def __init__(self, message="Я вас не совсем понял. Уточните, пожалуйста"):
        self.message = message
        super().__init__(self.message)


class CrmFieldNotFound(Exception):
    def __init__(self, message="Я вас не совсем понял. Уточните, пожалуйста"):
        self.message = message
        super().__init__(self.message)


class JsonParseError(Exception):
    def __init__(self, message="Я вас не совсем понял. Уточните, пожалуйста"):
        self.message = message
        super().__init__(self.message)

