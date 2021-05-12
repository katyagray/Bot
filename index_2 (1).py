import telegram
from telegram.ext import Updater
import pika


u = Updater('1717085872:AAH3pCMjOp1bS9eEpl9urGi4ph_V7gBEVmw', use_context=True)
j = u.job_queue


def callback(context):
    loop = True
    with pika.BlockingConnection(pika.ConnectionParameters(host='26.137.8.172', port=5672)) as connection:
        channel = connection.channel()

        while loop:
            method, properties, body = channel.basic_get(queue='lectures', auto_ack=True)
            if properties is not None:
                username = properties.headers['username']
                message = body.decode('utf-8')
                text = 'Викладач {} почав віддалену пару і написав:\n{}'.format(username, message)

                context.bot.send_message(chat_id=context.job.context,
                                         text=text)
            else:
                loop = False


def start(update, context) -> None:
    j.run_repeating(callback, interval=15, first=15, context=update.message.chat_id)


u.dispatcher.add_handler(telegram.ext.CommandHandler('start', start))

u.start_polling()
