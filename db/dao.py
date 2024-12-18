from create_bot import bot, logger
from .base import connection
from .models import User, Userstate, Message, Photo, Reminder
from sqlalchemy import select, func
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from json import loads as jsloads
from datetime import datetime
from .filterdate import Filterdates


@connection
async def set_user(session, tg_id: int, username: str, full_name: str) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            new_user = User(id=tg_id, username=username, full_name=full_name)
            session.add(new_user)
            new_state = Userstate(user_id=tg_id, state="{\"state\": \"start\"}")
            session.add(new_state)
            await session.commit()
            logger.info(f"Зарегистрировал пользователя с ID {tg_id}!")
            return None
        else:
            logger.info(f"Пользователь с ID {tg_id} найден!")
            return user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        await session.rollback()

@connection
async def process_text(session, tg_id: int, text: str, photo: str):
	logger.info(f"Пользователь {tg_id} написал {text}")
	try:
		state = await session.scalar(select(Userstate).filter_by(user_id=tg_id))
		logger.info(state.state)
		s=jsloads(state.state)
		if photo:
			new_photo = Photo(path=photo,score=0,user_id=tg_id)
			session.add(new_photo)
			await session.flush()
			new_message = Message(user_id=tg_id,text=text,photo_id=new_photo.id)
		elif text[0]=='/':
			return "Не понимаю команды "+text
		else:
			new_message = Message(user_id=tg_id,text=text)
		
		session.add(new_message)
		await session.flush()
		state.state="{\"state\": \"message\", \"last_mes_id\": "+str(new_message.id)+"}"
		logger.info(state.state)
		await session.commit()
		#if text.split()[0].lower()=="напомни":
		#	return "Хорошо, напомню"
		
	except SQLAlchemyError as e:
		logger.error(f"Ошибка при записи сообщения: {e}")
		await session.rollback()	

@connection
async def show_posts(session, tg_id: int, date: str):
	logger.info("запрос постов: "+date)
	try:
		dates=Filterdates(date)
		posts = await session.scalars(select(Message).filter(Message.user_id==tg_id,Message.created_at.between(dates.frm,dates.to)))
		ans=""
		for post in posts:
			ans+=str(post.created_at)+"("+str(post.id)+"):\n"
			ans+=post.text+"\n\n"
		if ans=="":
			return "Нет сообщений на дату "+date
		else:
			return ans
	except SQLAlchemyError as e:
		logger.error(f"Ошибка при показе постов: {e}")
		await session.rollback()	
	pass
	
@connection
async def show_reminders(session, tg_id: int, text: str):
	try:
		reminders = await session.scalars(select(Reminder).filter(Reminder.user_id==tg_id,Reminder.reminded==False))
		ans=""
		for rem in reminders:
			ans+=str(rem.remind_at)+"("+str(rem.text)+", поставлено "+str(rem.created_at)+")\n"

		if ans=="":
			return "У вас нет ожидаемых напоминаний"
		else:
			return ans
	except SQLAlchemyError as e:
		logger.error(f"Ошибка при показе напоминаний: {e}")
		await session.rollback()	
	pass
	
@connection
async def add_reminder(session, tg_id: int, text: str):
	logger.info("добавляем напоминалку: "+text)
	
	try:
		state = await session.scalar(select(Userstate).filter_by(user_id=tg_id))
		s=jsloads(state.state)
		dates=Filterdates(text)
		print (s,dates)
		if s["last_mes_id"]:
			new_reminder=Reminder(user_id=tg_id,remind_at=dates.frm,text=str(s["last_mes_id"]),reminded=False)
			session.add(new_reminder)
			await session.commit()
			ans="поставил напоминалку на "+str(dates.frm)
		else:
			ans="что-то пошло не так"
		return ans
		
	except SQLAlchemyError as e:
		logger.error(f"Ошибка при показе постов: {e}")
		await session.rollback()	
	pass


@connection
async def send_reminders(session):
	try:
		actual_reminders = await session.scalars(select(Reminder).filter(Reminder.reminded==False,Reminder.remind_at<=func.now()))
		for rem in actual_reminders:
			message = await session.scalar(select(Message).filter_by(id=int(rem.text)))
			await bot.send_message(rem.user_id,"Напоминаю:\n"+message.text)
			rem.reminded=True
		await session.commit()
		
	except SQLAlchemyError as e:
		logger.error(f"Ошибка при отправке напоминалок: {e}")
		await session.rollback()	
	pass


@connection
async def set_userstate(session, tg_id: int, state: str):
	pass
