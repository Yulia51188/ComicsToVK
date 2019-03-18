# ComicsToVK
The script download comics from [xkcd](http://xkcd.com) and post it to the wall of the specified VK group. Finally downloaded file is removed after posting to the wall.

- The function `def post_photo_to_wall` can post any photo with text comment to the wall of VK group. 

- The script `fetch_xkcd.py` can get and download comics from [xkcd](http://xkcd.com). 

- If it is specified the comics png file can be saved with `def download_image()` from module `download_images.py`.

# How to install

Th file '.env' must include following data:
- VK access token as 'ACCESS_TOKEN'
- version of VK API as'VERSION'
- group id as 'GROUP_ID'

Python3 should be already installed. Then use pip3 (or pip) to install dependencies:
```bash
pip3 install -r requirements.txt
```
# How to launch
To post random comics to VK group wall do:
```bash
$ python3 vk_publisher.py 
Image is saved as images/comics.png
GET request to https://api.vk.com/method/photos.getWallUploadServer
Ключи getwall: dict_keys(['response'])
POST request to https://pu.vk.com/c845524/upload.php?act=do_add&mid=1949163&aid=-14&gid=179375383&hash=44a6010504830c1dbc85a7b79486d975&rhash=0e7b1a8504b4dc515e4fd07b29178491&swfupload=1&api=1&wallphoto=1
POST request to https://api.vk.com/method/photos.saveWallPhoto
POST request to https://api.vk.com/method/wall.post
The random comics №1174 is posted to the wall of group 179375383 with post id 8
File is removed: images/comics.png
```
To get data from [xkcd](http://xkcd.com) do:

```bash
$ python3 fetch_xkcd.py 
{'alt': "No, tell the park rangers to calm down, it's fine--I put a screen on the front. I just want to get the birds a little closer.", 'year': '2017', 'news': '', 'img': 'https://imgs.xkcd.com/comics/birdwatching.png', 'num': 1826, 'safe_title': 'Birdwatching', 'title': 'Birdwatching', 'month': '4', 'day': '19', 'link': '', 'transcript': ''}
```
You also can add argument `-n` (`--number`) to get data of the latest comics or by number. Use `--help` to get argument description.

# Project Goals

The code is written for educational purposes on online-course for web-developers dvmn.org.
