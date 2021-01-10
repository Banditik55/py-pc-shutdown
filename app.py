# telegram bot
# pip3 install python-telegram-bot
# https://python-telegram-bot.org/
# https://github.com/python-telegram-bot/python-telegram-bot
# .env
# pip3 install -U python-dotenv
# https://pypi.org/project/python-dotenv/

from dotenv import load_dotenv
load_dotenv()
from subprocess import call
from time import sleep
from threading import Timer
from os import environ
from math import floor
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

updater = Updater(environ.get("TG_TOKEN"))
adminID = int(environ.get("ADMIN_ID"))
private_message = "Sorry, this is a private bot ¯\\_(ツ)_/¯"
timer = {
	"active": False,
	"sec": 0,
}

def is_admin(id):
	if id == adminID:
		return True
	return False

def start_hander(update: Update, context: CallbackContext) -> None:
	if not is_admin(update.effective_user.id):
		update.message.reply_text(private_message)
		return
	reply_markup=ReplyKeyboardMarkup(
		keyboard=[
			[KeyboardButton(text="+15 min"), KeyboardButton(text="+30 min"), KeyboardButton(text="+60 min")],
			[KeyboardButton(text="check"), KeyboardButton(text="delete")],
			[KeyboardButton(text="shutdown")],
		],
		resize_keyboard=True,
		one_time_keyboard = False,
	)
	update.message.reply_text(f"Welcome, {update.effective_user.first_name}", reply_markup=reply_markup)

def message_handler(update: Update, context: CallbackContext) -> None:
	if not is_admin(update.effective_user.id):
		update.message.reply_text(private_message)
		return
	msg = update.message.text
	if msg == "+15 min":
		timer["active"] = True
		timer["sec"] += (60 * 15)
		update.message.reply_text(update.message.text)
	elif msg == "+30 min":
		timer["active"] = True
		timer["sec"] += (60 * 30)
		update.message.reply_text(update.message.text)
	elif msg == "+60 min":
		timer["active"] = True
		timer["sec"] += (60 * 60)
		update.message.reply_text(update.message.text)
	elif msg == "check":
		if timer["active"] == False:
			update.message.reply_text("Timer is disabled")
			return
		left = str(floor(timer["sec"]/60)) + " min. (" + str(timer["sec"]) + " sec.)"
		update.message.reply_text(f"{left}")
	elif msg == "delete":
		if timer["active"] == False:
			update.message.reply_text("Timer is already disabled")
			return
		timer["active"] = False
		timer["sec"] = 0
		update.message.reply_text(update.message.text)
	elif msg == "shutdown":
		update.message.reply_text("shutdown")
		shutdown()
	else:
		update.message.reply_text("error 404")

def command_not_found(update: Update, context: CallbackContext) -> None:
	update.message.reply_text("error 404")

def send_message_to_admin(msg):
	updater.bot.send_message(adminID, msg)

def shutdown():
	return
	# subprocess.call(["shutdown", "/s", "/t", "3"])
	# subprocess.call(["sudo", "shutdown", "-h", "1"])

def notify():
	if (timer["active"] == True):
		if (timer["sec"] == 60):
			send_message_to_admin("1 min. left")
		elif (timer["sec"] == 300):
			send_message_to_admin("5 min. left")
		elif (timer["sec"] == 600):
			send_message_to_admin("10 min. left")

def update_timer():
	if timer["active"] == True:
		if timer["sec"] > 0:
			timer["sec"] -= 1
		elif timer["sec"] <= 0:
			timer["active"] = False
			timer["sec"] = 0
			shutdown()
		notify()

def interval():
	while True:
		update_timer()
		sleep(1)
t = Timer(0, interval)
t.start()

updater.dispatcher.add_handler(CommandHandler("start", start_hander))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.text & Filters.command, command_not_found))
updater.start_polling()
updater.idle()