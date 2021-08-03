import csv
import os
from turtle import pd


def create_csv(path):
    if not os.path.isfile(path):
        with open(path, "w+", newline='') as file:
            csv_file = csv.writer(file)
            head = ["terminalId"]
            csv_file.writerow(head)


def append_csv(path, datas):
    with open(path, "a+", newline='') as file:  # 处理csv读写时不同换行符  linux:\n    windows:\r\n    mac:\r
            csv_file = csv.writer(file)
            # datas = [["hoojjack", "boy"], ["hoojjack1", "boy"]]
            csv_file.writerows(datas)


def read_csv(path):
    with open(path, "r+") as file:
        csv_file = csv.reader(file)
        for data in csv_file:
            print("data:", data)


def pandas_write(path):
    name = ["hoojjack", "hoojjack1"]
    sex = ["boy", "boy"]
    # 字典中的key值即为csv中列名
    data_frame = pd.DataFrame({"name": name, "sex": sex})
    # 将DataFrame存储为csv,index表示是否显示行名，default=True，path指写入的文件名称
    data_frame.to_csv(path, index=True, sep='')
