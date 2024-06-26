# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Extra


class Key(BaseModel):
    class Config:
        extra = Extra.forbid

    id: str
    owner: str


class Value(BaseModel):
    class Config:
        extra = Extra.forbid

    address: str
    ctez_outstanding: str
    tez_balance: str


class Oven(BaseModel):
    class Config:
        extra = Extra.forbid

    key: Key
    value: Value


class CtezAdminStorage(BaseModel):
    class Config:
        extra = Extra.forbid

    cfmm_address: str
    ctez_fa12_address: str
    drift: str
    last_drift_update: str
    metadata: Dict[str, str]
    ovens: List[Oven]
    target: str
