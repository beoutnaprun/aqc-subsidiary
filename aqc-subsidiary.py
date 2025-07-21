import json
import time
import urllib
import urllib3
import requests
import argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
parser = argparse.ArgumentParser(description='This is the help!')
parser.add_argument('-c', '--company', help='要查询的单位全称', default='')
parser.add_argument('-n', '--number', help='要查询大于等于的控股数值', default='')
parser.add_argument('-o', '--out', help='输出的文件名，默认不输出', default='')
args = parser.parse_args()


def getConfig():
    with open('config.json','r',encoding='utf-8') as json_file:
        config = json.load(json_file)
    return config

proxy = {
    # 'http': 'http://127.0.0.1:8082',
    # 'https': 'http://127.0.0.1:8082',
}

header = {
    'cookie': urllib.parse.unquote(getConfig()['cookie']),
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://aiqicha.baidu.com',
    'Accept-Encoding': 'gzip'
}

# 先通过公司名获取pid
def Suggest(name):
    url = 'https://aiqicha.baidu.com/index/suggest'
    data = {
        'q':name
    }
    try:
        response = requests.post(url,verify=False,allow_redirects=False,headers=header,data=data,proxies=proxy,timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(e)
        return ''



def StockchartAjax(pid):
    url = f'https://aiqicha.baidu.com/stockchart/stockchartAjax?drill=0&pid={pid}'
    try:
        response = requests.get(url,verify=False,allow_redirects=False,headers=header,proxies=proxy,timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(e)
        return ''

def main():
    print('=' * 50)
    print('Tips:请自行前往config.json 配置爱企查的Cookie')
    print('='*50)
    filename = ''
    try:
        number = int(args.number)
    except Exception as e:
        number = 50
    if args.out != "":
        filename = args.out
    if args.company != '':
        company = args.company
        resp = Suggest(company)
        pid = 0
        if resp != "":
            for name_list in resp['data']['queryList']:
                com_name = name_list['resultStr'].replace('</em>','').replace('<em>','')
                if com_name == company:
                    pid = name_list['pid']
        if pid != 0:
            time.sleep(1)
            resp_data = StockchartAjax(pid)
            out_data = ''
            if resp_data != "":
                # 打印上级单位
                sj_com_data = resp_data['data']['shareholdersData']['list']
                print("*" * 50)
                print("上级单位-列表")
                print("*" * 50)
                for sj_com in sj_com_data:
                    print(sj_com['name'])
                print("*" * 50)
                print('-' * 20 +"分割" + '-'* 20)
                # 打印下级单位
                xj_com_data = resp_data['data']['investRecordData']['list']
                print("*" * 50)
                print("下级单位-列表 - 控股大于等于：" + str(number))
                print("*" * 50)
                for xj_com in xj_com_data:
                    kg_number = int(float(xj_com['regRate'].replace('%','')))
                    if int(number) <= kg_number:
                        print(xj_com['entName'])
                        if filename != '':
                            out_data += xj_com['entName'] +'\n'
                print("*" * 50)
                if filename != '':
                    with open(filename,'w',encoding='utf-8') as f:
                        f.write(out_data)
                    print("out file is " + filename )
            else:
                print(f'pid={pid} 未查询到数据')
        else:
            print(f'未查询到 {company} 的pid数据')
    else:
        print('python aqc-subsidiary.py -c {company}')



if __name__ == '__main__':
    main()
