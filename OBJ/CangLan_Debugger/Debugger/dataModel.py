import numpy as np
import matplotlib.pyplot as plt
import time
import json


class DataBlock:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.valueArray = 0


class DataLinspace:
    def __init__(self, name, num):
        self.name = name
        self.valueArray = np.linspace(0, 1, num)


class DataBase:
    def __init__(self, dataDict: dict):
        self.dataDict = dataDict  # 从这里读取数据
        self.points_num = 10
        self.dataList = list()
        self.x_axis = DataLinspace('default', self.points_num)  # x轴数据存储
        self.y_axis_dict = dict()  # y轴数据存储
        self.timeLinspace = np.linspace(0, 1, self.points_num)
        self.zerotime = time.time()

        self.stepSTA = False
        self.pointer = 0

    def set_x_axis(self, dataName='__TS'):
        if dataName == '__TS':
            self.x_axis = DataLinspace('time', self.points_num)
        elif dataName in self.dataDict.keys():
            self.x_axis = DataLinspace(dataName, self.points_num)

    def set_y_axis_list(self, dataNameList: list):
        not_in = [element for element in dataNameList if element not in self.dataDict.keys()]
        if len(not_in) < 1:
            self.y_axis_dict = {}
            for dataName in dataNameList:
                self.y_axis_dict[dataName] = DataLinspace(dataName, self.points_num)

    def drawCanvas(self):
        plt.clf()
        plt.xlabel(self.x_axis.name)
        print(f'即将绘制图片:x->[{self.x_axis.name}],y->{self.y_axis_dict.keys()}')

        print(self.x_axis.valueArray)
        for y in self.y_axis_dict.keys():
            print(self.y_axis_dict[y].valueArray)

        if self.x_axis.name != 'time':
            for y in self.y_axis_dict.keys():
                plt.plot(self.x_axis.valueArray, self.y_axis_dict[y].valueArray, label=self.y_axis_dict[y].name)
        elif self.x_axis.name == 'time':
            for y in self.y_axis_dict.keys():
                plt.plot(self.timeLinspace, self.y_axis_dict[y].valueArray, label=self.y_axis_dict[y].name)

        plt.show()

    def reset_input(self, points_num, x_name, y_namelist):
        self.zerotime = time.time()
        self.points_num = points_num
        self.pointer = 0
        self.set_x_axis(x_name)
        self.set_y_axis_list(y_namelist)
        self.timeLinspace = np.linspace(0, 1, self.points_num)

        self.stepSTA = True

    def step_input(self, time):
        if self.stepSTA:
            self.timeLinspace[self.pointer] = time - self.zerotime
            if self.x_axis.name != 'time':
                self.x_axis.valueArray[self.pointer] = self.dataDict[self.x_axis.name]
            for y in self.y_axis_dict.keys():
                self.y_axis_dict[y].valueArray[self.pointer] = self.dataDict[y]
            self.pointer += 1
            if self.pointer >= self.points_num:
                self.stepSTA = False

        return self.stepSTA

    def export_dict_to_json(self):
        print("将数据导出至database.json")
        with open("database.json", 'w', encoding='utf-8') as f:
            json.dump(self.dataDict, f, ensure_ascii=False, indent=4)

    def read_json_to_dict(self):
        print("从database.json导入数据")
        with open("database.json", 'r', encoding='utf-8') as f:
            newdict = json.load(f)
            for key,value in newdict.items():
                self.dataDict[key]=value

if __name__ == "__main__":
    import time

    testDataDict = {'x': 0, 'y1': 0, 'y2': 10, 'y3': 5}
    db = DataBase(testDataDict)
    num = 100
    db.reset_input(num, 'x', ['y1', 'y2', 'y3'])
    while db.step_input(time.time()):
        testDataDict['x'] = testDataDict['x'] + 1
        testDataDict['y1'] = testDataDict['y1'] + 0.1
        testDataDict['y2'] = testDataDict['y2'] - 0.1
        testDataDict['y3'] = testDataDict['y3'] - 0.1

    db.drawCanvas()
