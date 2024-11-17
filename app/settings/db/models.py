from datetime import datetime
from sqlalchemy import Enum

from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from sqlalchemy.orm import relationship

from app.enums.tasks import TaskStatus, TaskPriority

Base = declarative_base()


Ssubscriptions = db.Table(
    'Ssubscriptions', Base.metadata,
    db.Column('user_id', db.BigInteger, db.ForeignKey('Users.id'), primary_key=True),
    db.Column('task_id', db.BigInteger, db.ForeignKey('Tasks.id'), primary_key=True)
)


class Tasks(Base):
    __tablename__ = 'Tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column("task_name", db.String)
    task_descriptions = db.Column("task_descriptions", db.String)
    status = db.Column(Enum(TaskStatus, native_enum=False), default=TaskStatus.NEW, nullable=False)
    priority = db.Column(Enum(TaskPriority, native_enum=False), default=TaskPriority.LOW, nullable=False)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow())
    creator_id = db.Column(db.BigInteger, db.ForeignKey("Users.id"))  # Внешний ключ, связывающий задачу с пользователем
    creator = relationship("Users", back_populates="tasks")  # Отношение к пользователю
    subscribers = relationship("Users", secondary=Ssubscriptions,
                               back_populates="subscribed_tasks")  # Связь с подписчиками


class Users(Base):
    __tablename__ = "Users"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column("name", db.String)
    username = db.Column("username", db.String)
    password = db.Column("password", db.String)
    email = db.Column("email", db.String)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow())
    is_verified = db.Column("is_verified", db.Boolean, default=False)
    tasks = relationship("Tasks", back_populates="creator")
    subscribed_tasks = relationship("Tasks", secondary=Ssubscriptions,
                                    back_populates="subscribers")  # Связь с подписками пользователя на задачи
