from 	telegram.ext import Updater,CommandHandler	,MessageHandler,Filters	,InlineQueryHandler,ChosenInlineResultHandler,CallbackQueryHandler
import telegram
from telegram import InlineQueryResultArticle,InputTextMessageContent,InlineKeyboardButton,InlineKeyboardMarkup

import logging

from game import game


bot = telegram.Bot(token='599024129:AAH4rkk1PpIImUj9YVansGEHJVU65zTYbaI')

ch = list()

status = list()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)


def start(bot,update):
	bot.send_message(chat_id=update.message.chat_id,text="Deja vu")

def new_game(bot,update):
	if not update.message.chat_id in ch:
		game_new = game(update.message.chat_id)
		ch.append(update.message.chat_id)
		status.append(game_new)
	else:
		k = ch.index(update.message.chat_id)
		ch.pop(k)
		status.pop(k)
		game_new = game(update.message.chat_id)
		ch.append(update.message.chat_id)
		status.append(game_new)
	bot.send_message(chat_id=update.message.chat_id,text = "已創建賽局！")
	try:	
		bot.deleteMessage(chat_id=update.message.chat.id,message_id=update.message.message_id)
	except:
		return
		

def join_game(bot,update):
	reply=""
	if not update.message.chat_id in ch:
		 bot.send_message(chat_id=update.message.chat_id,text="沒有創建賽局：使用 /new")
	else:
		players=""
		reply = status[ch.index(update.message.chat_id)].join(update.message.from_user)
		for name in status[ch.index(update.message.chat_id)].players:
			players+=name.first_name + " " + name.last_name + "\n"

		a = InlineKeyboardButton(text = "剪刀✌️",callback_data="Scissors")
		b = InlineKeyboardButton(text = "石頭👊",callback_data="Rock")
		c = InlineKeyboardButton(text = "布🖐",callback_data="Paper")

		bot.send_message(chat_id=update.message.chat_id,text="玩家們：\n"+players+"\n點擊按鈕以猜拳",reply_to_message_id = update.message.message_id,reply_markup=InlineKeyboardMarkup([[a,b,c]]))

	if not reply == None:
		bot.send_message(chat_id=update.message.chat_id,text=reply)

	try:	
		bot.deleteMessage(chat_id=update.message.chat.id,message_id=update.message.message_id)
	except:
		return

def reply_to_keyboard(bot,update):
	result = update.callback_query.data
	have_game = False
	for q in status:
		for player in q.players:
			if update.callback_query.from_user == player:
				have_game = True
				if result =='Scissors':
					q.out[q.players.index(update.callback_query.from_user)] =1
				elif result =='Rock':
					q.out[q.players.index(update.callback_query.from_user)] =2
				elif result =='Paper':
					q.out[q.players.index(update.callback_query.from_user)] =3
				
	if have_game:
		bot.send_message(chat_id=update.callback_query.message.chat_id,text=update.callback_query.from_user.first_name + " "+update.callback_query.from_user.last_name+"  已選擇了世界的收束點")
	else:	
		bot.send_message(chat_id=update.message.chat_id,text="沒有加入賽局喔")

def end_game(bot,update): 
	have_game = False
	for now_game in status:
		if now_game.identity == update.message.chat_id:
			have_game = True
			game_end = True
			for player_out in now_game.out:
				if player_out == 0:
					game_end = False


			if game_end == True:
				reply = "賭徒選擇：\n"
				Rock = list()
				Paper = list()
				Scissors = list()
				for player in now_game.players:
					if now_game.out[now_game.players.index(player)] == 1:
						reply += player.first_name + " " + player.last_name +":剪刀✌️\n"
						Scissors.append(player)
					elif now_game.out[now_game.players.index(player)] == 2:
						reply += player.first_name + " " + player.last_name +":石頭👊\n"
						Rock.append(player)
					else:
						reply += player.first_name + " " + player.last_name +":布🖐\n"
						Paper.append(player)
				winner_and_loser = '\nWinners:'

				if len(Rock)>0 and len(Scissors)>0 and len(Paper)==0:
					for player in now_game.players:
						if now_game.out[now_game.players.index(player)] == 2:
							winner_and_loser += player.first_name +" "+player.last_name+",  "
					winner_and_loser+="\nLosers:"
					for player in now_game.players:
						if now_game.out[now_game.players.index(player)] == 1:
							winner_and_loser += player.first_name +" "+player.last_name+",  "


				if len(Rock)>0 and len(Paper)>0 and len(Scissors)==0:
					for player in now_game.players:
						if now_game.out[now_game.players.index(player)] == 3:
							winner_and_loser += player.first_name +" "+player.last_name+",  "
					winner_and_loser+="\nLosers:"
					for player in now_game.players:
						if now_game.out[now_game.players.index(player)] == 2:
							winner_and_loser += player.first_name +" "+player.last_name+",  "


				if len(Paper)>0 and len(Scissors)>0 and len(Rock)==0:
					for player in now_game.players:
						if now_game.out[now_game.players.index(player)] == 1:
							winner_and_loser += player.first_name +" "+player.last_name+",  "
					winner_and_loser+="\nLosers:"
					for player in now_game.players:
						if now_game.out[now_game.players.index(player)] == 3:
							winner_and_loser += player.first_name +" "+player.last_name+",  "
				
				if winner_and_loser == '\nWinners:':#no winner
					winner_and_loser = '\n沒有人輸的和平世界'


				bot.send_message(chat_id=update.message.chat_id,text="\n"+reply+winner_and_loser)
				ch.remove(now_game.identity)
				status.remove(now_game)
			else:#not ending
				reply = ''
				for player in now_game.players:
					if now_game.out[now_game.players.index(player)] == 0:
						reply += player.first_name +' '+ player.last_name +'\n'


				bot.send_message(chat_id=update.message.chat_id,text="\n以下為未選擇的玩家\n\n"+reply)
	if not have_game:
		bot.send_message(chat_id=update.message.chat_id,text="這群沒有賽局啦")
	try:	
		bot.deleteMessage(chat_id=update.message.chat.id,message_id=update.message.message_id)
	except:
		return

	'''	
				game_end = True
				for player_out in q.out:
					if player_out == 0:
						game_end = False

				if game_end == True:
					end_game(bot,update,game)
				#else:
	'''




updater = Updater(token='599024129:AAH4rkk1PpIImUj9YVansGEHJVU65zTYbaI')
dispatcher = updater.dispatcher

keyboard_chsd_handler = CallbackQueryHandler(reply_to_keyboard)
dispatcher.add_handler(keyboard_chsd_handler)

start_handler = CommandHandler('start',start)
dispatcher.add_handler(start_handler)

new_handler = CommandHandler('new',new_game)
dispatcher.add_handler(new_handler)

join_handler = CommandHandler('join',join_game)
dispatcher.add_handler(join_handler)

result_handler = CommandHandler('result',end_game)
dispatcher.add_handler(result_handler)

updater.start_polling()
