import requests
from requests.exceptions import RequestException
import re
import json
import time


def get_one_page(url):
    """
    获取一个页面的数据
    :param url: 目标资源链接
    :return: response or None
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/77.0.3865.90 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    """
    解析一个页面的内容
    :param html: HTML数据
    :return: None
    """
    #  定义模式化对象，compile()返回一个模式对象
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>'
                         '.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>'
                         '.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>'
                         '.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    #  使用正则提取数据
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6],
        }


def write_to_file(content):
    """
    将解析完的内容保存到本地
    :param content: 要保存的内容
    :return: None
    """
    # 定义保存路径
    with open('../Spider_Demo_data/猫眼排行top100', 'a', encoding='utf8') as f:
        # json.dumps() 将python对象编码成json字符串，因为输出中文所有指定ensure_ascii=False
        f.write(json.dumps(content, ensure_ascii=False)+'\n')


def main(offset):
    """
    主函数
    :param offset: 目标链接的偏移量
    :return: None
    """
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    #  调用获取页面数据的方法，得到一个HTML数据
    html = get_one_page(url)
    # 使用for循环遍历解析完的数据
    for item in parse_one_page(html):
        # 保存数据
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(i*10)
        # 增加一个延时等待
        time.sleep(1)
