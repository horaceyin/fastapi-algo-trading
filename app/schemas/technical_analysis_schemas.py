from pydantic import BaseModel

class GetDoneTradeModel(BaseModel):
    sessionToken: str
    targetAccNo: str