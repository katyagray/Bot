import telebot
import pika


bot = telebot.TeleBot(token="1573888987:AAEPYhHamanSQ79-bGQf9aqhXlVXKnqTKa4")

with pika.BlockingConnection(pika.ConnectionParameters(host='26.137.8.172', port=5672)) as connection:
    channel = connection.channel()
    channel.queue_declare(queue="lectures", durable=True)
    connection.close()


@bot.message_handler(func=lambda m: m.text == "Де народ?")
def react(message):
    # text = str("message received from {}".format(message.from_user.username))
    text = "message received from " + message.from_user.username
    print(text)
    with pika.BlockingConnection(pika.ConnectionParameters(host='26.137.8.172', port=5672)) as connection:
        channel = connection.channel()
        channel.basic_publish(exchange='lectures',
                              routing_key='lectures',
                              properties=pika.BasicProperties(headers={'id': message.from_user.id, 'username':message.from_user.username}),
                              body=message.text)


bot.polling()
