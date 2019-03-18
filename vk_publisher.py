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


def add_image_to_album(image_server_data, base_payload):
    photo_server = image_server_data['server']
    photo_json = image_server_data['photo']
    photo_hash = image_server_data['hash']
    payload = base_payload
    payload['server'] = photo_server
    payload['photo'] = photo_json
    payload['hash'] = photo_hash 
    response_add_to_album = make_post_request_to_vk(
        method='photos.saveWallPhoto', 
        params=payload
    )
    if (not 'response' in response_add_to_album.keys() or
            not 'id' in response_add_to_album['response'][0]):
        return
    return response_add_to_album


def post_image_to_wall(image_album_data, base_payload, comment=''):
    owner_id = image_album_data['response'][0]['owner_id']
    media_id = image_album_data['response'][0]['id']
    payload = base_payload
    payload['owner_id'] = '-{id}'.format(id=base_payload['group_id'])
    attachments_temp = 'photo{owner_id}_{media_id}'
    attachments = attachments_temp.format(owner_id=owner_id, media_id=media_id)    
    payload['attachments'] = attachments
    payload['from_group'] = 1
    payload['message'] = comment
    response_wallpost = make_post_request_to_vk(method='wall.post', 
                                                params=payload)    
    if (not 'response' in response_wallpost.keys() or
            not 'post_id' in response_wallpost['response'].keys()):
        return
    return response_wallpost['response']['post_id']


def post_photo_to_wall(access_token, vk_group_id, version, file_data):
    base_payload = {
        'access_token': access_token,
        'v': version,  
        'group_id': vk_group_id, 
    }
    upload_url = get_server_upload_url(base_payload)
    if upload_url is None:
        exit('Get server upload url failed')  
    image_server_data = upload_image_to_server(file_data['filename'], upload_url)
    if image_server_data is None:
        exit('Upload image to server failed')        
    image_album_data = add_image_to_album(image_server_data, base_payload)
    if image_album_data is None:
        exit('Adding image to server failed')      
    return post_image_to_wall(image_album_data, base_payload, comment=file_data['alt'])




def main():
    load_dotenv()
    access_token = os.getenv("ACCESS_TOKEN")
    vk_api_version = os.getenv("VERSION")
    vk_group_id = os.getenv("GROUP_ID")
    comics_photo = fetch_xkcd.download_random_comics()
    post_id = post_photo_to_wall(
        access_token, 
        vk_group_id, 
        vk_api_version, 
        comics_photo
    )
    if post_id is None:
        exit("The comics can't be posted to the wall")
    print('The random comics #{number} is posted to the wall of group \
        {group_id} with post id {post_id}'.format(
            number=comics_photo['num'],
            group_id=vk_group_id,
            post_id=post_id
        ))
    for item in delete_file_and_dir(comics_photo['filename'])['msg']:
        print(item)
    exit()

    
    

if __name__ == '__main__':
    main()
