import os
import imageio
def check_folder():
    if not os.path.exists('./bilibili_music') == True:
        os.makedirs('./bilibili_music')
    if not os.path.exists('./img') == True:
        os.makedirs('./img')
    if not os.path.exists('./bilibili_video') == True:
        os.makedirs('./bilibili_video')    
    return

if __name__ == '__main__':
    check_folder()
    imageio.plugins.ffmpeg.download()
