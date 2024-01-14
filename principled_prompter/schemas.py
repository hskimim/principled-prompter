from pydantic import BaseModel


class FewShotSamplesAboutPrinciples(BaseModel):
    before_principle: str
    after_principle: str


class Principles(BaseModel):
    advice: str
    few_shot_samples: list[FewShotSamplesAboutPrinciples]


class CalibratedPrompt(BaseModel):
    question: str
    calibrated_question: str
    followed_principles: list[str]
