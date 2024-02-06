from pydantic import BaseModel, Field


class SuccessCreateResponse(BaseModel):
    message: str
