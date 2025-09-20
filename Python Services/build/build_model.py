from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class Projects(BaseModel):
    projectName: str
    owner: str = None
    status :str

class ProjectsInDB(Projects):
    _id: ObjectId
    createdTime: datetime = Field(default_factory=datetime.utcnow)
    updatedTime: datetime = Field(default_factory=datetime.utcnow)

class changeModel(BaseModel):
    projectName: str
    userName: str

class BuildModel(BaseModel):
    fileName: str
    test_size = int
    algo: str
    pTune:bool


