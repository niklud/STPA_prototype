from sqlalchemy import Boolean, DateTime, ForeignKey, Column, Integer, String
from datetime import datetime

from stpa_prototype.database.database_project import ProjectDB


class Goal(ProjectDB.PBase):
    __tablename__ = 'system_goals'
    id = Column('goal_id', Integer, primary_key=True)
    title = Column(String(60))
    text = Column(String)
    vcs_check = Column(Boolean)
    pub_date = Column(DateTime)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.vcs_check = False
        self.pub_date = datetime.utcnow()
