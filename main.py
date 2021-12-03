import time, re, os, shutil
import config
# prepare environment
if not os.path.exists(config.music_path) == True:
    os.makedirs(config.music_path)
if not os.path.exists(config.video_path) == True:
    os.makedirs(config.video_path)
path = re.sub(r'\\Roaming','',os.getenv("APPDATA")) + '\\Local\\imageio\\ffmpeg\\'
if not os.path.exists(path) == True:
    os.makedirs(path)
# print(path)
shutil.copyfile('./ffmpeg.win32.exe',path + 'ffmpeg.win32.exe')
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import downloader
import cover
import getInfo

if __name__ == '__main__':
    list = getInfo.get_list(config.fid)
    # prepare historylist
    with open('./history.list', 'r') as f:
        donelist = f.read().split('$')
    # check update
    update_pool = []
    print('本次待执行的任务:',end='\n')
    for i in list:
        if i['link'] not in donelist :
            print(i['link'])
            update_pool.append(i)
    # update
    print('\ndownloading start\n')
    for i in update_pool:
        try:
            print('正在下载' + i['title'] + ',请稍等:\n')
            # download video
            ftitle = downloader.main(i['link'] + '?p=1')
            # convert into audio
            mp3path = config.music_path + re.sub(r'[\/\\:*?"<>|]', '', i['title']) + '.mp3'
            clip = AudioFileClip(config.video_path + ftitle + '/' + ftitle + '.flv') 
            clip.write_audiofile(mp3path)
            # insert cover
            try:
                cover.add_cover(i['cover'], mp3path)
            except:
                print('error when inserting cover to: ' + ftitle + i['link'] + '\n')
                with open('./log.txt', 'a') as f:
                    f.writelines('error when inserting cover to: ' + ftitle + i['link'] + '\n')
        except:
            print('error when downloading: ' + i['link'] + '\n')
            with open('./log.txt', 'a') as f:
                f.writelines('error when downloading: ' + i['link'] + '\n')
        else:
            print('successfully downloaded: ' + i['link'] + '\n')
            with open('./log.txt', 'a') as f:
                f.writelines('successfully downloaded: ' + i['link'] + '\n')
            # update database
            donelist.append(i['link'])
            with open('./history.list', 'w') as f:
                f.write('$'.join(donelist))
                f.close()
        time.sleep(config.delayTime)
