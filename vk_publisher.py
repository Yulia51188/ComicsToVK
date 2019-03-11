import requests
from dotenv import load_dotenv
import os


def get_response_from_vk(method_name, payload={}, 
                        vk_host='https://api.vk.com/method'):
    url = '{host}/{method}'.format(host=vk_host, method=method_name)
    print(url)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    if response.ok:
        return response.json()


def make_post_request_to_vk(url, payload):
    response = requests.post(url, files=payload)
    response.raise_for_status()
    if response.ok:
        return response.json()


def main():
    load_dotenv()
    access_token = os.getenv("ACCESS_TOKEN")
    vk_api_version = os.getenv("VERSION")
    vk_group_id = os.getenv("GROUP_ID")
    payload = {
        'access_token': access_token,
        'v': vk_api_version,  
        'group_id': vk_group_id, 
    }
    response_getwall = get_response_from_vk('photos.getWallUploadServer', payload=payload)
    #
    upload_url = response_getwall['response']['upload_url']
    print(upload_url)
    #
    image_file_descriptor = open('images/python_comics.png', 'rb')
    post_data = { 'photo': image_file_descriptor}
    response_upload_photo = make_post_request_to_vk(upload_url, payload=post_data)
    photo_server = response_upload_photo['server']
    photo_json = response_upload_photo['photo']
    photo_hash = response_upload_photo['hash']
    payload = {
        'access_token': access_token,
        'v': vk_api_version,  
        'server': photo_server,
        'photo': photo_json,
        'hash': photo_hash, 
    }
    url = '{host}/{method}'.format(host='https://api.vk.com/method', 
                                    method='photos.saveWallPhoto')
    response = requests.post(url, params=payload)
    print(response.json())


if __name__ == '__main__':
    main()
