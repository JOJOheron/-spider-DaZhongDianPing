import os
from shopinfo_function import shopinfo
from spider_function_plus import spider
cookie = "_lxsdk_cuid=176949db63a9d-0ccd78352dd0ac-c791039-1fa400-176949db63bc8; _lxsdk=176949db63a9d-0ccd78352dd0ac-c791039-1fa400-176949db63bc8; _hc.v=53da40ef-bb11-aa2a-11ec-bf6146b71457.1629703636; ctu=535739e024946b42805ec591dabc7bbba53bb49715c163daea500d76e1a7f592; s_ViewType=10; cityid=344; fspop=test; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1639619727; dplet=4dfea44aab4017cd1db5df2584cf3f0e; dper=a7084ea5f9ef99a8d964fb598b1735723a7793b980de3860e64aadf835646840e6a223e05118a9b88ebef5876b55dbb8eb4702db0213cda7595a62912c0257150880c0b04b2da6df5386ed1b005d556ecda90933891f48746876dd5435e55e55; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_0436014240; cy=2; cye=beijing; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1639621803; _lxsdk_s=17dc0f38c8c-33c-126-33f%7C%7C1999"
agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
url_spider = "http://www.dianping.com/beijing/ch10/o11p"
pagenum = 2
start = 1
end = 6
lite = "gv"
num = 0
result = shopinfo(cookie, agent, url_spider, pagenum, start, end)
for resultindex in result:
    shopid = resultindex
    spider(cookie, agent, shopid, pagenum, start, end, lite)
    num = num + 1
    print("第" + str(num) + "家店获取成功")
print("一共爬取了" + str(len(result)) + "个店铺")
print("**************爬虫结束，成功爬取所有数据***************")
os.remove("css.txt")
os.remove("svg.txt")
