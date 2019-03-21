import download_images
import requests
import random
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Get comics from xkcd.com.'
        'Use download_images.py to save file in the folder "images"'
        'if it is neccessary.'
    )
    parser.add_argument(
        '-n', '--number',
        default=None,
        type=int,
        help='If not specified then download random comics. If get "0" then'
        'download current comics. Else download comics with input number.',
    )
    return parser.parse_args()


def fetch_xkcd(host='http://xkcd.com', method='info.0.json', number=None):
    if not number is None:
        method_api = '{0}/{1}'.format(number, method)
    else:
        method_api = method        
    url = '{host}/{method}'.format(host=host, method=method_api)
    response = requests.get(url)
    response.raise_for_status()
    if response.ok:
        return response.json()


def download_random_comics(save_file=True):
    max_number = get_comics_count()
    random.seed()
    random_number = random.randint(1, max_number)
    comics_data = fetch_xkcd(number=random_number)
    saved_comics_data = comics_data
    if save_file:
        download_result = download_images.download_image(
            comics_data['img'], 
            'comics.png'
        )
        saved_comics_data['filename'] = download_result['filename']  
    return saved_comics_data


def get_comics_count():
    response = fetch_xkcd()
    return response['num']


def main():
    args = parse_arguments()
    if args.number is None:
        print(download_random_comics(save_file=False))
        exit()
    if args.number == 0:
        print(fetch_xkcd())
        exit()
    max_number = get_comics_count()
    if args.number > max_number:
        exit("The input number {num} is too large."
            "Max available comics number is {max}".format(
                num=args.number,
                max=max_number)
        )
    print(fetch_xkcd(number=args.number))   


if __name__ == '__main__':
    main()