import requests
from dotenv import load_dotenv
import os
import fetch_xkcd
from download_images import delete_file_and_dir


def get_request_to_vk(method, payload={}, 
        host='https://api.vk.com/method'):
    url = '{host}/{method}'.format(host=host, method=method)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    if response.ok:
        return response.json()


def make_post_request_to_vk(input_url=None, method=None, params={}, 
        files = {}, host='https://api.vk.com/method'):
    if not input_url:
        url = '{host}/{method}'.format(host=host, method=method)
    else:
        url = input_url
    response = requests.post(url, files=files, params=params)
    response.raise_for_status()
    if response.ok:
        return response.json()


def get_server_upload_url(payload):
    response_getwall = get_request_to_vk(
        'photos.getWallUploadServer', 
        payload=payload
    )
    if (not 'response' in response_getwall.keys() or 
            not 'upload_url' in response_getwall['response'].keys()):
        return
    return response_getwall['response']['upload_url']


def upload_image_to_server(filename, upload_url):
    image_file_descriptor = open(filename, 'rb')
    post_data = { 'photo': image_file_descriptor}
    response_upload = make_post_request_to_vk(
        input_url=upload_url, 
        files=post_data
    )
    if (not 'photo' in response_upload.keys() or 
            response_upload['photo'] is []):
        return
    return response_upload


def add_image_to_album(image_server_data, base_payload):
    photo_server = 
    photo_json = 
    photo_hash = 
    payload = {
        **base_payload,
        'server': image_server_data['server'],
        'photo': image_server_data['photo'],
        'hash': image_server_data['hash'],      
    }
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
    attachments_temp = 'photo{owner_id}_{media_id}'
    attachments = attachments_temp.format(
        owner_id=owner_id, 
        media_id=media_id,
    )    
    payload = {
        **base_payload,
        'owner_id':'-{id}'.format(id=base_payload['group_id']),
        'attachments':attachments,
        'from_group':1,
        'message':comment,        
    }
    response_wallpost = make_post_request_to_vk(
        method='wall.post', 
        params=payload
    )    
    if (not 'response' in response_wallpost.keys() or
            not 'post_id' in response_wallpost['response'].keys()):
        return
    return response_wallpost['response']['post_id']


class VKWallPostError(Exception):
    pass


def post_photo_to_wall(access_token, vk_group_id, version, filepath, comment):
    base_payload = {
        'access_token': access_token,
        'v': version,  
        'group_id': vk_group_id, 
    }
    upload_url = get_server_upload_url(base_payload)
    if not upload_url:
        raise VKWallPostError('Getting server upload url failed') 
    image_server_data = upload_image_to_server(
        filepath, 
        upload_url
    )
    if not image_server_data:
        raise VKWallPostError('Upload image to server failed')     
    image_album_data = add_image_to_album(image_server_data, base_payload)
    if not image_album_data:
        raise VKWallPostError('Adding image to server failed')  
    post_id = post_image_to_wall(
        image_album_data, 
        base_payload, 
        comment=comment
    )
    if not post_id:
        raise VKWallPostError('Posting image to the wall failed.')         
    return post_id

def main():
    load_dotenv()
    access_token = os.getenv("ACCESS_TOKEN")
    vk_api_version = os.getenv("VERSION")
    vk_group_id = os.getenv("GROUP_ID")
    comics_photo = fetch_xkcd.download_random_comics()
    try:
        post_id = post_photo_to_wall(
            access_token, 
            vk_group_id, 
            vk_api_version, 
            comics_photo['filename'],
            '{0}\n{1}'.format(comics_photo['title'].upper(),comics_photo['alt']),
        )   
        print('The random comics №{number} is posted to the wall of group '
            '{group_id} with post id {post_id}'.format(
            number=comics_photo['num'],
            group_id=vk_group_id,
            post_id=post_id
        ))
    except VKWallPostError as error:
        exit(error)
    finally:
        if not delete_file_and_dir(comics_photo['filename'])['result']:
            exit("Attention! Downloaded file with image can't be deleted")
    

if __name__ == '__main__':
    main()
