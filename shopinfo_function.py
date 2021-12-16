import re
import time
import requests
import xlwt

def shopinfo(cookie,agent,shoplisturl,pagenum,pagestart,pageend):
    shopurllist=[]
    headers = {
        "Cookie": "navCtgScroll=0; _lxsdk_cuid=176949db63a9d-0ccd78352dd0ac-c791039-1fa400-176949db63bc8; _lxsdk=176949db63a9d-0ccd78352dd0ac-c791039-1fa400-176949db63bc8; _hc.v=53da40ef-bb11-aa2a-11ec-bf6146b71457.1629703636; ctu=535739e024946b42805ec591dabc7bbba53bb49715c163daea500d76e1a7f592; s_ViewType=10; cityid=344; fspop=test; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1639619727; dplet=4dfea44aab4017cd1db5df2584cf3f0e; dper=a7084ea5f9ef99a8d964fb598b1735723a7793b980de3860e64aadf835646840e6a223e05118a9b88ebef5876b55dbb8eb4702db0213cda7595a62912c0257150880c0b04b2da6df5386ed1b005d556ecda90933891f48746876dd5435e55e55; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_0436014240; cy=2; cye=beijing; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1639631199; _lxsdk_s=17dc18f41ed-701-f01-783%7C%7C240",
        "Host": "www.dianping.com",
        "Referer": "http://www.dianping.com/beijing/ch10/o11p3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    for page in range(int(pagestart), int(pageend)+1):
        time.sleep(2)
        respones = requests.get(shoplisturl+str(page), headers=headers)
        shoplist = re.findall('\<div class=\"tit\">([\s\S]*?)\>', respones.text)
        for i in range(1, len(shoplist)+1):
            shopurl=re.findall('http:\/\/www\.dianping\.com/shop/(.*?)\"', shoplist[i-1])
            shopurllist.append(shopurl[0])

    print("成功获取"+str(pagestart)+"到"+str(pageend)+"页所有的店铺ID，一共"+str(len(shopurllist))+"家店。")

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('first sheet', cell_overwrite_ok=True)
    worksheet.write(0, 0, "店铺ID")
    worksheet.write(0, 1, "店铺人均消费")
    worksheet.write(0, 2, "店铺综合口味评分")
    worksheet.write(0, 3, "店铺综合环境评分")
    worksheet.write(0, 4, "店铺综合服务评分")
    worksheet.write(0, 5, "文本内容")
    worksheet.write(0, 6, "差评点赞数")
    worksheet.write(0, 7, "回应数目")
    worksheet.write(0, 8, "评论星级")
    worksheet.write(0, 9, "用户口味评分")
    worksheet.write(0, 10, "用户环境评分")
    worksheet.write(0, 11, "用户服务评分")
    worksheet.write(0, 12, "照片数目")
    workbook.save('TEST_'+str(pagestart)+'_'+str(pageend)+'_'+str(pagenum)+'.xls')  # 保存文件
    return shopurllist
