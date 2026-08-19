from uuid import UUID

class CallbackNotFound(Exception):
    def __init__(self, callback_id: UUID) -> None:
        super().__init__(f"Callback {callback_id} not found")
        self.callback_id = callback_id
class InvalidPhoneNumber(Exception):
    pass