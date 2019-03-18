import download_images
import requests
import random


def fetch_xkcd(host='http://xkcd.com', method='info.0.json', number=None):
    method_api = method
    if not number is None:
        method_api = '{0}/{1}'.format(number, method)
    url = '{host}/{method}'.format(host=host, method=method_api)
    response = requests.get(url)
    response.raise_for_status()
    if response.ok:
        return response.json()


def download_random_comics():
    max_number = get_comics_count()
    random.seed()
    random_number = random.randint(1, max_number)
    comics_data = fetch_xkcd(number=random_number)
    download_result = download_images.download_image(comics_data['img'], 'comics.png')
    print(download_result['msg'])
    saved_comics_data = comics_data
    saved_comics_data['filename'] = download_result['filename']
    return saved_comics_data


def get_comics_count():
    response = fetch_xkcd()
    return response['num']


def main():
    download_random_comics()
    # current_comics = fetch_xkcd()
    # current_comics_url = current_comics['img']
    # print(current_comics_url)
    
    # python_comics = fetch_xkcd(number=353)
    # python_comics_url = python_comics['img']
    # print(python_comics_url)
    #print(download_images.download_image(comics_url, 'python_comics.png'))
    


if __name__ == '__main__':
    main()