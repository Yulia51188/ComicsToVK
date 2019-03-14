import requests
import os
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Download photos by url list'
    )
    parser.add_argument(
        'url_list',
        nargs='+',
        type=str,
        help='Image_url_list'
    )
    parser.add_argument(
        '-n', '--filename',
        type=str,
        default='image',
        help='Basename to files with download images'
    )    
    return parser.parse_args()


def save_image_as_file_in_folder(image, folder_name='images', 
                                image_filename='image.jpeg'):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    filename = os.path.join(folder_name, image_filename)
    with open(filename, 'wb') as file:
        file.write(image)	
    return filename


def get_file_extention(url, default_url_list=('jpg', 'jpeg', 'tif', 'pdf', 
                                            'png', 'bmp')):
    parts = url.split('.')
    if len(parts)>0 and parts[-1] in :
        return parts[-1]
    else:
        return 'jpeg'


def download_image(image_url, image_filename):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        if response.ok:
            save_image_as_file_in_folder(response.content, 
                image_filename=image_filename)
            msg = "Image is saved as {}".format(filename)
            return {'result': True, 'msg': msg, 'filename':filename_saved,}
    except requests.exceptions.HTTPError as error:
        msg = "Can't download image by url {0} with error: \n {1}".format(
                                                    image_url, error)
        return { 'result': False, 'msg': msg, 'filename':None, }

    
def download_images_by_urls(image_urls, image_filename_template='space'):
    for image_index, image_url in enumerate(image_urls, 1):
        ext = get_file_extention(image_url)
        image_filename = '{name}{number}.{extention}'.format(
            name=image_filename_template, 
            number=image_index,
            extention=ext
        )
        print(download_image(image_url, image_filename)['msg'])


def download_images_by_urls_and_names(image_urls):
    for image_index, image in enumerate(image_urls, 1):
        ext = get_file_extention(image['url'])
        image_filename = '{name}.{extention}'.format(
            name=image['name'],       
            extention=ext
        )
        print(download_image(image['url'], image_filename)['msg'])


def main():
    args = parse_arguments()
    download_images_by_urls(args.url_list, args.filename)


if __name__ == '__main__':
    main()