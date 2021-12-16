import os
import time
import parsel
import requests
import re
import xlrd
from bs4 import BeautifulSoup
from xlutils.copy import copy


def spider(cookie, agent, shopid, pagenum, pagestart, pageend, lite):
    # 设置请求头
    global css_respones, comment_block
    headers = {
        "Cookie": cookie,
        "Host": "www.dianping.com",
        "Referer": "http://www.dianping.com/shop/" + str(shopid) + "/review_all?queryType=reviewGrade&queryVal=bad",
        "User-Agent": agent
    }
    headers_svg = {
        "Host": "s3plus.meituan.net",
        "User-Agent": "jojo"
    }
    # 初始化差评文本、excel、以及col差评数量参数
    commenttext = ""
    workbook = xlrd.open_workbook('TEST_' + str(pagestart) + '_' + str(pageend) + '_' + str(pagenum) + '.xls')
    worksheet = workbook.sheet_by_name('first sheet')
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    cols = int(worksheet.nrows)

    # 依次爬取差评的每一个页面,pagenum表示爬取每一家店面的差评的前几页
    for page in range(1, int(pagenum) + 1):
        # 获取html
        # 抛出异常，避免店铺的差评页数不够
        try:
            time.sleep(10)
            respones = requests.get("http://www.dianping.com/shop/" + str(shopid) + "/review_all/p" + str(
                page) + "?queryType=reviewGrade&queryVal=bad", headers=headers)
            print("获取html成功——该家(" + str(shopid) + ")店面差评的第" + str(page) + "页面")
            if (not (os.path.isfile("css.txt"))):
                # 获取css
                css_url = re.findall(r'<link rel="stylesheet" type="text/css" href="(//s3plus.meituan.*?)">',
                                     respones.text)
                css_url = 'http:' + css_url[0]
                css_respones = requests.get(css_url)
                print("获取css成功——该家(" + str(shopid) + ")店面差评的第" + str(page) + "页面")
                f = open("css.txt", "w", encoding='utf-8')
                f.write(css_respones.text)
                f.close()
            else:
                print("获取css成功——该家(" + str(shopid) + ")店面差评css")
            if (not (os.path.isfile("svg.txt"))):
                # 获取svg
                svg_url = re.findall(
                    r'background-image: url\((.*?)\);',
                    css_respones.text)
                svg_url = 'http:' + svg_url[1]
                svg_respones = requests.get(svg_url, headers=headers_svg)
                f = open("svg.txt", "w", encoding='utf-8')
                f.write(svg_respones.text)
                f.close()
                print("获取svg成功——该家(" + str(shopid) + ")店面差评的第" + str(page) + "页面")
            else:
                print("获取svg成功——该家(" + str(shopid) + ")店面差评svg")
        except:
            print("抛出异常")
            continue
        # 获取解密字体集合map
        svg = open("svg.txt", "r", encoding='utf-8')
        svg_text = svg.read()
        css = open("css.txt", "r", encoding='utf-8')
        css_text = css.read()
        sel = parsel.Selector(svg_text)
        texts = sel.css("text")
        lines = []
        for text in texts:
            lines.append([int(text.css("text::attr(y)").get()), text.css("text::text").get()])
        class_map = re.findall("\.(" + str(lite) + "\w+){background:-(\d+)\.0px -(\d+)\.0px;\}", css_text)
        class_map = [(cls_name, int(x), int(y)) for cls_name, x, y in class_map]
        d_map = {}
        # 将加密字体与解密字体集合匹配
        for one_char in (class_map):
            try:
                cls_name, x, y = one_char
                for line in lines:
                    if line[0] < y:
                        pass
                    else:
                        index = int(x / 14)
                        char = line[1][index]
                        d_map[cls_name] = char
                        break
            except Exception as e:
                print(e)

        # 将加密字体进行解密，创建解密后的html
        responestext = respones.text
        for key, value in d_map.items():
            html = responestext.replace('<svgmtsi class="' + key + '"></svgmtsi>', value)
            responestext = html
        soup = BeautifulSoup(html, "html.parser")
        # 获取店铺人均消费
        avg_price = soup.find_all('span', class_='price')
        shopavg_price = re.findall('\d+', str(avg_price))[0]
        # 店铺综合评分信息
        shopinfo = soup.find_all('span', class_='score')
        shop_taste_0 = re.findall('\>口味：\d+.\d', str(shopinfo))
        shop_taste = re.findall('\d+.\d', str(shop_taste_0))[0]
        shop_envir_0 = re.findall('\>环境：\d+.\d', str(shopinfo))
        shop_envir = re.findall('\d+.\d', str(shop_envir_0))[0]
        shop_ser_0 = re.findall('\>服务：\d+.\d', str(shopinfo))
        shop_ser = re.findall('\d+.\d', str(shop_ser_0))[0]

        # 获取每一条评论块
        comments = soup.find_all('div', class_='main-review')
        # 每一页评论数序数参数
        pagecols = -1
        # 依次读取每一条评论块
        for comment in comments:
            cols = cols + 1
            pagecols = pagecols + 1

            # 获取每一条评论的文本、点赞数目（try语句适应不同的评论块结构（是否需要展开评论））
            try:
                comment_block = BeautifulSoup(str(comment), "html.parser").find_all('div', class_='review-words Hide')
                comment_replyinfo = BeautifulSoup(str(comment), "html.parser").find_all('span', class_='actions')
            except Exception as e:
                print(e)
            else:
                comment_block = BeautifulSoup(str(comment), "html.parser").find_all('div', class_='review-words')

            # 评论星级
            comment_replystar = BeautifulSoup(str(comment), "html.parser").find_all('div', class_='review-rank')
            star = re.findall('<span class=\"sml-rank-stars sml-str[\d]* star\">', str(comment_replystar))
            comment_star = re.findall('\d+', str(star))[0]

            # 口味评分
            taste_envir_ser = BeautifulSoup(str(comment), "html.parser").find_all('span', class_='score')
            comment_taste = re.findall('口味：\d+.\d', str(taste_envir_ser))
            comment_tastenum = re.findall('\d+.\d', str(comment_taste))[0]

            # 环境评分
            comment_envir = re.findall('环境：\d+.\d', str(taste_envir_ser))
            comment_envirnum = re.findall('\d+.\d', str(comment_envir))[0]

            # 服务评分
            comment_ser = re.findall('服务：\d+.\d', str(taste_envir_ser))
            comment_sernum = re.findall('\d+.\d', str(comment_ser))[0]

            # 照片数目
            comment_img = BeautifulSoup(str(comment), "html.parser").find_all('ul')
            list_img = re.findall('<img data-big=(.*?) data-lazyload=(.*?)>', str(comment_img))
            img_num = len(list_img)

            # 正则表达式获取点赞数字
            comment_goodnum_0 = re.findall('\赞\D([\s]*?)\<\/[a]\>([\s]*?)\<(.*)\)', str(comment_replyinfo))
            try:
                comment_goodnum = re.findall('\d', str(comment_goodnum_0))[0]
            except:
                comment_goodnum=0

            # 正则表达式获取回应数字
            comment_replynum_0 = re.findall('\回应<\/a\>([\s]*?)\<(.*)\)', str(comment_replyinfo))
            try:
                comment_replynum = re.findall('\d', str(comment_replynum_0))[0]
            except:
                comment_replynum=0

            # 获得评论内容
            delcomment = comment_block[0].get_text().replace(" ", "").replace('\n', '').replace("收起评价", "")
            # 创建excel文件
            new_worksheet.write(cols, 0, str(shopid))
            new_worksheet.write(cols, 1, str(shopavg_price))
            new_worksheet.write(cols, 2, str(shop_taste))
            new_worksheet.write(cols, 3, str(shop_envir))
            new_worksheet.write(cols, 4, str(shop_ser))
            new_worksheet.write(cols, 5, str(delcomment))
            new_worksheet.write(cols, 6, str(comment_goodnum))
            new_worksheet.write(cols, 7, str(comment_replynum))
            new_worksheet.write(cols, 8, str(comment_star))
            new_worksheet.write(cols, 9, str(comment_tastenum))
            new_worksheet.write(cols, 10, str(comment_envirnum))
            new_worksheet.write(cols, 11, str(comment_sernum))
            new_worksheet.write(cols, 12, str(img_num))
    new_workbook.save('TEST_' + str(pagestart) + '_' + str(pageend) + '_' + str(pagenum) + '.xls')  # 保存文件
    print("更新excel成功")