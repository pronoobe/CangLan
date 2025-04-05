import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class KeyValueBlock:
    def __init__(self, root, valueDict: dict, valueName: str, label_width: int):
        self.frame = tk.Frame(root)
        self.valueDict = valueDict
        self.valueName = valueName
        self.type = type(self.valueDict[self.valueName])
        self.label_width = label_width
        self.create_widgets()
        self.readMode = True

    def create_widgets(self):
        # 创建Label
        self.label = tk.Label(self.frame, text=self.valueName + ' : ', width=self.label_width, anchor='e')
        self.label.pack(side='left')

        # 创建Entry
        self.entry = tk.Entry(self.frame, state='normal')
        self.readModeRefresh()
        self.entry.pack(side='left')

        # 创建两个多选框的变量
        self.var_x = tk.IntVar(self.frame)
        self.var_y = tk.IntVar(self.frame)

        # 创建两个多选框，每个多选框绑定到一个不同的变量
        self.x_checkbox = tk.Checkbutton(self.frame, text='x', variable=self.var_x, command=self.setVarX)
        self.y_checkbox = tk.Checkbutton(self.frame, text='y', variable=self.var_y, command=self.setVarY)

        self.x_checkbox.pack(side='left')
        self.y_checkbox.pack(side='left')

    def setVarX(self):
        if self.var_x.get():
            self.var_y.set(False)

    def setVarY(self):
        if self.var_y.get():
            self.var_x.set(False)

    def readModeRefresh(self):
        # self.entry.config(state='normal')
        self.entry.delete(0, tk.END)
        self.entry.insert(0, f"{self.valueDict[self.valueName]}")
        # self.entry.config(state='readonly')

    def setReadMode(self, mode):
        self.readMode = mode
        if not mode:
            self.entry.config(state='normal')
        else:
            self.entry.config(state='normal')

        return self.readMode

    def clearButton(self, buttonStr: str):
        if buttonStr == 'x':
            self.var_x.set(False)
        if buttonStr == 'y':
            self.var_y.set(False)
        if buttonStr == 'xy':
            self.var_x.set(False)
            self.var_y.set(False)

    def getvalue(self):
        if self.type == float:
            self.valueDict[self.valueName] = float(self.entry.get())
        elif self.type == int:
            self.valueDict[self.valueName] = int(self.entry.get())

        return self.valueDict[self.valueName]


class ValueDictTable:
    def __init__(self, root, key_value_dict):
        self.frame = tk.Frame(root, height=300, width=200, padx=10, pady=10)
        self.valueTableFrame = tk.Frame(self.frame)
        self.ButtonFrame = tk.Frame(self.frame, padx=10, pady=10)

        self.loadjson_function = lambda :print("从JSON文件中加载数据")
        self.exportjson_function = lambda :print("从JSON文件中导出数据")

        self.DrawTips = tk.Label(self.ButtonFrame, text="注：如不选择x坐标则默认以采样时间为绘图x坐标")
        self.clearXButton = tk.Button(self.ButtonFrame, text="清空已选中的X", command=self.clearAllX, width=20)
        self.clearYButton = tk.Button(self.ButtonFrame, text="清空已选中的Y", command=self.clearAllY, width=20)
        self.loadButton = tk.Button(self.ButtonFrame, text="加载数据", command=self.load, width=16)
        self.exportButton = tk.Button(self.ButtonFrame, text="导出数据", command=self.export, width=16)

        self.DrawTips.pack(side='left', padx=20)
        self.clearXButton.pack(side='left', padx=20)
        self.clearYButton.pack(side='left', padx=20)
        self.exportButton.pack(side='left', padx=20)
        self.loadButton.pack(side='left', padx=20)

        self.key_value_dict = key_value_dict
        self.max_key_length = max(len(key) for key in key_value_dict.keys()) * 2
        self.blockDict = dict()

        # self.canvas=tk.Canvas(self.frame, height=300, width=200)
        # self.canvas.pack(side="left", fill="both", expand=True)

        self.valueNum = len(self.key_value_dict.keys())

        i = 0
        j = 0

        for key in self.key_value_dict.keys():
            self.blockDict[key] = KeyValueBlock(self.valueTableFrame, self.key_value_dict, key, self.max_key_length)
            self.blockDict[key].frame.grid(row=j, column=i, pady=2)
            i += 1
            if i >= 3:
                i = 0
                j += 1

        self.valueTableFrame.grid(row=0,column=0)
        self.ButtonFrame.grid(row=1,column=0,columnspan=2)

    def get_checked_values(self):
        checked_x = [key for key, block in self.blockDict.items() if block.var_x.get()]
        checked_y = [key for key, block in self.blockDict.items() if block.var_y.get()]
        return checked_x, checked_y

    def clearAllX(self):
        for valueBlock in self.blockDict.values():
            valueBlock.clearButton('x')

    def clearAllY(self):
        for valueBlock in self.blockDict.values():
            valueBlock.clearButton('y')

    def setValueReadMode(self, mode):
        for valueBlock in self.blockDict.values():
            valueBlock.setReadMode(mode)

    def refreshAllvalue(self):
        for valueBlock in self.blockDict.values():
            valueBlock.readModeRefresh()

    def load(self):
        result = messagebox.askokcancel("数据操作",
                                        f"是否从database.json导入数据？")
        if result:
            self.loadjson_function()
            self.refreshAllvalue()

    def export(self):
        result = messagebox.askokcancel("数据操作",
                                        f"是否将数据导出至database.json？")
        if result:
            self.setAllNewValue()
            self.refreshAllvalue()
            self.exportjson_function()

    def setAllNewValue(self):
        for valueBlock in self.blockDict.values():
            valueBlock.getvalue()

