from create_bot import logger
from .base import connection
from .models import User, Userstate, Message, Photo
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from json import loads as jsloads

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
		else:
			new_message = Message(user_id=tg_id,text=text)
		session.add(new_message)
		await session.commit()
		#if text.split()[0].lower()=="напомни":
		#	return "Хорошо, напомню"
		
	except SQLAlchemyError as e:
		logger.error(f"Ошибка при получении состояния пользователя: {e}")
		await session.rollback()	

@connection
async def show_posts(session, tg_id: int, date: str):
	try:
		posts = await session.scalars(select(Message).filter_by(user_id=tg_id))
		ans=""
		for post in posts:
			ans+=str(post.created_at)+"\n"
			ans+=post.text+"\n\n"
		return ans
	except SQLAlchemyError as e:
		logger.error(f"Ошибка при получении состояния пользователя: {e}")
		await session.rollback()	
	pass
	
@connection
async def set_userstate(session, tg_id: int, state: str):
	pass
