import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from db.dao import send_reminders
# from work_time.time_func import send_time_msg

async def main():
    scheduler.add_job(send_time_msg, 'interval', seconds=30)
    scheduler.start()
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
async def send_time_msg():
	await send_reminders ()

if __name__ == "__main__":
    asyncio.run(main())
