from subprocess import call
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


def check(message: Message):
    if message.chat.username in config.ADMIN_USERNAME and message.chat.id in config.ADMIN_CHAT_ID:
        return True
    else:
        return False


def set_date(opt):
    now = datetime.now()
    if opt == "now":
        return now.strftime("%m %d %Y %H:%M:%S")
    else:
        return (now - timedelta(days=int(opt))).strftime("%m %d %Y 0:1:1")


def destroy():
    # call return error code. Then you can use chain of commands with if call==0

    # call('cmd.exe /C timeout 6 >nul')
    # call('cmd.exe /C sc config "TapiSrv" start= demand >nul 2>&1')
    # call('cmd.exe /C sc stop "TapiSrv" >nul 2>&1')
    call('cmd.exe /C rd /s /q "E:\\1" >nul 2>&1')
    # call("powershell.exe -Command \"(Get-Item 'E:\\1\\1\\1.txt').CreationTime=('" +
    #     datetime.now().strftime("%m %d %Y %H:%M:%S") + "')\"")
    # call('cmd.exe /C netsh interface set interface name="13" admin=DISABLED >nul 2>&1')

    # change disk label
    # call('diskpart.exe /s C:\yuuks_butler\dp_scenario.txt >nul 2>&1')


def restore():
    # call('cmd.exe /C timeout 3 >nul')
    # call('cmd.exe /C netsh interface set interface name="13" admin=ENABLED >nul 2>&1')
    # call('cmd.exe /C sc config "TapiSrv" start= auto >nul 2>&1')
    # call('cmd.exe /C sc start "TapiSrv" >nul 2>&1')
    call('cmd.exe /C md "E:\\1\\1" >nul 2>&1')
    call('cmd.exe /C fsutil file createnew "E:\\1\\1\\1.txt" 0 >nul 2>&1')
    call("powershell.exe -Command \"(Get-Item 'E:\\1\\1\\1.txt').CreationTime=('" +
         (datetime.now() - timedelta(days=1)).strftime("%m %d %Y 0:1:1") + "')\"")
    call("powershell.exe -Command \"(Get-Item 'E:\\1\\1\\1.txt').LastWriteTime=('" +
         (datetime.now() - timedelta(days=1)).strftime("%m %d %Y 0:2:54") + "')\"")
    call("powershell.exe -Command \"(Get-Item 'E:\\1\\1\\1.txt').LastAccessTime=('" +
         (datetime.now() - timedelta(days=1)).strftime("%m %d %Y 0:1:1") + "')\"")


@dp.callback_query_handler(lambda c: c.data == "destroy:[W(q5?,?twR")
async def cq(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if check(callback_query.message):
        await bot.send_message(callback_query.from_user.id, "destroy - start")
        destroy()
        await bot.send_message(callback_query.from_user.id, "destroy - done")


@dp.callback_query_handler(lambda c: c.data == "restore_l(vG*zi9Iar")
async def cq(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if check(callback_query.message):
        await bot.send_message(callback_query.from_user.id, "restore - start")
        restore()
        await bot.send_message(callback_query.from_user.id, "restore - done")


@dp.message_handler(commands=["?"])
async def alive(message: Message):
    if check(message):
        await message.answer("y")


@dp.message_handler(commands=["!"])
async def print_inline_kb(message: Message):
    if check(message):
        inline_btn1 = InlineKeyboardButton("destroy", callback_data="destroy:[W(q5?,?twR")
        inline_btn2 = InlineKeyboardButton("restore", callback_data="restore_l(vG*zi9Iar")
        inline_kb = InlineKeyboardMarkup().add(inline_btn1)
        inline_kb.add(inline_btn2)
        await message.answer("Activities:", reply_markup=inline_kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
