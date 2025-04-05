import serial, time


def scanSerialCom():
    import serial.tools.list_ports
    import re
    ports = list(serial.tools.list_ports.comports())
    r = re.compile(r'COM\d{1,3}')
    s = []
    for i in ports:
        s.append(re.match(r, str(ports[0])).group())
    return s


class serialModule:
    def __init__(self, port: str, baudrate: int):
        self.port = port
        self.baudrate = baudrate
        self.rxBufferLen = 0
        self.serialSTA = False
        print(f'初始化串口{port},波特率为{baudrate}')
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
            self.initSTA = True
        except:
            self.ser = None
            self.initSTA = False
        self.rxBuffer = list()

        self.close()

    def resetSerial(self, port: str, baudrate: int):
        self.close()
        self.port = port
        self.baudrate = baudrate
        print(f'初始化串口{port},波特率为{baudrate}')
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
            self.initSTA = True
        except:
            self.ser = None
            self.initSTA = False
        self.close()

    def open(self):
        if self.initSTA:
            self.clear_rxBuffer()
            self.ser.open()
            time.sleep(0.2)
            self.serialSTA = True

    def close(self):
        if self.initSTA:
            self.serialSTA = False
            time.sleep(0.2)
            self.ser.close()
            self.clear_rxBuffer()

    def readCom(self):
        if self.initSTA:
            if self.serialSTA:
                if self.ser.in_waiting:
                    self.rxBuffer.append((self.ser.readline().rstrip(), time.time()))
                    self.rxBufferLen += 1

    def readline(self):
        if self.initSTA:
            if self.rxBufferLen > 0:
                data = self.rxBuffer.pop(0)
                self.rxBufferLen -= 1
                return data
            else:
                return None

    def readNewline(self):
        if self.initSTA:
            if self.rxBufferLen > 0:
                data = self.rxBuffer.pop()
                self.rxBufferLen = 1
                return data
            else:
                return None
        pass

    def clear_rxBuffer(self):
        if self.initSTA:
            self.rxBuffer = []
            self.rxBufferLen = 0

    def write(self, data):
        if self.initSTA:
            self.ser.write(data)


def scanSerial():
    import serial.tools.list_ports
    import re
    ports = list(serial.tools.list_ports.comports())
    r = re.compile(r'COM\d{1,3}')
    s = []
    for i in ports:
        s.append(re.match(r, str(ports[0])).group())
    return s


if __name__ == "__main__":
    print(scanSerialCom())
    sm = serialModule(scanSerialCom()[0], 115200)
    while True:
        sm.readCom()
        if sm.rxBufferLen > 0:
            print(sm.readline())
