from abc import ABC, abstractmethod
from typing import List, Optional

from repository.RepositoryData import LectureManager, ParticipantStatus,Lecture,LectureParticipant, Student

class IRepository(ABC):
    
    #基础流程相关
    def find_student(self,id:str,name:str)->bool:
        pass
    
    #活动/讲座相关
    @abstractmethod
    def create_lecture(self,lecture : Lecture) -> None:
        pass
    
    @abstractmethod
    def get_all_lectures(self) -> List[Lecture]:
        pass
    
    @abstractmethod
    def get_lecture(self,lecture_id : str)->Lecture:
        pass
    

    #参与人员相关
    @abstractmethod
    def add_participant(self,lecture_id : str, participant : LectureParticipant)->None:
        pass
    
    
    @abstractmethod
    def update_participant_status(self,lecture_id : str, 
                                  participant_id : str,
                                  new_status : ParticipantStatus) -> None:
        pass
    
    @abstractmethod
    def get_student(self,student_id : str)->Student:
        pass
    
    @abstractmethod
    def get_manager(self,manager_id : str)->LectureManager:
        pass
    
    @abstractmethod
    def get_student_in_activity(self,lecture_id: str, student_id: str) -> LectureParticipant:
        pass
    
    @abstractmethod
    def get_participant(self,lecture_id: str,student_id: str) -> Optional[LectureParticipant]:
        pass
    
    @abstractmethod
    def get_lecture_participants(self, lecture_id : str) -> List[LectureParticipant]:
        pass
    