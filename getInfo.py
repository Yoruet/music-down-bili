import requests, json, re, time
import Bv2Av, config
fid = config.fid
headers = {
            'Referer': 'https://space.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }

def send_request(url):
    i = 0
    while i < 3:
        try:
            return json.loads(requests.get(url, headers=headers).text)
        except:
            i += 1

def get_list(fid):
    list = []
    num = 0
    while(1):
        num = num + 1
        url = 'https://api.bilibili.com/x/v3/fav/resource/list?media_id=' + str(fid) + '&pn=' + str(num) + '&ps=20'
        res = send_request(url)
        pn = re.findall(r'(?<=pn=)[0-9]*',url)[0]
        elements = ['title', 'cover', 'bvid']
        try:
            len_videos = len(res['data']['medias'])
            for j in range(len_videos):
                video = {}
                for k in elements:
                    video[k] = res['data']['medias'][j][k]
                video['link'] = Bv2Av.bv2av(video['bvid'])
                video['pn'] = pn
                # print(vedio,'\n')
                list.append(video)
                # print(q.get())
        except:return list
    return list

if __name__ == '__main__':
    start_time = time.time()
    list = get_list(fid)
    # with open('database.pwp', 'r') as f:
    #     donelist = f.read().split('$')
    # print(list)
    with open('database.list','w', encoding='utf-8') as f:
        for i in list:
            f.write(str(i)+'\n')
    print(time.time()-start_time)
