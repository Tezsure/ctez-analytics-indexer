# generated by datamodel-codegen:
#   filename:  withdraw.json

from __future__ import annotations

from pydantic import BaseModel, Extra


class WithdrawParameter(BaseModel):
    class Config:
        extra = Extra.forbid

    id: str
    amount: str
    to: str
