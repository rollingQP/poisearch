from urllib.parse import quote
from urllib import request
import json
import sys
import csv


url = 'https://restapi.amap.com/v3/place/text'
page_max_limit = 80  # 最大搜索页数，最大100


def get_key(key_file_path, MSP):    # MSP: Map Service Provider
    with open(key_file_path, 'r') as key_json_file:
        keyData=key_json_file.read()
        keyData = json.loads(keyData)
    found = False
    for Key in keyData['Key']:
        if Key['name'] == MSP:
            web_key = Key['key']
            found = True
    if found:
        return web_key
    else:
        raise Exception('无法获取key')


web_key = get_key('key.json', 'amap')

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
        for classfiled in results:
            for result in classfiled:
                for i in range(len(result['pois'])):
                    try:
                        result['pois'][i]['gdwebsite'] = 'https://amap.com/place/' + result['pois'][i]['id']
                        try:
                            csvData.append({'name': result['pois'][i]['name'],
                                            'pname': result['pois'][i]['pname'],
                                            'cityname': result['pois'][i]['cityname'],
                                            'adname': result['pois'][i]['adname'],
                                            'business_area': result['pois'][i]['business_area'],
                                            'address': result['pois'][i]['address'],
                                            'gdwebsite': result['pois'][i]['gdwebsite']})
                        except:
                            print('有误，请单独处理：' + result['pois'][i]['gdwebsite'])
                    except:
                        pass

    else:
        for city in results:
            for result in city:
                for i in range(len(result['pois'])):
                    try:
                        result['pois'][i]['gdwebsite'] = 'https://amap.com/place/' + result['pois'][i]['id']
                        try:
                            csvData.append({'name': result['pois'][i]['name'],
                                            'pname': result['pois'][i]['pname'],
                                            'cityname': result['pois'][i]['cityname'],
                                            'adname': result['pois'][i]['adname'],
                                            'business_area': result['pois'][i]['business_area'],
                                            'address': result['pois'][i]['address'],
                                            'gdwebsite': result['pois'][i]['gdwebsite']})
                        except:
                            print('有误，请单独处理：' + result['pois'][i]['gdwebsite'])
                    except:
                        pass
    return csvData


def console_output(results, singleCity):
    count = 1
    if singleCity:
        for classfiled in results:
            for result in classfiled:
                for i in range(len(result['pois'])):
                    try:
                        result['pois'][i]['gdwebsite'] = 'https://amap.com/place/' + result['pois'][i]['id']
                        try:
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
                        except:
                            print('有误，请单独处理：' + result['pois'][i]['gdwebsite'])
                        count += 1
                    except:
                        pass

    else:
        for city in results:
            for result in city:
                for i in range(len(result['pois'])):
                    try:
                        result['pois'][i]['gdwebsite'] = 'https://amap.com/place/' + result['pois'][i]['id']
                        try:
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
                        except:
                            print('有误，请单独处理：' + result['pois'][i]['gdwebsite'])
                        count += 1
                    except:
                        pass


def csv_output(csvData, fileName):
    headers = ['name', 'pname', 'cityname', 'adname', 'business_area', 'address', 'gdwebsite']
    with open(fileName, 'w', newline='', encoding='utf-8-sig') as outPutFile:
        csvFile = csv.DictWriter(outPutFile, headers)
        csvFile.writeheader()
        for result in results:
            csvFile.writerows(csvData)


if __name__ == '__main__':

    with open('search.csv', 'r', encoding='utf-8-sig') as search_csv:
        reader_search = csv.reader(search_csv)
        column = [row[0] for row in reader_search]
    searchItems = column
    results = []

    with open('cities.csv', 'r', encoding='utf-8-sig') as cities_csv:
        reader_cities = csv.reader(cities_csv)
        column = [row[0] for row in reader_cities]
    cityNameList = column

    singleCity = False

    for classfiled in searchItems:
        for cityName in cityNameList:
            results.append(get_result(web_key, url, page_max_limit, cityName, classfiled))

# 输出
console_output(results, singleCity)

# csv
csvData = get_csvData(results, singleCity)
csv_output(csvData, 'output.csv')
