# реализация VKAPI
import vk
# url-запросы
import urllib.request
# парсинг url
import urllib.parse
# для парсинга объекта из JSON-представления
import json
# для дампа переменных
from pprint import pprint
# url-запросы
import requests
# парсинг аргументов
import argparse
# системные средства
import sys


# неиспользуемые библиотеки, но которые вам могут понадобится при дальнейшем развитии скрипта:
# может понадобится для ожидания
#from time import sleep
# кодирование по base64, можно использовать для изображений
#import base64


'''

документацию по работе в командой строке –  http://help.ubuntu.ru/wiki/командная_строка

Использование:

Отправка со стандартными параметрами (задаются ниже в createParser)
$ python3 send_message_img.py

Установить свои параметры, заменить стандартные
$ python3 send_message_img.py -mes Привет -uid 12345 -p /path/to/photo.jpg -t access_token

Можно передать путь до картинки глобальный или относительный:

photo.jpg - относительный
/home/photo.jpg - глобальный

В директории рядом может лежать картинка photo.jpg, однако,
можно отправить любую картинку из любой папки, указав адрес картинки в параметре -p

Этот скрипт можно добавить в cron, т.е. он может выслать сообщение по расписанию,
работа с кроном – help.ubuntu.ru/wiki/cron, либо вызывать из командной строки. 

Отправка разных картинок, разных сообщений разным людям: 

python3 send_message_img.py -mes 'Текст первого сообщения' -uid ID_ПОЛУЧАЕЛЯ_1 -t ВАШ_ТОКЕН -p /путь/до/картинки1.jpg 
python3 send_message_img.py -mes 'Текст второго сообщения' -uid ID_ПОЛУЧАЕЛЯ_2 -t ВАШ_ТОКЕН -p /путь/до/картинки2.jpg 
python3 send_message_img.py -mes 'Текст третьего сообщения' -uid ID_ПОЛУЧАЕЛЯ_3 -t ВАШ_ТОКЕН -p /путь/до/картинки3.jpg

'''

 # парсер аргументов запуска
def createParser ():
	parser = argparse.ArgumentParser()
	parser.add_argument ('-uid', '--user_id', default=0)
	parser.add_argument ('-mes', '--message', default='')
	parser.add_argument ('-t', '--token', default='')
	parser.add_argument ('-p', '--photo', default='')
	return parser

 # парсим аргументы запуска
if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args(sys.argv[1:])

	if namespace.user_id == 0:
		namespace.user_id = input ("введите id получателя:")
	if namespace.message == '':
		namespace.message = input ("введите сообщение:")
	if namespace.token == '':
		namespace.token = input ("введите токе:")
	if namespace.photo == '':
		namespace.photo = input ("введите путь до изображения:")

	print ("Указан id vk получателя: {}".format (namespace.user_id) )
	print ("Указано сообщение: {}".format (namespace.message) )
	print ("Указано токен: {}".format (namespace.token) )
	print ("Указан путь до картинки: {}".format (namespace.photo) )

#sys.exit()

# авторзуемся по токену
vkapi = vk.API(access_token=namespace.token)
# получаем сервер для загрузки
upload_info = vkapi.photos.getMessagesUploadServer()

# для вывода информации раскомментируйте
#print (upload_info)
#print (upload_info['upload_url'])

# загружаем картинку в вк
res = requests.post(upload_info['upload_url'], files={'photo': open(namespace.photo,"rb")})
res = res.json()
#pprint (res)

# сохраняем картинку в вк
photo = vkapi.photos.saveMessagesPhoto(
	server = res['server'],
	photo = res['photo'],
	hash = res['hash']
)

photo = photo[0]
#pprint (photo)

# отправляем сообщение с прикреплением картинки
vkapi.messages.send(
	message = namespace.message,
	user_id = namespace.user_id,
	attachment = 'photo' + str(photo['owner_id']) + '_' + str(photo['id'])
)