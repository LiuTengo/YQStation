import datetime
import os
import random
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from repository.RepositoryData import Lecture, LectureStatus
from repository.ExcelRepository import ExcelRepository
from service.LectureService import LectureService

from requestModel import LoginRequest,SigninRequest,CreateLectureRequest
from util.jwt_utils import create_token,decode_token

app = FastAPI()
EXCEL_SAVE_PATH = "./data/excel"
repo = ExcelRepository(EXCEL_SAVE_PATH)
lecture_service = LectureService(repo)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        # 手机访问前端地址
        "https://192.168.1.6:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello":"World"}

#Login 登录
@app.post("/api/login")
def login(data : LoginRequest):
    if data.login_role == "student":   
        student = lecture_service.login_student(data.login_id,data.login_name)
        if student:
            token = create_token(data.login_id)
            return {"login_res": True,
                    "token": token,
                    "role" : "student",
                    "student_info":
                        {
                            "id": student.id,
                            "name": student.name,
                            "major": student.major,
                            "grade": student.grade
                        }}
    else:
        manager = lecture_service.login_manager(data.login_id, data.login_name)
        if manager:
            token = create_token(data.login_id)
            return {"login_res": True,
                    "token": token,
                    "role" : "manager",
                    "manager_info":
                        {
                            "id": manager.id,
                            "name": manager.name
                        }}
        
    return {"login_res": False}

#签到
@app.post("/api/signin")
def signin(data : SigninRequest):
    res = lecture_service.signin(data.manager_id, data.client_id, data.activity_id)
    return {"signin_res":res}

@app.post("/api/signin_token")
def signin_token(data : SigninRequest):
    std_id = decode_token(data.client_id) #token解码
    res = lecture_service.signin(data.manager_id, std_id["student_id"], data.activity_id)
    return {"signin_res":res}

#签退
@app.post("/api/signout")
def signout(data : SigninRequest):
    res = lecture_service.signout(data.manager_id, data.client_id, data.activity_id)
    return {"signout_res":res}

@app.post("/api/reserve")
def reserve(data : SigninRequest):
    try:
        lecture_service.reserve_lecture(data.activity_id, data.client_id)
        return {"reserve_res": True}
    except HTTPException as e:
        if e.status_code == 404:
            return {"reserve_res": False, "error": "活动不存在或已预约过"}
        else:
            raise e

#获取学生在指定活动的状态
@app.get("/api/student_lecture_status")
def get_student_lecture_status(student_id: str, lecture_id: str):
    return lecture_service.get_student_lecture_status(lecture_id, student_id)

#获取学生预约的活动列表
@app.get("/api/reserved_lectures", response_model=list[LectureStatus])
def get_reserved_lectures(student_id: str):
    return lecture_service.get_reserved_lectures(student_id)

#获取所有活动列表
@app.get("/api/all_lectures",response_model=list[Lecture])
def get_all_lectures():
    return lecture_service.get_all_lectures()

#获取指定活动的活动详情
@app.get("/api/lecture/detail",response_model=Lecture)
def get_lecture(lecture_id: str):
    lecture = lecture_service.get_lecture_by_id(lecture_id)
    if lecture is None:
        raise HTTPException(status_code=404, detail="活动不存在")
    return lecture

#添加新活动
@app.post("/api/lecture/create")
def create_lecture(data : CreateLectureRequest):
    lid = lecture_service.create_lecture(
        name=data.name,
        description=data.description,
        time=data.time,
        location=data.location
    )
    return {"code": 200, "msg": "活动创建成功", "lecture_id": lid}



#Deprecated API, for testing only
#Test Function
@app.get("/api/random_num")
def get_random_number():
    return{"random" : random.randint(1,100)}
# 创建活动
@app.post("/api/lecture/create")
def create_lecture_api(name: str, description: str, activity_time: str, location: str):
    lid = lecture_service.create_lecture(
        name=name,
        description=description,
        time=activity_time,
        location=location
    )
    return {"code": 200, "msg": "活动创建成功", "lecture_id": lid}

# 1. 导入学生Excel名单
@app.post("/api/student/import")
async def import_student_list(file: UploadFile = File(...)):
    try:
        temp_file = f"temp_{file.filename}"
        with open(temp_file, "wb") as f:
            f.write(await file.read())
        repo.import_students(temp_file)
        os.remove(temp_file)
        return {"code": 200, "msg": "学生名单导入成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"导入失败：{str(e)}")
    
# 5. 学生预约活动
@app.post("/api/reserve")
async def student_reserve(lecture_id: str, student_id: str):
    lecture_service.reserve_lecture(lecture_id, student_id)
    return {"code": 200, "msg": "活动预约成功"}