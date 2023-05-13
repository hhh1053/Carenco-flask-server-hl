from datetime import datetime
from sqlalchemy import Column, DateTime


class BaseTimeEntity:
    insert_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, onupdate=datetime.now)
    delete_yn = Column(str(1), default='N')
    delete_time = Column(DateTime)

    def soft_delete(self):
        self.delete_yn = 'Y'
        self.delete_time = datetime.now()