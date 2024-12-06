from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    BigInteger, Text, Column, DateTime, ForeignKey, Numeric, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
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
	
	

#Модель для фотографий
class Photo(Base):
	__tablename__ = 'photos'
	
	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	path: Mapped[str]
	score: Mapped[int]
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
	created_at: Mapped[datetime] = mapped_column(server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
	
#Модель для заметок
class Message(Base):
	__tablename__ = 'messages'
	
	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	photo_id: Mapped[int] = mapped_column(ForeignKey('photos.id'), nullable=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
	text: Mapped[str]

	created_at: Mapped[datetime] = mapped_column(server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


# Модель для состояний
class Userstate(Base):
	__tablename__ = 'userstates'
	
	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
	state: Mapped[dict | None] = mapped_column(JSON)
	created_at: Mapped[datetime] = mapped_column(server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


Base.metadata.drop_all(engine)    
Base.metadata.create_all(engine)
engine.connect()

print(engine)
