import requests, eyed3, os
import config

def add_cover(url, mp3path):
    img = requests.get(url).content
    audiofile = eyed3.load(mp3path)
    if (audiofile.tag == None):
        audiofile.initTag()
    audiofile.tag.images.set(3, img, 'image/jpeg')
    audiofile.tag.save()

def save_cover(url):
    path = config.img_path + url.split('/')[-1]
    img = requests.get(url).content
    with open(path, 'wb') as f:
        f.write(img)
        f.close()

if __name__ == '__main__':
    url = 'http://i1.hdslb.com/bfs/archive/6765c058635e5c8ad920b655961ffa36e0b55038.jpg'
    try:
        if not os.path.exists(config.img_path):
            os.mkdir(config.img_path)
        save_cover(url)
        print("保存成功")
    except:
            print('爬取失败')
