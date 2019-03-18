import requests
from dotenv import load_dotenv
import os
import fetch_xkcd
from download_images import delete_file_and_dir


def get_request_to_vk(method, payload={}, 
                        host='https://api.vk.com/method'):
    url = '{host}/{method}'.format(host=host, method=method)
    print('GET request to {url}'.format(url=url))
    response = requests.get(url, params=payload)
    response.raise_for_status()
    if response.ok:
        return response.json()


def make_post_request_to_vk(url=None, method=None, params={}, files = {}, host='https://api.vk.com/method'):
    if url is None:
        url = '{host}/{method}'.format(host=host, method=method)
    print('POST request to {url}'.format(url=url))
    response = requests.post(url, files=files, params=params)
    response.raise_for_status()
    if response.ok:
        return response.json()


def main():
    load_dotenv()
    access_token = os.getenv("ACCESS_TOKEN")
    vk_api_version = os.getenv("VERSION")
    vk_group_id = os.getenv("GROUP_ID")
    
    comics_photo = fetch_xkcd.download_random_comics()

    payload = {
        'access_token': access_token,
        'v': vk_api_version,  
        'group_id': vk_group_id, 
    }
    #Получение адреса сервера
    response_getwall = get_response_from_vk('photos.getWallUploadServer', payload=payload)
    #
    upload_url = response_getwall['response']['upload_url']
    #Формируем структуру данных с изображением
    image_file_descriptor = open(comics_photo['filename'], 'rb')
    post_data = { 'photo': image_file_descriptor}
    #Загружаем изображение на сервер
    response_upload_photo = make_post_request_to_vk(url=upload_url, files=post_data)
    #Разбираем данные из ответа сервера
    photo_server = response_upload_photo['server']
    photo_json = response_upload_photo['photo']
    photo_hash = response_upload_photo['hash']
    payload = {
        'access_token': access_token,
        'v': vk_api_version,  
        'server': photo_server,
        'photo': photo_json,
        'hash': photo_hash, 
        'group_id': vk_group_id,
    }
    #Загружаем изображение в альбом VK
    #url = '{host}/{method}'.format(host='https://api.vk.com/method', 
    #                                method='photos.saveWallPhoto')
    response_save_wall = make_post_request_to_vk(method='photos.saveWallPhoto', params=payload)
    print(response_save_wall)
    #Публикуем фото на стене группы
    owner_id = response_save_wall['response'][0]['owner_id']
    media_id = response_save_wall['response'][0]['id']
    attachments_temp = 'photo{owner_id}_{media_id}'
    payload = {
        'access_token': access_token,
        'v': vk_api_version,  
        'owner_id': '-{id}'.format(id=vk_group_id),
        'attachments': attachments_temp.format(owner_id=owner_id, 
                                                media_id=media_id),
        'from_group': 1,
        'message': comics_photo['alt']
    }
    
    #url = '{host}/{method}'.format(host='https://api.vk.com/method', 
    #                                method='wall.post')
    response_wallpost = make_post_request_to_vk(method='wall.post', params=payload)
    print(response_wallpost)


def main():
    load_dotenv()
    access_token = os.getenv("ACCESS_TOKEN")
    vk_api_version = os.getenv("VERSION")
    vk_group_id = os.getenv("GROUP_ID")
    comics_photo = fetch_xkcd.download_random_comics()
    if not publish_comics_to_wall(
        access_token, 
        vk_group_id, 
        vk_api_version, 
        comics_photo,
    ):
        exit("The random comics is download but can't be published to the wall")
    for item in delete_file_and_dir(comics_photo['filename'])['msg']:
        print(item)
    exit()

    
    

if __name__ == '__main__':
    main()
