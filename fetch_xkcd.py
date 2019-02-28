import download_images


def main():
    xkcd_url = 'http://xkcd.com/{number}/info.0.json'.format(number=353)
    comics_url = 'https://imgs.xkcd.com/comics/python.png'
    print(download_images.download_image(comics_url, 'python_comics.png'))


if __name__ == '__main__':
    main()