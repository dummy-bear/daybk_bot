from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    BigInteger, Text, Column, DateTime, ForeignKey, Numeric, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime,timedelta
from sqlalchemy import func

engine = create_engine("")

class Base(DeclarativeBase):
    pass

# Модель для таблицы пользователей
class User(Base):
	__tablename__ = 'users'

	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	username: Mapped[str] = mapped_column(String, nullable=True)
	full_name: Mapped[str] = mapped_column(String, nullable=True)
	created_at: Mapped[datetime] = mapped_column(server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    # Связи с заметками и фотографиями
	messages: Mapped[list["Message"]] = relationship("Message", back_populates="user", cascade="all, delete-orphan")
	photos: Mapped[list["Photo"]] = relationship("Photo", back_populates="user", cascade="all, delete-orphan")
	reminders: Mapped[list["Reminder"]] = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")
	
# Модель для напоминалок
class Reminder(Base):
	__tablename__ = 'reminders'
	
	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
	remind_at: Mapped[datetime] = mapped_column(server_default=func.now())
	remind_next: Mapped[timedelta] = mapped_column(nullable=True)
	text: Mapped[str]
	reminded: Mapped[bool]
	created_at: Mapped[datetime] = mapped_column(server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
	
	user: Mapped["User"] = relationship("User", back_populates="reminders")
	
Base.metadata.create_all(engine)
engine.connect()

print(engine)
