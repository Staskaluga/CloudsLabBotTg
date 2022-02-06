from datetime import date
import telebot 
import gspread

bot_token = 'some_token'
googlesheet_id = 'some_spreadsheet_id'
bot = telebot.TeleBot(token)
gc = gspread.service_account()

# приветствуем пользователя и говорим что умеем..
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я буду записивать ваши расходы в таблицу. Введите расход через дефис в виде [КАТЕГОРИЯ-ЦЕНА]:")
    

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    try:
        today = date.today().strftime("%d.%m.%Y")
        
        #  разделяем сообщение на 2 части, категория и цена
        category, price = message.text.split("-", 1)
        text_message = f'На {today} в таблицу расходов добавлена запись: категория {category}, сумма {price} сум'
        bot.send_message(message.chat.id, text_message)
        
        # открываем Google таблицу и добавляем запись
        sh = gc.open_by_key(googlesheet_id)
        sh.sheet1.append_row([today, category, price])
    except:
        # если пользователь ввел неправильную информацию, оповещаем его и просим вводить повторно
        bot.send_message(message.chat.id, 'ОШИБКА! Неправильный формат данных!')
        
    bot.send_message(message.chat.id, 'Введите расход через дефис в виде [КАТЕГОРИЯ-ЦЕНА]:')
    
if __name__ == '__main__':
     bot.polling(none_stop=True)
