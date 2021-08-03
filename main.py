import time, re
import moviepy.editor
import downloader, cover, getInfo, config

if __name__ == '__main__':
    list = getInfo.get_list(config.fid)
    # prepare historylist
    with open('./history.list', 'r') as f:
        donelist = f.read().split('$')
    # check update
    update_pool = []
    for i in list:
        if i['link'] not in donelist :
            print(i['link'])
            update_pool.append(i)
    # update
    print('\ndownloading start\n')
    for i in update_pool:
        try:
            # download video
            ftitle = downloader.main(i['link'] + '?p=1')
            # convert into audio
            mp3path = config.music_path + re.sub(r'[\/\\:*?"<>|]', '', i['title']) + '.mp3'
            clip = moviepy.editor.AudioFileClip(config.video_path + ftitle + '/' + ftitle + '.flv') 
            clip.write_audiofile(mp3path)
            # save cover
            try:
                cover.save_cover(i['cover'])
            except:
                with open('./log.txt', 'a') as f:
                    f.writelines('error when save  the cover of ' + ftitle + i['link'] + '\n')
            # insert cover
            try:
                cover.add_cover(i['cover'], mp3path)
            except:
                with open('./log.txt', 'a') as f:
                    f.writelines('error when inserting cover to: ' + ftitle + i['link'] + '\n')
        except:
            with open('./log.txt', 'a') as f:
                f.writelines('error when downloading: ' + i['link'] + '\n')
        else:
            print('successfully downloaded: ' + i['link'] + '\n')
            # update database
            donelist.append(i['link'])
            with open('./history.list', 'w') as f:
                f.write('$'.join(donelist))
                f.close()
        time.sleep(config.delayTime)
