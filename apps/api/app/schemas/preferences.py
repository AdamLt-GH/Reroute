from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.scheduling.domain.preferences import ConstraintKind, PreferenceKind

type JsonValue = (
    str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]
)


class ConstraintCreate(BaseModel):
    kind: ConstraintKind
    settings: dict[str, JsonValue] = Field(default_factory=dict)
    enabled: bool = True


class PreferenceCreate(BaseModel):
    kind: PreferenceKind
    weight: float = Field(default=1.0, ge=0, le=100)
    settings: dict[str, JsonValue] = Field(default_factory=dict)
    enabled: bool = True


class ConstraintResponse(ConstraintCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class PreferenceResponse(PreferenceCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
