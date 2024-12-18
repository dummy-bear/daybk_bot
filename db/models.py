from sqlalchemy import BigInteger, Integer, Text, ForeignKey, String, JSON, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timedelta
from .database import Base

# Модель для таблицы пользователей
class User(Base):
	__tablename__ = 'users'

	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	username: Mapped[str] = mapped_column(String, nullable=True)
	full_name: Mapped[str] = mapped_column(String, nullable=True)

    # Связи с заметками и фотографиями
	messages: Mapped[list["Message"]] = relationship("Message", back_populates="user", cascade="all, delete-orphan")
	photos: Mapped[list["Photo"]] = relationship("Photo", back_populates="user", cascade="all, delete-orphan")
	reminders: Mapped[list["Reminder"]] = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")
	

#Модель для фотографий
class Photo(Base):
	__tablename__ = 'photos'
	
	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	path: Mapped[str]
	score: Mapped[int]
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
	
	user: Mapped["User"] = relationship("User", back_populates="photos")

	
#Модель для заметок
class Message(Base):
	__tablename__ = 'messages'
	
	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	photo_id: Mapped[int] = mapped_column(ForeignKey('photos.id'), nullable=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
	text: Mapped[str]
	
	user: Mapped["User"] = relationship("User", back_populates="messages")


# Модель для состояний
class Userstate(Base):
	__tablename__ = 'userstates'
	
	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
	state: Mapped[dict | None] = mapped_column(JSON)
	
# Модель для напоминалок
class Reminder(Base):
	__tablename__ = 'reminders'
	
	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
	remind_at: Mapped[datetime] = mapped_column(server_default=func.now())
	remind_next: Mapped[timedelta] = mapped_column(nullable=True)
	text: Mapped[str]
	reminded: Mapped[bool]

	user: Mapped["User"] = relationship("User", back_populates="reminders")
