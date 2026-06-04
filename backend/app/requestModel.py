from pydantic import BaseModel

from datetime import datetime

class LoginRequest(BaseModel):
    login_role : str
    login_id : str
    login_name : str
    
class SigninRequest(BaseModel):
    manager_id : str
    client_id : str
    activity_id : str
    
class CreateLectureRequest(BaseModel):
    name : str
    description : str
    time : datetime
    location : str