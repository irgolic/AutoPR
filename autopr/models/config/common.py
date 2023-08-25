import pydantic


class StrictModel(pydantic.BaseModel):
    class Config:
        extra = pydantic.Extra.forbid

        # Does not coerce when not necessary
        smart_union = True


# Use this to simulate the action/workflow invocation models in config
class ExtraModel(pydantic.BaseModel):
    class Config:
        extra = pydantic.Extra.allow
