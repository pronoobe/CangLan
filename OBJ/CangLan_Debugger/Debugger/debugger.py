from Debugger.dataModel import *
from Debugger.serialTool import *
from Debugger.gui import *
from Debugger.CangLan import *

import threading, time


class CangLan_Debugger:
    def __init__(self, formatter: CangLan_MicroDsp):
        self.formatter = formatter
        self.db = DataBase(formatter.var_dict)
        self.sm = serialModule('COM1', 115200)
        self.gui = GUI(formatter.var_dict, formatter.command_var_dict)

        # 重写gui中的部分方法
        self.gui.serialPortSelector.setScanComFunc(scanSerialCom)
        self.gui.initFuc = self.app_init_function
        self.gui.plotModel.drawFunc = self.start_plotterThread
        self.gui.serialPortSelector.serialCRTL_funcpointer = self.serialCTRL
        self.gui.modeChooser.txfuc_pointer =self.write_new_value
        self.gui.value_dict_table.loadjson_function = self.db.read_json_to_dict
        self.gui.value_dict_table.exportjson_function = self.db.export_dict_to_json

        # 读取串口的子线程
        self.serial_ReadComThread = threading.Thread(target=self.serial_ReadComThreadFunc, args=(1,))
        self.serial_ReadComThread.daemon = True

        # 刷新数值的子线程
        self.valueRefresh_Thread = threading.Thread(target=self.valueRefresh_ThreadFuc, args=(1,))
        self.valueRefresh_Thread.daemon = True

        # for key,value in formatter.var_dict.items():
        #     print(f"{key}:{type(value)}")

    # 重置串口模块
    def resetSerialModel(self):
        self.gui.serialPortSelector.getSerialConfigure()
        if self.sm.port != self.gui.serialPortSelector.serial_name or self.sm.baudrate != self.gui.serialPortSelector.serial_baudrate:
            self.sm.resetSerial(self.gui.serialPortSelector.serial_name, self.gui.serialPortSelector.serial_baudrate)

    # 串口状态修正
    def serialCTRL(self, *args):
        if self.gui.serialPortSelector.serialSTA:
            self.resetSerialModel()
            self.sm.open()
        else:
            self.sm.close()

    # 读取串口的子线程执行的函数
    def serial_ReadComThreadFunc(self, *args):
        while self.gui.STA:
            # if not app.plotModel.plotterSTA:
            #     sm.readCom()
            #     # print('正在读取')
            # time.sleep(0.005)
            self.sm.readCom()
            time.sleep(0.005)

    # 画图器的子线程执行的函数
    def plotter_DrawConvas(self, *args):
        self.gui.plotModel.plotterSTA = True
        num, x, y = self.gui.plotModel.getPlotterInformation()
        self.db.reset_input(num, x, y)
        self.sm.clear_rxBuffer()
        self.sm.ser.flushInput()
        while self.gui.plotModel.plotterSTA:
            self.sm.readCom()
            if self.sm.rxBufferLen > 0:
                data = self.sm.readline()
                if data is not None:
                    self.formatter.unpack_data(data[0])
                    if self.db.step_input(data[1]):
                        pass
                        # print(data)
                    else:
                        self.gui.plotModel.plotterSTA = False
                        self.db.drawCanvas()
                        break
                else:
                    print('None')
        print("绘图结束")

    # 刷新数值的子线程的函数
    def valueRefresh_ThreadFuc(self, *args):
        while self.gui.STA:
            if self.gui.modeChooser.read_mode and not self.gui.plotModel.plotterSTA:
                if self.sm.rxBufferLen > 0:
                    data = self.sm.readNewline()
                    if data is not None:
                        self.formatter.unpack_data(data[0])
                        self.gui.value_dict_table.refreshAllvalue()
                        self.sm.clear_rxBuffer()
            time.sleep(0.05)
            # print('正在读取')

    # 画图函数
    def start_plotterThread(self):
        self.drawConvasThread = threading.Thread(target=self.plotter_DrawConvas, args=(1,))
        self.drawConvasThread.daemon = True
        self.drawConvasThread.start()

    # 初始化时执行的一些功能
    def app_init_function(self):
        self.sm.close()
        self.valueRefresh_Thread.start()
        self.serial_ReadComThread.start()

    # 根据选定的指令设置新数据
    def write_new_value(self, cmd:str):
        var_list = self.formatter.command_var_dict[cmd]
        for var in var_list:
            new_value = self.gui.value_dict_table.blockDict[var].getvalue()
            print(f"{var} = {new_value}")
        data = self.formatter.pack_data(cmd)
        print(f"发送指令 {cmd} : {data}")
        self.sm.write(data)

    def run(self):
        self.gui.run()


