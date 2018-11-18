from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import File
import boto3


def hello(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello {}'.format(update.message.from_user.first_name))


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Send me some sticker or pic!")


def on_message_sticker(bot, update):
    print("Got sticker")
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    sticker_id = update.message.sticker.file_id
    file = bot.get_file(sticker_id)
    print(file)
    file.download()
    print("Sticker successfully downloaded!")
    bot.sendMessage(chat_id=chat_id, text=get_sticker_options(sticker_id), reply_to_message_id=message_id)
    bot.sendMessage("Chat id = {}".format(chat_id))


def on_message_picture(bot, update):
    print("Got pic")
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    photo = update.message.photo
    photo_id = photo[len(photo)-1].file_id
    file = bot.get_file(photo_id)
    file.download()
    print("Photo successfully downloaded!")
    bot.sendMessage(chat_id=chat_id, text="Got pic with id{}".format(photo_id), reply_to_message_id=message_id)
    bot.send_photo(chat_id=chat_id, photo='https://cdn.cnn.com/cnnnext/dam/assets/181113054953-01-detective-pikachu-film-pokemon-grab-1113-exlarge-169.jpg')


def get_sticker_options(sticker_id):
    """
    Finds information about the input sticker.
    """
    message = "ID: {sticker_id}" \
              "".format(sticker_id=sticker_id)

    return message


updater = Updater(str(open("key.txt", 'r').readline()).replace("\n", ""))
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(CommandHandler('start', start))

dispatcher.add_handler(MessageHandler(Filters.photo, on_message_picture))
dispatcher.add_handler(MessageHandler(Filters.sticker, on_message_sticker))

updater.start_polling()
updater.idle()




