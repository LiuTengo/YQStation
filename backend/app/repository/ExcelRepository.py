import os
import pandas as pd
from datetime import datetime
from typing import List, Optional

from repository.RepositoryData import LectureManager, Student
from repository.IRepository import IRepository
from repository.IRepository import ParticipantStatus,Lecture,LectureParticipant

class ExcelRepository(IRepository):
    
    def __init__(self, root_excel_dir: str = "excel_data"):
        self.root_excel_dir = root_excel_dir
        self.student_file = os.path.join(root_excel_dir, "students.xlsx")
        self.lecture_file = os.path.join(root_excel_dir, "lecture.xlsx")
        self.manager_file = os.path.join(root_excel_dir, "manager.xlsx")
        os.makedirs(root_excel_dir, exist_ok=True)

    #基础流程相关
    def find_student(self,s_id:str,s_name:str)->bool:
        if not os.path.exists(self.student_file):
            raise ValueError("学生名单文件不存在")

        df = pd.read_excel(
            self.student_file,
            dtype={"id": str,"name":str}
        )

        student_id = str(s_id).strip()
        student_name = str(s_name).strip()

        print((df["id"] == student_id))
        print((df["name"] == student_name))

        row = df[(df["id"] == student_id) & (df["name"] == student_name)]
        if row.empty:
            raise ValueError("查无此人")

        return True

    # 🔴 核心：创建讲座 → 自动生成文件夹 = lecture_id
    # 文件夹名规则：YYYYMMDD_活动名称
    def create_lecture(self,lecture : Lecture) -> None:
        lecture_folder = os.path.join(
            self.root_excel_dir,
            lecture.id
        )

        os.makedirs(lecture_folder, exist_ok=True)

        info_path = os.path.join(
            lecture_folder,
            "lecture_info.json"
        )

        with open(info_path, "w", encoding="utf-8") as f:
            f.write(
                lecture.model_dump_json(
                    indent=2,
                    ensure_ascii=False
                )
            )

        record_path = os.path.join(
            lecture_folder,
            "participants.xlsx"
        )

        if not os.path.exists(record_path):

            df = pd.DataFrame(columns=[
                "id",
                "name",
                "grade",
                "major",
                "status"
            ])

            df.to_excel(record_path, index=False)

    # =================================================================
    # 🟢 获取所有活动（扫描文件夹 = 所有 lecture_id）
    # =================================================================
    def get_all_lectures(self) -> List[Lecture]:
        lectures = []
        if not os.path.exists(self.root_excel_dir):
            return lectures

        # 遍历文件夹 → 每个文件夹名就是一个 lecture_id
        for lecture_id in os.listdir(self.root_excel_dir):
            if lecture_id == "students.xlsx":
                continue

            info_path = os.path.join(self.root_excel_dir, lecture_id, "lecture_info.json")
            if os.path.exists(info_path):
                with open(info_path, "r", encoding="utf-8") as f:
                    lectures.append(Lecture.model_validate_json(f.read()))
        return lectures

    # =================================================================
    # 🟡 根据 ID 查询活动（ID = 文件夹名）
    # =================================================================
    def get_lecture(self, lecture_id: str) -> Optional[Lecture]:

        info_path = os.path.join(self.root_excel_dir, lecture_id, "lecture_info.json")
        
        if not os.path.exists(info_path):
            return None

        with open(info_path, "r", encoding="utf-8") as f:
            return Lecture.model_validate_json(f.read())

    # =================================================================
    # 🟣 学生相关
    # =================================================================
    def import_students(self, file_path: str) -> None:
        df = pd.read_excel(
            file_path,
            dtype={"student_id": str}
        )

        required = [
            "student_id",
            "name",
            "class_name"
        ]

        if not all(c in df.columns for c in required):
            raise ValueError(
                "Excel必须包含：student_id、name、class_name"
            )

        # 转内部统一格式
        df = df.rename(columns={
            "student_id": "id",
            "class_name": "major"
        })

        df["grade"] = "2022"

        df.to_excel(
            self.student_file,
            index=False
        )


    # =================================================================
    # 🟠 添加预约记录
    # =================================================================
    def add_participant(self, lecture_id: str, participant: LectureParticipant) -> None:
        record_path = os.path.join(
            self.root_excel_dir,
            lecture_id,
            "participants.xlsx"
        )

        if not os.path.exists(record_path):
            raise ValueError("活动不存在")

        df = pd.read_excel(
            record_path,
            dtype={"id": str}
        )

        if not df[df["id"] == participant.id].empty:
            raise ValueError("已预约")

        new_row = participant.model_dump()

        new_row["status"] = participant.status.value

        df = pd.concat(
            [df, pd.DataFrame([new_row])],
            ignore_index=True
        )

        df.to_excel(
            record_path,
            index=False
        )

    # =================================================================
    # 🔵 更新状态：签到 / 签退
    # =================================================================
    def update_participant_status(self, lecture_id: str, student_id: str, new_status : ParticipantStatus) -> None:
        record_path = os.path.join(
            self.root_excel_dir,
            lecture_id,
            "participants.xlsx"
        )

        df = pd.read_excel(
            record_path,
            dtype={"id": str}
        )

        idx = df[df["id"] == str(student_id)].index

        if len(idx) == 0:
            raise ValueError("无预约记录")

        df.loc[idx, "status"] = new_status.value

        df.to_excel(
            record_path,
            index=False
        )

    # =================================================================
    # 🟤 获取某个活动的所有参与记录
    # =================================================================
    def get_lecture_participants(self, lecture_id: str) -> List[LectureParticipant]:
        record_path = os.path.join(
            self.root_excel_dir,
            lecture_id,
            "participants.xlsx"
        )

        if not os.path.exists(record_path):
            return []

        df = pd.read_excel(
            record_path,
            dtype={
                "id": str,
                "grade": str
            }
        )

        participants = []

        for _, row in df.iterrows():

            participant = LectureParticipant(
                id=str(row["id"]),
                name=row["name"],
                grade=str(row["grade"]),
                major=row["major"],
                status=ParticipantStatus(
                    int(row["status"])
                )
            )

            participants.append(participant)

        return participants
    

    
    def get_student(self,student_id : str)->Student:
        if not os.path.exists(self.student_file):
            raise ValueError(
                "学生名单文件不存在"
            )

        df = pd.read_excel(
            self.student_file,
            dtype={"id": str}
        )

        student_id = str(student_id).strip()

        row = df[df["id"] == student_id]

        if row.empty:
            raise ValueError("查无此人")

        row = row.iloc[0]

        return Student(
            id=row["id"],
            name=row["name"],
            grade=str(row["grade"]),
            major=row["major"]
        )
        
    def get_manager(self,manager_id : str)->LectureManager:
        if not os.path.exists(self.manager_file):
            raise ValueError(
                "管理员名单文件不存在"
            )

        df = pd.read_excel(
            self.manager_file,
            dtype={"manager_id": str}
        )

        mag_id = str(manager_id).strip()

        row = df[df["manager_id"] == mag_id]

        if row.empty:
            raise ValueError("查无此人")

        row = row.iloc[0]

        return LectureManager(
            id=row["manager_id"],
            name=row["manager_name"]
        )
        
    def get_student_in_activity(self,lecture_id: str, student_id: str) -> LectureParticipant:
        record_path = os.path.join(
            self.root_excel_dir,
            lecture_id,
            "participants.xlsx"
        )

        if not os.path.exists(record_path):
            return None

        df = pd.read_excel(
            record_path,
            dtype={
                "id": str,
                "grade": str
            }
        )

        student_id = str(student_id).strip()

        row = df[df["id"] == student_id]

        if row.empty:
            return None

        row = row.iloc[0]

        return LectureParticipant(
            id=str(row["id"]),
            name=row["name"],
            grade=str(row["grade"]),
            major=row["major"],
            status=ParticipantStatus(
                str(row["status"])
            )
        )
        
    def get_participant(self,lecture_id: str,student_id: str
    ) -> Optional[LectureParticipant]:

        record_path = os.path.join(
            self.root_excel_dir,
            lecture_id,
            "participants.xlsx"
        )

        if not os.path.exists(record_path):
            return None

        df = pd.read_excel(
            record_path,
            dtype={
                "id": str,
                "grade": str
            }
        )

        student_id = str(student_id).strip()

        row = df[df["id"] == student_id]

        if row.empty:
            return None

        row = row.iloc[0]

        return LectureParticipant(
            id=str(row["id"]),
            name=row["name"],
            grade=str(row["grade"]),
            major=row["major"],
            status=ParticipantStatus(
                int(row["status"])
            )
        )