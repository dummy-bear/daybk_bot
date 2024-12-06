from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from db.dao import set_user, process_text, show_posts
from keyboards.all_kb import main_kb, create_spec_kb
from create_bot import bot
from datetime import date
from os import makedirs, path, listdir

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
	user = await set_user(tg_id=message.from_user.id, username=message.from_user.username, full_name=message.from_user.full_name)
	await message.answer('Привет, ' + str(message.from_user.first_name) + '! Этот бот просто запоминает всё, что вы ему пишете, а потом выдаёт по запросу.')

@start_router.message(Command('home'))
async def cmd_start_2(message: Message):
    await message.answer('Возвращаемся к началу')
    
@start_router.message(Command('show'))
async def cmd_show(message: Message):
	ans = await show_posts(tg_id=message.from_user.id, date=message.text)
	await message.answer(ans)    

@start_router.message(F.text)
async def cmd_test_3(message: Message):
	ans = await process_text(tg_id=message.from_user.id, text=message.text)
	if ans:
		await message.answer(ans)

@start_router.message(F.photo)
async def cmd_test_phot(message: Message):
	print ("Получено изображение",message.photo)
	print ("Текст к фото",message.caption)
	photo_id = message.photo[-1].file_id
	photo_path = str(message.from_user.id) +"/"+str(date.today().year)+"/"+str(date.today().month)+"/"+str(date.today().day)+"/"
	if not path.exists(photo_path):
		makedirs(photo_path)
	photo_name = str (len(listdir(photo_path))+1)+".jpg"
	photo = await bot.get_file(photo_id)
	await bot.download(photo,destination=photo_path+photo_name)
	await process_text(tg_id=message.from_user.id, text=message.caption, photo=photo_path+photo_name)
	#await photo.download(f'photo{photo_id}.jpg')

@start_router.message(F.document)
async def cmd_test_file(message: Message):
	print ("Получен файл",message.__dict__)
	print ("Текст к файлу",message.caption)
