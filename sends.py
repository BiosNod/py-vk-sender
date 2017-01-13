import vk
import urllib.request
import urllib.parse
import json
from pprint import pprint
import requests
import argparse
import sys

def createParser ():
	parser = argparse.ArgumentParser()
	parser.add_argument ('-uid', '--user_id', default=0)
	parser.add_argument ('-mes', '--message', default='')
	parser.add_argument ('-t', '--token', default='')
	parser.add_argument ('-p', '--photo', default='')
	return parser

if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args(sys.argv[1:])

	if namespace.user_id == 0:
		namespace.user_id = input ("введите id получателей через запятую:")
	if namespace.message == '':
		namespace.message = input ("введите сообщение:")
	if namespace.token == '':
		namespace.token = input ("введите токе:")
	if namespace.photo == '':
		namespace.photo = input ("введите путь до изображения:")

	print ("Указан id vk получателя/ей: {}".format (namespace.user_id) )
	print ("Указано сообщение: {}".format (namespace.message) )
	print ("Указан токен: {}".format (namespace.token) )
	print ("Указан путь до картинки: {}".format (namespace.photo) )

users_ids = namespace.user_id.split(',')

vkapi = vk.API(access_token=namespace.token)
upload_info = vkapi.photos.getMessagesUploadServer()

res = requests.post(upload_info['upload_url'], files={'photo': open(namespace.photo,"rb")})
res = res.json()

photo = vkapi.photos.saveMessagesPhoto(
	server = res['server'],
	photo = res['photo'],
	hash = res['hash']
)

photo = photo[0]

for user_id in users_ids:
	vkapi.messages.send(
		message = namespace.message,
		user_id = user_id,
		attachment = 'photo' + str(photo['owner_id']) + '_' + str(photo['id'])
	)