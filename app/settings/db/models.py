from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from sqlalchemy.orm import relationship

Base = declarative_base()


Subscriptions = db.Table(
    'Subscriptions', Base.metadata,
    db.Column('user_id', db.BigInteger, db.ForeignKey('Users.id'), primary_key=True),
    db.Column('task_id', db.BigInteger, db.ForeignKey('Tasks.id'), primary_key=True)
)


class Tasks(Base):
    __tablename__ = 'Tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column("task_name", db.String)
    task_descriptions = db.Column("task_descriptions", db.String)
    status = db.Column("status", db.String)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow())
    creator_id = db.Column(db.BigInteger, db.ForeignKey("Users.id"))  # Внешний ключ, связывающий задачу с пользователем
    creator = relationship("Users", back_populates="tasks")  # Отношение к пользователю
    subscribers = relationship("Users", secondary=Subscriptions,
                               back_populates="subscribed_tasks")  # Связь с подписчиками


class Users(Base):
    __tablename__ = "Users"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column("name", db.String)
    username = db.Column("username", db.String)
    password = db.Column("password", db.String)
    email = db.Column("email", db.String)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow())
    tasks = relationship("Tasks", back_populates="creator")
    subscribed_tasks = relationship("Tasks", secondary=Subscriptions,
                                    back_populates="subscribers")  # Связь с подписками пользователя на задачи