class ModeChoser:
    def __init__(self, root, formatList: list):
        self.formatList = formatList
        self.frame = tk.Frame(root, padx=10, pady=10)
        self.modeVar = tk.StringVar(self.frame)
        self.modeVar.set("read")  # 设置默认值为READ模式
        self.read_mode = True

        self.txfuc_pointer = lambda a: print(f"发送指令{a}")
        self.valueModeChangeFunc = lambda a: print(f"当前读取状态为{a}")
        self.modeChangeFunc = lambda a: print(f"状态为{a}")

        self.textMode = tk.Label(self.frame, text='设定工作模式:')
        self.textFormat = tk.Label(self.frame, text='设定传输格式:')
        self.combobox_format = ttk.Combobox(self.frame, values=self.formatList, state='readonly', width=40)
        self.TXButton = tk.Button(self.frame, text="向下位机发送数据", command=self.TXfunc, width=30)

        self.readButton = tk.Radiobutton(self.frame, text="READ", variable=self.modeVar, value="read",
                                         command=self.toggle_controls)
        self.writeButton = tk.Radiobutton(self.frame, text="WRITE", variable=self.modeVar, value="write",
                                          command=self.toggle_controls)

        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.combobox_format.xview)
        self.combobox_format.configure(xscrollcommand=self.scrollbar.set)
        

        self.toggle_controls()

        self.textMode.grid(row=0, column=0, pady=3)
        self.readButton.grid(row=0, column=1, pady=3)
        self.writeButton.grid(row=0, column=2, pady=3)

        self.textFormat.grid(row=1, column=0)
        self.combobox_format.grid(row=1, column=1, columnspan=2)
        self.scrollbar.grid(row=2, column=1, columnspan=2, sticky="we")
        self.TXButton.grid(row=3, column=1, columnspan=2, pady=3)

        pass

    def get_radio_state(self):
        """获取单选框的状态"""
        return self.modeVar.get()

    def set_radio_options(self, formatList):
        """设定单选框的选项"""
        self.formatList = formatList
        self.combobox_format['values'] = self.formatList
        self.combobox_format.set('')

    def TXfunc(self):
        try:
            cmd = self.get_cmd()
            if cmd[:3]=='cmd' and int(cmd[3:])<len(self.formatList):
                print(cmd[:3],int(cmd[3:]))
                self.txfuc_pointer(cmd)
            else:
                print("error",cmd[:3],int(cmd[3:]))
        except:
            messagebox.showerror('警告', '请选择发送指令！')

    def setTXfuc(self, txfuc):
        self.txfuc_pointer = txfuc

    def toggle_controls(self):
        """切换控制按钮和组合框的状态"""
        mode = self.modeVar.get()
        if mode == "read":
            self.combobox_format.config(state='disabled')
            self.TXButton.config(state='disabled')
            self.read_mode = True
        else:  # mode == "write"
            self.combobox_format.config(state='readonly')
            self.TXButton.config(state='normal')
            self.read_mode = False
        self.valueModeChangeFunc(self.read_mode)
        self.modeChangeFunc(self.read_mode)

    def get_cmd(self):
        s = self.combobox_format.get()
        return s[:s.find(':')]


