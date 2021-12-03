import requests, eyed3

def add_cover(url, mp3path):
    img = requests.get(url).content
    audiofile = eyed3.load(mp3path)
    if (audiofile.tag == None):
        audiofile.initTag()
    audiofile.tag.images.set(3, img, 'image/jpeg')
    audiofile.tag.save()

if __name__ == '__main__':
    url = 'http://i1.hdslb.com/bfs/archive/6765c058635e5c8ad920b655961ffa36e0b55038.jpg'