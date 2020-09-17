from subprocess import call
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from time import sleep
import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


def check(message: Message):
    if message.chat.username in config.ADMIN_USERNAME and message.chat.id in config.ADMIN_CHAT_ID:
        return True
    else:
        return False


def run(cmd, args):
    if cmd == "cmd":
        return call("PsExec64.exe \\\\" + config.EXEC_SERVER + " -nobanner -h -u " + config.EXEC_USERNAME + " -p " +
                    config.EXEC_PASSWD + " cmd.exe /c \"" + args + "\" >nul 2>&1")
    elif cmd == "ps" or cmd == "powershell":
        return call("PsExec64.exe \\\\" + config.EXEC_SERVER + " -nobanner -h -u " + config.EXEC_USERNAME + " -p " +
                    config.EXEC_PASSWD + " powershell.exe -Command \"" + args + "\"")
    else:
        return 1


def destroy():
    now = datetime.now()

    run("cmd", "ren " + config.BAK_1 + " " + now.strftime("%Y_%m_%d_000101_6441143.bak") +
        " && ren " + config.BAK_2 + " " + (now - timedelta(days=1)).strftime("%Y_%m_%d_000101_8651948.bak") +
        " && ren " + config.BAK_3 + " " + (now - timedelta(days=2)).strftime("%Y_%m_%d_000101_2255729.bak"))
    run("ps",
        "(Get-Item \"" + config.BAK_1 + "\").CreationTime=('" + now.strftime("%m %d %Y 0:1:1") + "') ; "
        "(Get-Item \"" + config.BAK_1 + "\").LastWriteTime=('" + now.strftime("%m %d %Y 0:2:54") + "') ; "
        "(Get-Item \"" + config.BAK_1 + "\").LastAccessTime=('" + now.strftime("%m %d %Y 0:1:1") + "')")
    run("ps",
        "(Get-Item \"" + config.BAK_2 + "\").CreationTime=('" + (now - timedelta(days=1)).strftime("%m %d %Y 0:1:1") + 
        "') ; "
        "(Get-Item \"" + config.BAK_2 + "\").LastWriteTime=('" + (now - timedelta(days=1)).strftime("%m %d %Y 0:1:57") + 
        "') ; "
        "(Get-Item \"" + config.BAK_2 + "\").LastAccessTime=('" + (now - timedelta(days=1)).strftime("%m %d %Y 0:1:1") + 
        "')")
    run("ps",
        "(Get-Item \"" + config.BAK_3 + "\").CreationTime=('" + (now - timedelta(days=2)).strftime("%m %d %Y 0:1:1") + 
        "') ; "
        "(Get-Item \"" + config.BAK_3 + "\").LastWriteTime=('" + (now - timedelta(days=2)).strftime("%m %d %Y 0:2:44") + 
        "') ; "
        "(Get-Item \"" + config.BAK_3 + "\").LastAccessTime=('" + (now - timedelta(days=2)).strftime("%m %d %Y 0:1:1") + 
        "')")

    run("cmd", "sc config \"TapiSrv\" start=auto")
    run("cmd", "sc start \"TapiSrv\"")
    
    run("cmd", config.DISKPART_SCR_DESTROY + " && diskpart.exe /s " + config.DISKPART_SCR_PATH + " >nul && del " +
        config.DISKPART_SCR_PATH)

    run("cmd", "netsh interface set interface name=\"13\" admin=DISABLED")


def restore():
    run("cmd", "netsh interface set interface name=\"13\" admin=ENABLED")

    run("cmd", config.DISKPART_SCR_RESTORE + " && diskpart.exe /s " + config.DISKPART_SCR_PATH + " >nul && del " +
        config.DISKPART_SCR_PATH)
    
    run("cmd", "sc config \"TapiSrv\" start=demand")
    run("cmd", "sc stop \"TapiSrv\"")

    call("PsExec64.exe \\\\" + config.EXEC_SERVER + " -nobanner -h -u " + config.EXEC_USERNAME + " -p "
         + config.EXEC_PASSWD + " -c restore_names.bat cmd.exe /c restore_names.bat >nul 2>&1")


def reload(service):
    run("cmd", "sc stop \"" + service + "\"")
    sleep(3)
    run("cmd", "sc start \"" + service + "\"")


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


@dp.callback_query_handler(lambda c: c.data == "reload_1c_srv_fewod")
async def cq(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if check(callback_query.message):
        await bot.send_message(callback_query.from_user.id, "reload 1c srv- start")
        reload("1C:Enterprise 8.3 Server Agent")
        await bot.send_message(callback_query.from_user.id, "reload 1c srv - done")


@dp.callback_query_handler(lambda c: c.data == "reload_hasp_d3fj201hc")
async def cq(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if check(callback_query.message):
        await bot.send_message(callback_query.from_user.id, "reload hasp - start")
        reload("HASP Loader")
        await bot.send_message(callback_query.from_user.id, "reload hasp - done")


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


@dp.message_handler(commands=["reload"])
async def reload_inline_kb(message: Message):
    if check(message):
        inline_btn1 = InlineKeyboardButton("1c srv", callback_data="reload_1c_srv_fewod")
        inline_btn2 = InlineKeyboardButton("hasp", callback_data="reload_hasp_d3fj201hc")
        inline_kb = InlineKeyboardMarkup().add(inline_btn1)
        inline_kb.add(inline_btn2)
        await message.answer("Services:", reply_markup=inline_kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
