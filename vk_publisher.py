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


def get_server_upload_url(payload):
    response_getwall = get_request_to_vk('photos.getWallUploadServer', payload=payload)
    print('Ключи getwall: {}'.format(response_getwall.keys()))
    if (not 'response' in response_getwall.keys() or 
            not 'upload_url' in response_getwall['response'].keys()):
        return
    return response_getwall['response']['upload_url']


def upload_image_to_server(filename, upload_url):
    image_file_descriptor = open(filename, 'rb')
    post_data = { 'photo': image_file_descriptor}
    response_upload = make_post_request_to_vk(url=upload_url, files=post_data)
    if (not 'photo' in response_upload.keys() or 
        response_upload['photo'] is []):
        return
    return response_upload


def publish_comics_to_wall(access_token, vk_group_id, version, file_data):
    base_payload = {
        'access_token': access_token,
        'v': version,  
        'group_id': vk_group_id, 
    }
    upload_url = get_server_upload_url(base_payload)
    if upload_url is None:
        exit('Get server upload url failed')  
    #Формируем структуру данных с изображением
    image_server_data = upload_image_to_server(file_data['filename'], upload_url)
    if image_server_data is None:
        exit('Upload image to server failed')        
    #Разбираем данные из ответа сервера
    photo_server = image_server_data['server']
    photo_json = image_server_data['photo']
    photo_hash = image_server_data['hash']
    payload = {
        'access_token': access_token,
        'v': version,  
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
        'v': version,  
        'owner_id': '-{id}'.format(id=vk_group_id),
        'attachments': attachments_temp.format(owner_id=owner_id, 
                                                media_id=media_id),
        'from_group': 1,
        'message': file_data['alt']
    }
    
    #url = '{host}/{method}'.format(host='https://api.vk.com/method', 
    #                                method='wall.post')
    response_wallpost = make_post_request_to_vk(method='wall.post', params=payload)
    print(response_wallpost)
    return True


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
