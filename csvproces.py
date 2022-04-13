from urllib.parse import quote
from urllib import request
import json
import sys
import csv

web_key = 'a2d03b09e4cd9c7a207cab6dc40a39f6'  # 替换成自己的
url = 'https://restapi.amap.com/v3/place/text'
page_max_limit = 50  # 最大搜索页数，最大100
cityNameList = ['北京', '上海', '广州', '深圳', '武汉', '南京', '成都', '重庆', '杭州', '天津', '苏州', '长沙', '青岛', '西安', '郑州', '宁波', '无锡',
                '大连']


def get_result(web_key, url, page_max_limit, cityname, classfiled):
    results = []
    page_num = 1
    continueSearch = True
    sys.stdout.write('\r正在搜索：%s' % (cityname))
    sys.stdout.flush()
    while continueSearch:
        request_url = url + '?key=' + web_key + '&extensions=all&keywords=' + quote(classfiled) + '&city=' + quote(
            cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(page_num) + '&output=json'
        request_result = request.urlopen(request_url)
        data = request_result.read()
        data = data.decode('utf-8')
        if json.loads(data)['count'] == '0' or page_num > page_max_limit:
            continueSearch = False
            if page_num > page_max_limit:
                print('达到最大搜索页数限制，请调大page_max_limit')
        results.append(json.loads(data))
        page_num += 1
    return results


def get_csvData(results, singleCity):
    csvData = []
    if singleCity:
        for result in results:
            for i in range(len(result['pois'])):
                result['pois'][i]['gdwebsite'] = 'https://amap.com/place/' + result['pois'][i]['id']
                csvData.append({'name': result['pois'][i]['name'],
                                'pname': result['pois'][i]['pname'],
                                'cityname': result['pois'][i]['cityname'],
                                'adname': result['pois'][i]['adname'],
                                'business_area': result['pois'][i]['business_area'],
                                'address': result['pois'][i]['address'],
                                'gdwebsite': result['pois'][i]['gdwebsite']})

    else:
        for city in results:
            for result in city:
                for i in range(len(result['pois'])):
                    result['pois'][i]['gdwebsite'] = 'https://amap.com/place/' + result['pois'][i]['id']
                    csvData.append({'name': result['pois'][i]['name'],
                                    'pname': result['pois'][i]['pname'],
                                    'cityname': result['pois'][i]['cityname'],
                                    'adname': result['pois'][i]['adname'],
                                    'business_area': result['pois'][i]['business_area'],
                                    'address': result['pois'][i]['address'],
                                    'gdwebsite': result['pois'][i]['gdwebsite']})
    return csvData


def console_output(results, singleCity):
    count = 1
    if singleCity:
        for result in results:
            for i in range(len(result['pois'])):
                result['pois'][i]['gdwebsite'] = 'https://amap.com/place/' + result['pois'][i]['id']
                print(count, ': 名称:', result['pois'][i]['name']
                      , '\n类型:', result['pois'][i]['type']
                      , '\n省份:', result['pois'][i]['pname']
                      , '\n城市:', result['pois'][i]['cityname']
                      , '\n地区:', result['pois'][i]['adname']
                      , '\n乡镇:', result['pois'][i]['business_area']
                      , '\n详细地址:', result['pois'][i]['address']
                      # , '\n经纬度:', result['pois'][i]['location']
                      , '\n在高德地图中显示:', result['pois'][i]['gdwebsite']
                      , '\n'
                      )
                count += 1

    else:
        for city in results:
            for result in city:
                for i in range(len(result['pois'])):
                    print(count, ': 名称:', result['pois'][i]['name']
                          , '\n类型:', result['pois'][i]['type']
                          , '\n省份:', result['pois'][i]['pname']
                          , '\n城市:', result['pois'][i]['cityname']
                          , '\n地区:', result['pois'][i]['adname']
                          , '\n乡镇:', result['pois'][i]['business_area']
                          , '\n详细地址:', result['pois'][i]['address']
                          # , '\n经纬度:', result['pois'][i]['location']
                          , '\n在高德地图中显示:', 'https://amap.com/place/' + result['pois'][i]['id']
                          , '\n'
                          )
                    count += 1


def csv_output(csvData, fileName):
    headers = ['name', 'pname', 'cityname', 'adname', 'business_area', 'address', 'gdwebsite']
    with open(fileName, 'w', newline='') as outPutFile:
        csvFile = csv.DictWriter(outPutFile, headers)
        csvFile.writeheader()
        for result in results:
            csvFile.writerows(csvData)


if __name__ == '__main__':

    # 输入
    cityName = input('城市名：')
    if len(cityName) > 0:
        singleCity = True
        classfiled = input('搜索：')
        results = get_result(web_key, url, page_max_limit, cityName, classfiled)
    else:
        singleCity = False
        classfiled = input('搜索：')
        results = []
        for cityName in cityNameList:
            results.append(get_result(web_key, url, page_max_limit, cityName, classfiled))

    # 输出
    console_output(results, singleCity)

    # csv
    csvData = get_csvData(results, singleCity)
    csv_output(csvData, 'output.csv')

