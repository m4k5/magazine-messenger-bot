from django.shortcuts import render
from pymessenger.bot import Bot
from os import environ
from .models import Subscriber

# You have to specify them in environmental variables
ACCESS_TOKEN = environ.get('ACCESS_TOKEN')
VERIFY_TOKEN = environ.get('VERIFY_TOKEN')
bot = Bot(ACCESS_TOKEN)


# Create your views here.
def new_message_received(request):
    if request.method == 'GET':
        token_sent = request.GET.get('hub.verify_token')
        if token_sent == VERIFY_TOKEN:
            return request.GET.get('hub.challange')
        return 'Invalid verification token'
    else:
        for event in request.POST.get('entry'):
            messaging = event.get('messaging')
            for message in messaging:
                if message.get('message'):
                    user = message['sender']
                    bot.send_action(user['id'], 'mark_seen')
                    bot.send_action(user['id'], 'typing_on')
                    process_message(user, message['message'])
                    bot.send_action(user['id'], 'typing_off')


def process_message(user, msg):
    if user['id'] not in Subscriber.objects.all():
        if msg.get('quick_reply', {}).get('payload') == 'start_subscription':
            add_subscriber(user)
            bot.send_message(user['id'],
                             'Gotowe! Teraz będziesz otrzymywać powiadomienia o nowych wydaniach magazynu Politechnik Junior.')
        else:
            payload = {'receipient': user['id'],
                       'messaging_type': 'RESPONSE',
                       'message': {'text': 'Chcesz zapisać się na powiadomienia o nowych wydaniach?',
                                   'quick_replies': ({'content_type': 'text',
                                                      'title': 'Oczywiście!',
                                                      'payload': 'start_subscription'})}}
            bot.send_raw(payload)
    else:
        if msg.get('quick_reply', {}).get('payload') == 'stop_subscription':
            remove_subscriber(user)
            bot.send_message(user['id'], 'Już nie będziesz otrzymywać powiadomień :(. Do zobaczenia!')
        else:
            payload = {'receipient': user['id'],
                       'messaging_type': 'RESPONSE',
                       'message': {'text': 'Jesteś zapisany na otrzymywanie notyfikacji o nowych wydaniach,',
                                   'quick_replies': ({'content_type': 'text',
                                                      'title': 'Wypiszcie mnie :(',
                                                      'payload': 'stop_subscription'})}}
            bot.send_raw(payload)


def add_subscriber(user):
    new_subscriber = Subscriber()
    new_subscriber.id = user['id']
    new_subscriber.name = user['name']
    new_subscriber.save()
    # new_subscriber.profile_pic = user['profile_pic']


def remove_subscriber(user):
    subscriber = Subscriber.objects.get(id=user['id'])
    subscriber.is_subscribed = False
    subscriber.save()
