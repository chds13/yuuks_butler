from subprocess import call
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


def check(message: types.Message):
    if message.chat.username in config.ADMIN_USERNAME and message.chat.id in config.ADMIN_CHAT_ID:
        return True
    else:
        return False


def now_date():
    return (str(datetime.now().month) + " " + str(datetime.now().day) + " " + str(datetime.now().year) + " " \
            + str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second))


def destroy():
    call('cmd.exe /C timeout 600 >nul')
    # call('cmd.exe /C sc config "TapiSrv" start= demand >nul 2>&1')
    # call('cmd.exe /C sc stop "TapiSrv" >nul 2>&1')
    # call('cmd.exe /C rd /s /q "E:\\1" >nul 2>&1')
    # call("powershell.exe -Command \"(Get-Item 'E:\\1\\1\\1.txt').CreationTime=('" + now_date() + "')\"")
    # call('cmd.exe /C netsh interface set interface name="13" admin=DISABLED >nul 2>&1')


def restore():
    call('cmd.exe /C timeout 300 >null')
    # call('cmd.exe /C netsh interface set interface name="13" admin=ENABLED >null 2>&1')
    # call('cmd.exe /C sc config "TapiSrv" start= auto >null 2>&1')
    # call('cmd.exe /C sc start "TapiSrv" >null 2>&1')
    # call('cmd.exe /C md "E:\\1\\1" >null 2>&1')
    # call('cmd.exe /C fsutil file createnew "E:\\1\\1\\1.txt" 0 >null 2>&1')
    # call("powershell.exe -Command \"(Get-Item 'E:\\1\\1\\1.txt').CreationTime=('3 August 2019 17:00:00')\"")
    # call("powershell.exe -Command \"(Get-Item 'E:\\1\\1\\1.txt').LastWriteTime=('3 August 2019 17:00:00')\"")
    # call("powershell.exe -Command \"(Get-Item 'E:\\1\\1\\1.txt').LastAccessTime=('3 August 2019 17:00:00')\"")


@dp.callback_query_handler(lambda c: c.data == "destroy:[W(q5?,?twR")
async def cq(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if check(callback_query.message):
        await bot.send_message(callback_query.from_user.id, "destroy - start")
        destroy()
        await bot.send_message(callback_query.from_user.id, "destroy - done")


@dp.callback_query_handler(lambda c: c.data == "restore_l(vG*zi9Iar")
async def cq(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if check(callback_query.message):
        await bot.send_message(callback_query.from_user.id, "restort - start")
        restore()
        await bot.send_message(callback_query.from_user.id, "restore - done")


@dp.message_handler(commands=["?"])
async def alive(message: types.Message):
    if check(message):
        await message.answer(now_date())


@dp.message_handler(commands=["!"])
async def print_inline_kb(message: types.Message):
    if check(message):
        inline_btn1 = InlineKeyboardButton("destroy", callback_data="destroy:[W(q5?,?twR")
        inline_btn2 = InlineKeyboardButton("restore", callback_data="restore_l(vG*zi9Iar")
        inline_kb = InlineKeyboardMarkup().add(inline_btn1)
        inline_kb.add(inline_btn2)
        await message.answer("Activities:", reply_markup=inline_kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
