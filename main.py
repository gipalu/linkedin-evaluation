from fastapi import FastAPI
from pydantic import BaseModel

from services import linkedin_evaluation


app = FastAPI()


class Info(BaseModel):
    linkedinData : dict
    userId : str
    level : int
    highlightedSkills: list
    secondarySkills: list
    career: str

@app.post("/ezdevs/linkedin-evaluation")
def get_score(info: Info):
    response = linkedin_evaluation(info.dict())
    return response