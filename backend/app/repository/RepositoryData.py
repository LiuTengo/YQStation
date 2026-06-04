from enum import Enum
from datetime import datetime
from pydantic import BaseModel

#参与人员状态
class ParticipantStatus(str,Enum):
    NotReserved = "未预约"
    Reserved = "已预约"
    SignIn = "已签到"
    SignOut = "已签退"
    Absent = "缺席"

#活动/讲座信息
class Lecture(BaseModel):
    id : str #活动id
    name : str #活动名称
    description : str #活动描述
    start_time : datetime #活动开始时间
    created_time : datetime = datetime.now() #活动创建时间
    location : str #活动地点
    
class Student(BaseModel):
    id : str #学生id
    name : str #学生姓名
    grade : str #年级
    major : str #专业
    
class LectureManager(BaseModel):
    id : str #管理员/教师id
    name : str #管理员/教师姓名
    
#参加活动人员信息
class LectureParticipant(BaseModel):
    id : str #人员id
    name : str #人员名称
    grade : str #年级
    major : str #专业
    status : ParticipantStatus #状态
    
class LectureStatus(BaseModel):
    lecture_id: str
    lecture_name: str
    start_time: datetime
    status: ParticipantStatus
