from pydantic import BaseModel


class SuccessMessageResponse(BaseModel):
    message: str