class SerialPortSelector:
    def __init__(self, root):
        self.serial_ports = []
        self.baud_rates = ['9600', '19200', '38400', '57600', '115200']
        self.frame = tk.Frame(root, padx=10, pady=10)

        self.serialSTA = False
        self.serial_name = None
        self.serial_baudrate = 115200

        self.var = tk.StringVar(self.frame)
        self.var.set("串口状态 : 关闭  (点击启动)")
        self.serialCRTL_funcpointer = lambda a: print(f"串口状态:{a}")

        self.scanCom_pointer = lambda: print('即将扫描串口')

        self.label_serial = tk.Label(self.frame, text="选取串口")
        self.label_serial.grid(row=0, column=0, pady=3)

        self.combobox_serial = ttk.Combobox(self.frame, values=self.serial_ports, state='readonly')
        self.combobox_serial.grid(row=0, column=1, sticky="we", pady=3)

        self.label_baud = tk.Label(self.frame, text="波特率")
        self.label_baud.grid(row=1, column=0, pady=3)

        self.combobox_baud = ttk.Combobox(self.frame, values=self.baud_rates, state='readonly')
        self.combobox_baud.grid(row=1, column=1, sticky="e", pady=3)

        self.button = tk.Button(self.frame, text='扫描串口', command=self.scanCom)
        self.button.grid(row=2, column=0, sticky="ew", pady=3)

        self.startButton = tk.Button(self.frame, textvariable=self.var, command=self.serialCTRL)
        self.startButton.grid(row=2, column=1, sticky="ew", pady=3)

    def scanCom(self):
        self.serial_ports = self.scanCom_pointer()
        self.combobox_serial['values'] = self.serial_ports

    def setScanComFunc(self, fuc):
        self.scanCom_pointer = fuc
        self.scanCom()

    def getSerialConfigure(self):
        self.serial_name = self.combobox_serial.get()
        self.serial_baudrate = int(self.combobox_baud.get())

    def serialCTRL(self):
        self.serialSTA = not self.serialSTA
        self.serialCRTL_funcpointer(self.serialSTA)
        if self.serialSTA:
            self.var.set("串口状态 : 开启  (点击关闭)")
        else:
            self.var.set("串口状态 : 关闭  (点击开启)")
        pass


class PlotterMoudle:
    def __init__(self, root):
        self.pointNum = 1
        self.x_axis = ['__TS']
        self.y_axis = []
        self.plotterSTA = False

        self.getAxisFucPointer = self.getAxisDefault
        self.shutdown = lambda: print("终止画图")

        self.frame = tk.Frame(root, padx=10, pady=10)
        self.drawFunc = lambda: print(f"数据点数量为{self.pointNum}")
        self.pointNumText = tk.Label(self.frame, text='设置采样点数')
        self.pointNumEntry = tk.Entry(self.frame, width=8)
        self.plotButton = tk.Button(self.frame, text='开始采样并画图', command=self.on_button_click, width=20)
        self.shutButton = tk.Button(self.frame, text='终止采样与画图', command=self.shutDrawing, width=20)

        self.pointNumText.grid(row=0, column=0, pady=3)
        self.pointNumEntry.grid(row=0, column=1, pady=3)
        self.plotButton.grid(row=1, columnspan=2, column=0, pady=3)
        self.shutButton.grid(row=2, columnspan=2, column=0, pady=3)

    def getPlotterInformation(self):
        return self.pointNum, self.x_axis[0], self.y_axis

    def getAxis(self):
        self.x_axis, self.y_axis = self.getAxisFucPointer()

    def getAxisDefault(self):
        print("获取x,y轴数据")
        return [], []

    def shutDrawing(self):
        self.plotterSTA = False
        self.shutdown()
        messagebox.showerror('画图器状态提示', '已终止采样与画图')

    def on_button_click(self):
        if not self.plotterSTA:
            try:
                self.pointNum = int(self.pointNumEntry.get())
            except:
                messagebox.showerror('画图器错误警告', '请输入整数！')
                return
            self.getAxis()
            if len(self.x_axis) < 1:
                self.x_axis = ['__TS', ]
            elif len(self.x_axis) > 1:
                messagebox.showerror('画图器错误警告', '请只选取1个x坐标！')
                return
            if len(self.y_axis) <= 0:
                messagebox.showerror('画图器错误警告', '请选择y坐标！')
                return

            if self.x_axis == ['__TS', ]:
                result = messagebox.askokcancel("绘图确认",
                                                f"采样点数量: {self.pointNum}\n" +
                                                f"x: 时间\n" +
                                                f"y: {', '.join(self.y_axis)}")
                if result:
                    self.drawFunc()

            else:
                result = messagebox.askokcancel("绘图确认",
                                                f"采样点数量:{self.pointNum}\n" +
                                                f"x:{self.x_axis[0]}\n" +
                                                f"y:{', '.join(self.y_axis)}")
                if result:
                    self.drawFunc()

        else:
            messagebox.showerror('画图器错误警告', '已在执行画图任务！')



