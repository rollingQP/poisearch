from autosearch3 import *
import tkinter as tk
from tkinter import filedialog
import threading


def select_file():
    file = tk.filedialog.askopenfilename(title='请选择配置文件')
    configure_path.set(file)

def select_cities():
    file = tk.filedialog.askopenfilename(title='请选择城市文件')
    cities_file_path.set(file)

def select_keywords():
    file = tk.filedialog.askopenfilename(title='请选择关键词文件')
    keywords_file_path.set(file)

def main_func():
    (web_key, page_max_limit, keywords_file, cities_file)=load_configure(configure_path.get())
    if os.path.exists(cities_file_path.get()):
        cities_file = cities_file_path.get()
    if os.path.exists(keywords_file_path.get()):
        keywords_file = keywords_file_path.get()
    with open(keywords_file, 'r', encoding='utf-8-sig') as search_csv:
        reader_search = csv.reader(search_csv)
        column = [row[0] for row in reader_search]
    searchItems = column
    results = []

    with open(cities_file, 'r', encoding='utf-8-sig') as cities_csv:
        reader_cities = csv.reader(cities_csv)
        column = [row[0] for row in reader_cities]
    cityNameList = column

    singleCity = False

    for classfiled in searchItems:
        for cityName in cityNameList:
            results.append(get_result(web_key, url, page_max_limit, cityName, classfiled))

    # 输出
    # console_output(results, singleCity)

    # csv
    csvData = get_csvData(results, singleCity)
    csv_output(csvData, 'output.csv')
    messagetext.set('运行完毕')


def multithread():
    try:
        t = threading.Thread(target=main_func)
        t.start()
        messagetext.set('正在运行')
    except:
        print('运行失败')



if __name__ == '__main__':
    window = tk.Tk()
    window.title('地图自动搜索')

    messagetext = tk.StringVar()
    messagetext.set('等待操作')

    configure_path = tk.StringVar()
    configure_path.set(os.path.dirname(os.path.realpath(sys.argv[0]))+'/configure.txt')

    cities_file_path = tk.StringVar()

    keywords_file_path = tk.StringVar()

    label = tk.Label(window, text="配置文件:").grid(row=0, column=0)
    entry = tk.Entry(window, textvariable=configure_path, state="readonly").grid(row=0, column=1, ipadx=200)

    label2 = tk.Label(window, text="城市文件:").grid(row=1, column=0)
    entry2 = tk.Entry(window, textvariable=cities_file_path, state="readonly").grid(row=1, column=1, ipadx=200)

    label3 = tk.Label(window, text="关键词文件:").grid(row=2, column=0)
    entry3 = tk.Entry(window, textvariable=keywords_file_path, state="readonly").grid(row=2, column=1, ipadx=200)

    selectBotton1 = tk.Button(window, text="选择", command=select_file).grid(row=0, column=2)
    selectBotton2 = tk.Button(window, text="选择", command=select_cities).grid(row=1, column=2)
    selectBotton3 = tk.Button(window, text="选择", command=select_keywords).grid(row=2, column=2)

    startBotton = tk.Button(window, text="开始", command=multithread).grid(row=3, column=2)

    messagetextlabel = tk.Label(window, textvariable=messagetext).grid(row=3, column=1)

    window.mainloop()