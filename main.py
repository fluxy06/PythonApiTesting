from unicodedata import category
import requests
from urllib3 import request

#Класс в котором метод для вывода отсортированной информации по запросу
class HelperRequests: #Т.к есть два частных случая, когда мы получаем и выводим несколько параметров и делаем поиск по нескольким параметрам
  #или одному, то пришлось метод как бы разделить на двое, для того что бы метод корректно обрабатывал ситуации когда на вход
  #поается только id
    # Get метод для получения информации о питомце
    def GetInfo(infoGet):
      if infoGet.status_code == 200:
        info = infoGet.json()
        # Проверяем, является ли info списком или одним объектом
        if isinstance(info, list):
          for inf in info:
            HelperRequests._print_pet_info(inf)
        else:
          HelperRequests._print_pet_info(info)
      else:
        print("Ошибка при выполнении get запроса: " + str(infoGet.status_code))
    @staticmethod
    def _print_pet_info(inf):
      id = inf.get('id')
      pet_name = inf.get('name', 'Нет имени')
      pet_status = inf.get('status', 'Нет статуса')
      category = inf.get('category', {})
      category_name = category.get('name', 'Нет названия категории')
      print(f"ID {id}||||Статус: {pet_status}||||Категория животных: {category_name}||||Имя: {pet_name}\n")


# Основная ссылка
base_url = 'https://petstore.swagger.io/v2'

#region Задание с пользователями(USER): GER, POST, DELETE, PUT
#region Создание двух новых пользователей при помощи POST /user/createWithList
keyForPostCreateUsesr = "/user/createWithList" #Ключ ссылки для создания нового пользователя
firstUser = {
  "id": 0,
  "username": "Никита",
  "firstName": "Никита",
  "lastName": "Сорокин",
  "email": "ni.sorokin@agatgroup.com",
  "password": "qwerty123",
  "phone": "79082342635",
  "userStatus": 1
} #заголовки для создания пользователя Никита Сорокин
secondUser = {
  "id": 1,
  "username": "Антон",
  "firstName": "Антон",
  "lastName": "Тереня",
  "email": "an.terenya@agatgroup.com",
  "password": "zxcvbn123",
  "phone": "79200624695",
  "userStatus": 500
}
newUser1 = requests.post(base_url + keyForPostCreateUsesr, json=[firstUser, secondUser])
#print(newUser1.status_code) результат запроса Post, созданы 2 новых пользователя
#endregion
#region Получение информации по второму созданому пользователю secondUser, name = 'Антон'
nameUser = "Антон"
keyForGetInfoOfSecondUser = f"/user/{nameUser}"
infoOfUser = requests.get(base_url + keyForGetInfoOfSecondUser)
#print(infoOfUser.text)Проверил , выводит информацию о втором созданном пользователе
#endregion
#region Изменение любого необязательного парамера у первого пользователя name = 'Никита'
nameUserForPut = "Никита"
keyForPutMethod = f"/user/{nameUserForPut}"
body = {
  "id": 871248712471420,
  "password": "1234567890",
  "userStatus": 404
} #тело для изменения необязательных параметров
newFirstUser = requests.put(base_url + keyForPutMethod, json=body)
#print(newFirstUser.text) Результат изменения данных.
#endregion
#region Удаление двух пользователей при помощи запроса
username = 'Никита'
username2 = 'Антон'
url_for_delete_user = f'/user/{username}'
url_for_delete_user2 = f'/user/{username2}'
fullUrl_for_delete_users = base_url + url_for_delete_user
fullUrl_for_delete_users2 = base_url + url_for_delete_user2
deleteFirstUser = requests.delete(fullUrl_for_delete_users);
deleteSecondUser = requests.delete(fullUrl_for_delete_users2)
#print(deleteFirstUser.json()) #Успешно выполняется код 200
#print(deleteSecondUser.json()) #Успешно выполняется код 200

#endregion
#endregion
#region Задание с питомцами: GET, POST, DELETE, PUT

#region Ключи ссылки
petId = 123 #параметр для поиска по id, get запрос через id который))
keyGetPetByID = f"/pet/{petId}"
keyPostPet = "/pet"
keyGetPetByStatus = "/pet/findByStatus"
keyPostChangeInformationPet = f"/pet/{petId}"
#endregion
#region Данные для создания двух питомцев через POST запрос, также параметры для изменения информации о них, тоже тут)
#создал 2 питомцев
dataForCreateFirstPet = {
  "id": 123,
  "category": {
    "id": 1,
    "name": "Dog"
  },
  "name": "Малыш",
  "status": "available"
}
dataForCreateSecondPet = {
  "id": 5,
  "category": {
    "id": 4,
    "name": "Кот"
  },
  "name": "Барсик",
  "status": "available"
}
#данные для изменения информации о двух питомцах
dataForChangeInfoFirstPET = {
  "id": petId,
  "name": "Стрелка",
  "status": "pending"
}
#endregion
#region Отправка POST-запросов
response1 = requests.post(base_url + keyPostPet, json=dataForCreateFirstPet) #Создал питомца №1 id = 123, category_id = 1, category_name = Dog, name = "Малыш", status = "available"
response2 = requests.post(base_url + keyPostPet, json=dataForCreateSecondPet) #Создал питомца №2 id = 5, category_id = 4, category_name = Кот, name = "Барсик", status = "available"
responseForChangePetDog = requests.post(base_url + keyPostChangeInformationPet, data=dataForChangeInfoFirstPET) #Изменение имени Кота 'Бариск' с id = 5 на name = 'Тюльпан' , status = 'sold'

#endregion
#region Параметры для GET запросов
paramsForFindByStatus = {
  "status": 'sold'
}
#endregion
#region Get запросы
infoPetsByStatusSOLD = requests.get(base_url + keyGetPetByStatus, params=paramsForFindByStatus)
infoPetsById = requests.get(base_url + keyGetPetByID)
#endregion
#region Информация для DELETE запроса по питомцам
headers = {
  "api_key": "special-key"
}
#endregion
#region Вызываем методы класса для проверки корректной работы запросов
#HelperRequests.GetInfo(infoPetsByStatusSOLD) #Поиск по статусу "sold"
#HelperRequests.GetInfo(infoPetsById) #Поиск по id = 123 для первого питомца по заданию
#endregion
#region DELETE запросы
testForDebuggerCat = requests.delete(base_url + "/pet/5", headers=headers) #удаляем кота с id = 5, status_code = 200
testForDebuggerDog = requests.delete(base_url + "/pet/123", headers=headers) #удаляем собаку с id = 123 , status_code = 200
#print(testForDebuggerCat.status_code, "\n", testForDebuggerDog.status_code)
#endregion
#region Данные для изменения при помощи PUT запроса
body = {
  "id": 5,
  "category": {
    "id": 10,
    "name": "Обезьяна"
  },
  "name": "Капуцин",
  "tags": [
    {
      "id": 24,
      "name": "Бублик"
    }
  ],
  "status": "available"
}

full_url_for_put = base_url + keyPostPet

testPutRequest = requests.put(full_url_for_put, json=body)#передали параметры для изменения информации о питомце с id = 5
#print(testPutRequest.status_code)#получили ответ 200
#endregion

#endregion
