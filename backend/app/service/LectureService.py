from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException

from repository.IRepository import IRepository
from repository.RepositoryData import LectureStatus, ParticipantStatus,Lecture,LectureParticipant, Student

class LectureService():
    
    def __init__(self,repo : IRepository):
        self.repo = repo
        pass
    
    ##登录等流程方法
    def login_student(self, id : str, name : str) -> Student:
        student = self.repo.get_student(id)
        if student.name == name:
            return student
        
        return None

    def login_manager(self, id : str, name : str) -> Student:
        manager = self.repo.get_manager(id)
        if manager.name == name:
            return manager

        return None
    
    ##学生签到
    def signin(self, manager_id : str, client_id : str, activity_id : str) -> bool:
        # 1. 检查活动是否存在
        lecture = self.repo.get_lecture(activity_id)
        if lecture is None:
            #TODO: 这里应该区分活动不存在和其他错误，目前先统一返回 404
            raise HTTPException(
                status_code=404,
                detail="活动不存在"
            )

        # 2. 获取学生信息
        student = self.repo.get_student_in_activity(activity_id, client_id)
        if student is None:
            return False
        
        if student.status != ParticipantStatus.Reserved:
            #TODO: 这里应该区分活动不存在和其他错误，目前先统一返回 404
            raise HTTPException(
                status_code=404,
                detail="已预约过该活动"
            )
        else:
            # 3. 写入活动预约名单
            self.repo.update_participant_status(
                activity_id,
                student.id,
                ParticipantStatus.SignIn
            )
            return True
    
    ##学生签退
    def signout(self, manager_id : str, client_id : str, activity_id : str) -> bool:
        # 1. 检查活动是否存在
        lecture = self.repo.get_lecture(activity_id)
        if lecture is None:
            #TODO: 这里应该区分活动不存在和其他错误，目前先统一返回 404
            raise HTTPException(
                status_code=404,
                detail="活动不存在"
            )

        # 2. 获取学生信息
        try:
            student = self.repo.get_student_in_activity(activity_id, client_id)
        except ValueError:
            #TODO: 这里应该区分活动不存在和其他错误，目前先统一返回 404
            raise HTTPException(
                status_code=404,
                detail="查无此学生"
            )
            
        if student.status != ParticipantStatus.SignIn:
            #TODO: 这里应该区分活动不存在和其他错误，目前先统一返回 404
            raise HTTPException(
                status_code=400,
                detail="已预约过该活动"
            )
        else:
            # 3. 写入活动预约名单
            self.repo.update_participant_status(
                activity_id,
                student.id,
                ParticipantStatus.SignOut
            )
            return True
            
        
    ##获取学生预约课程状态
    def get_student_lecture_status(self, lecture_id : str,student_id: str) -> LectureStatus:
            participant = self.repo.get_student_in_activity(lecture_id, student_id)
            if participant:
                status = LectureStatus(
                    lecture_id= lecture_id,
                    lecture_name = self.repo.get_lecture(lecture_id).name,
                    start_time = self.repo.get_lecture(lecture_id).start_time,
                    status = participant.status
                )
                return status
            else:
                raise HTTPException(status_code=404, detail="未预约该活动")
        
    ##获取学生预约课程列表
    def get_reserved_lectures(self, student_id: str) -> List[LectureStatus]:
        lectures = self.repo.get_all_lectures()
        reserved_lectures = []
        for lecture in lectures:
            participant = self.repo.get_student_in_activity(lecture.id, student_id)
            if participant:
                status = LectureStatus(
                    lecture_id= lecture.id,
                    lecture_name = lecture.name,
                    start_time = lecture.start_time,
                    status = participant.status
                )
                reserved_lectures.append(status)
        return reserved_lectures


    ##讲座/活动方法
    # ============================
    # 创建讲座（自动生成文件夹作为 lecture_id）
    # ============================
    def create_lecture(self, name: str, description: str, time: datetime, location: str) -> str:
        # 自动生成 lecture_id = 年月日_活动名称
        date_str = datetime.now().strftime("%Y%m%d")
        safe_name = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
        lecture_id = f"{date_str}_{safe_name}"

        # 构建讲座对象
        lecture = Lecture(
            id=lecture_id,
            name=name,
            description=description,
            start_time=time,
            location = location
        )

        # 调用 repo → 创建文件夹 + Excel
        self.repo.create_lecture(lecture)
        return lecture_id

    # ============================
    # 获取所有活动列表
    # ============================
    def get_all_lectures(self):
        return self.repo.get_all_lectures()

    # ============================
    # 根据 ID 获取单个活动（ID = 文件夹名）
    # ============================
    def get_lecture_by_id(self, lecture_id: str):
        lecture = self.repo.get_lecture(lecture_id)
        if not lecture:
            raise HTTPException(status_code=404, detail="活动不存在")
        return lecture

    # ============================
    # 学生预约活动
    # ============================
    def reserve_lecture(self, lecture_id: str, student_id: str):
        student_id = str(student_id).strip()

        # 1. 检查活动是否存在
        lecture = self.repo.get_lecture(lecture_id)
        if lecture is None:
            raise HTTPException(
                status_code=404,
                detail="活动不存在"
            )

        # 2. 检查是否已经预约
        participant = self.repo.get_participant(
            lecture_id,
            student_id
        )

        if participant is not None:
            raise HTTPException(
                status_code=400,
                detail="已预约过该活动"
            )

        # 3. 获取学生信息
        try:
            student = self.repo.get_student(student_id)
        except ValueError:
            raise HTTPException(
                status_code=404,
                detail="查无此学生"
            )

        participant = LectureParticipant(
            id=student.id,
            name=student.name,
            grade=student.grade,
            major=student.major,
            status=ParticipantStatus.Reserved
        )

        # 4. 写入活动预约名单
        self.repo.add_participant(
            lecture_id,
            participant
        )


    # ============================
    # 学生签到
    # ============================
    def sign_in(self, lecture_id: str, student_id: str):
        # 1. 获取该活动所有参与记录
        participants = self.repo.get_lecture_participants(lecture_id)
        target = None

        for p in participants:
            if p.student_id == student_id:
                target = p
                break

        if not target:
            raise HTTPException(status_code=400, detail="未预约，无法签到")

        # 2. 状态校验
        if target.status == "已签到":
            raise HTTPException(status_code=400, detail="已签到，无需重复操作")
        if target.status == "已签退":
            raise HTTPException(status_code=400, detail="已签退，无法签到")

        # 3. 更新为已签到
        self.repo.update_participant_status(lecture_id, student_id, "已签到")

    # ============================
    # 学生签退
    # ============================
    def sign_out(self, lecture_id: str, student_id: str):
        participants = self.repo.get_lecture_participants(lecture_id)
        target = None

        for p in participants:
            if p.student_id == student_id:
                target = p
                break

        if not target:
            raise HTTPException(status_code=400, detail="无预约记录")

        if target.status != "已签到":
            raise HTTPException(status_code=400, detail="未签到，无法签退")

        self.repo.update_participant_status(lecture_id, student_id, "已签退")

    # ============================
    # 获取活动所有参与记录（管理员查看）
    # ============================
    def get_lecture_participants(self, lecture_id: str):
        return self.repo.get_lecture_participants(lecture_id)
    
    # ============================
    # 测试方法
    # ============================
    def add_participant(self,lecture_id : str,id:str,name:str):
        sid = LectureParticipant(
            id = id,
            name = name,
            grade = "2022",
            major = "GameDesign",
            status =  ParticipantStatus.NotReserved
        )
        
        self.repo.add_participant(lecture_id,sid)
        return sid