class GUI:
    def __init__(self, key_value_dict, formatDict: dict):
        self.STA = True
        self.formatDict = formatDict
        self.formatList = []
        self.initFuc = lambda: print("窗口即将启动")
        self.distroyFuc = lambda: print("窗口已关闭")

        for key, value in self.formatDict.items():
            # 将键值对转换为字符串，并添加到列表中
            self.formatList.append(f"{key}:{str(value).replace('[', '').replace(']', '')}")

        self.root = tk.Tk()
        self.root.title("”沧澜“ —— 在线调试参数与绘图工具")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.serialPortSelector = SerialPortSelector(self.root)

        self.value_dict_table = ValueDictTable(self.root, key_value_dict)
        # self.button = tk.Button(self.root, text="Check Checked Values", command=self.print_checked_values)

        self.modeChooser = ModeChoser(self.root, self.formatList)
        self.plotModel = PlotterMoudle(self.root)

        # 显示模块之间相互调用的函数关系
        self.plotModel.getAxisFucPointer = self.value_dict_table.get_checked_values
        self.modeChooser.valueModeChangeFunc = self.value_dict_table.setValueReadMode

        # 摆放显示模块
        self.serialPortSelector.frame.grid(row=0, column=0)
        self.modeChooser.frame.grid(row=0, column=1)
        # self.button.grid(row=0, column=2)
        self.plotModel.frame.grid(row=0, column=2)
        self.value_dict_table.frame.grid(row=1, column=0, columnspan=3)

    # def print_checked_values(self):
    #     checked_x, checked_y = self.value_dict_table.get_checked_values()
    #     if len(checked_x) > 1:
    #         messagebox.showerror("Error", "选取了超过1个x坐标！")
    #     else:
    #         print(f"Checked 'x': {checked_x}")
    #         print(f"Checked 'y': {checked_y}")

    def run(self):
        self.initFuc()
        time.sleep(0.1)
        self.root.mainloop()

    def on_closing(self):
        self.distroyFuc()
        self.STA = False
        self.plotModel.plotterSTA = False
        time.sleep(0.2)
        self.root.destroy()


if __name__ == "__main__":
    # 示例字典
    example_dict = {
        "阿米娅": "Amiya",
        "逻各斯": "logos",
        "小火龙": "Little Dragon",
        "远山": "Yu Shan",
        "角峰": "Corner Peak",
        "阻挡者": "Blocker",
        "因陀罗": "Indra",
        "天火": "Sky Fire",
        "清道夫": "Scavenger",
        "凛冬": "Lynn",
        "红": "Crimson",
        "蓝毒": "Blue Poison",
        "白金": "Platinum",
        "陨星": "Meteor",
        "灰喉": "Grey Throat",
        "慕斯": "Mousse",
        "守林人": "Forest Guardian",
        "陨石": "Asteroid",
        "霞": "Glaze",
        "梅尔": "Mel",
        "极境": "Polar Region",
        "风笛": "Bagpipe"
    }

    app = GUI(example_dict, example_dict)
    app.run()
