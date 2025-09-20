from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId


class login(BaseModel):
    username: str
    password: str

class UserInDB(login):
    _id: ObjectId
    role: str = "public"
    firstName: str
    lastName: str
    securityQuestion: str
    securityAnswer: str
    createdTime: datetime = Field(default_factory=datetime.utcnow)

class UpdatePasswd(login):
    _id: ObjectId
    securityQuestion: str
    securityAnswer: str

class DataUploadModel(BaseModel):
    h1n1_concern : int =0
    h1n1_knowledge: int =0
    behavioral_antiviral_meds: int =0
    behavioral_avoidance: int =0
    behavioral_face_mask: int =0
    behavioral_wash_hands: int =0
    behavioral_large_gatherings: int =0
    behavioral_outside_home: int =0
    behavioral_touch_face: int =0
    doctor_recc_h1n1: int =0
    doctor_recc_seasonal: int =0
    chronic_med_condition: int =0
    child_under_6_months: int =0
    health_worker: int =0
    health_insurance: int =0
    opinion_h1n1_vacc_effective: int =0
    opinion_h1n1_risk: int =0
    opinion_h1n1_sick_from_vacc: int =0
    opinion_seas_vacc_effective: int =0
    opinion_seas_risk: int =0
    opinion_seas_sick_from_vacc: int =0
    age_group: str
    education: str
    race: str
    sex: str
    income_poverty: str
    marital_status: str
    rent_or_own: str
    employment_status: str
    hhs_geo_region: str
    census_msa: str
    household_adults: int =0
    household_children: int =0
    employment_industry: str
    employment_occupation: str