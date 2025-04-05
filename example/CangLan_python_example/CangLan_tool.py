import re
import struct

COM1 = []


class CangLan_VarManager(object):
    def __init__(self):
        ...

    def setvar(self, name, value):
        setattr(self, name, value)

    def getvar(self, name):
        return getattr(self, name)


class CangLan_MicroDsp(CangLan_VarManager):
    def __init__(self):
        """
        @+FORMAT+LEN+=+BUF+CRC+#
        """
        super().__init__()
        self.command_form_dict = {}  # 命令对应的类型{命令:类型（比如4个int,两个float）}，命令是u8 eg:{0b00000001:(int, int, float)}
        self.command_function_dict = {}  # 收到命令对应的回调函数的字典（例如收到0b00000001命令执行func1）
        self.name_command_dict = {}  # 名字对应的命令 eg:{'c1':0b00000001}
        self.command_name_dict = {}  # 名字对应的命令 eg:{0b00000001:'c1'}
        self.start = b"@"
        self.end = b"#"
        self.char = 1  # 字符类型
        self.type_dict_send = {float: '<f', int: '<i', self.char: '<B'}  # 发送和接收分别采用大端和小端
        self.type_dict_recv = {float: '<f', int: '<i', self.char: '<B'}
        self.type_len = {float: 4, int: 4, self.char: 1}
        self.eq = b'='
        self.eq_loc = 3
        self.info_len = 2
        self.command_var_dict = {}

    def add_new_command(self, name, command_u8, command_type, var_name):
        """
        添加新的命令
        例如:add_new_command('com1', 0b00000001, (int, float, int), ('a', 'b', 'c'))
        """
        self.command_form_dict.update({command_u8: command_type})
        self.name_command_dict.update({name: command_u8})
        self.command_name_dict.update({command_u8: name})
        self.command_var_dict.update({name: var_name})
        for name in var_name:
            self.setvar(name, 0)

    @staticmethod
    def crc(data) -> bytes:
        res_sum = 0
        for i in data:
            res_sum += int(i)
        return (res_sum % 256).to_bytes(1, 'big')

    def pack_data(self, data_type_name, data):
        # 发送数据，例如发送名字为‘com1’，格式为(int, float, int)的数据时
        # 应该发送：pack_data('com1', (20, 30.3, 2))
        data_pack = b""
        data_type = self.name_command_dict[data_type_name]
        command_pack = data_type.to_bytes(1, 'big')

        data_forms = self.command_form_dict[data_type]
        for i, form in enumerate(data_forms):
            if form != str:
                struct_form = self.type_dict_send[form]
                struct_data = struct.pack(struct_form, data[i])
                if struct_form == '>B':
                    struct_data += b'\0'
                data_pack += struct_data
            else:
                for char in data[i]:
                    struct_form = '>B'
                    struct_data = struct.pack(struct_form, ord(char))
                    data_pack += struct_data
                data_pack += b'\0'
        buf_len = len(data_pack)
        res = self.start + command_pack + buf_len.to_bytes(1, 'big') + self.eq + data_pack + self.crc(
            data_pack) + b'#'  # @+FORMAT+LEN+=+BUF+CRC+#
        return res

    def unpack_data(self, data):
        data_list = self.split_many_data(data)
        print(data_list)
        final_res = []
        for data in data_list:
            res = []
            if chr(data[0]) != '@' or chr(data[-1]) != '#':
                print(f"数据{data}接收出现问题")
                continue
            data_real = data[1:-1]
            data_info = data_real[:self.info_len]
            data_content = data_real[self.eq_loc:-1]  # 跳过等号和CRC
            # 获取长度和格式 (例如0b00000001对应(int, int, float))
            data_form, data_len = self.command_form_dict[data_info[0]], data_info[1]
            data_name = self.command_name_dict[data_info[0]]
            data_crc = data_real[3 + data_len:]  # 取crc
            if data_crc != self.crc(data_content):
                print(f"数据 {data_content} 未能成功进行crc校验")
                continue
            for data_type in data_form:
                if data_type != str:  # 非字符串接收
                    now_data_len = self.type_len[data_type]
                    now_data_content = data_content[:now_data_len]
                    struct_type = self.type_dict_recv[data_type]
                    now_data = struct.unpack(struct_type, now_data_content)[0]
                    data_content = data_content[now_data_len:]
                    if isinstance(now_data, float):
                        now_data = now_data.__round__(4)
                    res.append(now_data)
                else:  # 字符串接收
                    str_res = ""
                    while True:
                        now_data_len = 1
                        now_data_content = data_content[:now_data_len]
                        struct_type = '>B'
                        single_char = chr(struct.unpack(struct_type, now_data_content)[0])
                        if single_char == '\0':
                            data_content = data_content[now_data_len:]
                            break
                        str_res += single_char
                        data_content = data_content[now_data_len:]
                    res.append(str_res)
            final_res.append({data_name: res})
            self.change_var(self.command_name_dict[data_info[0]], res)
        return final_res

    def change_var(self, command_name, data):
        try:
            for i, name in enumerate(self.command_var_dict[command_name]):
                self.setvar(name, data[i])
        except KeyError:
            print(f'命令 {command_name} 没有对应的绑定变量')

    @staticmethod
    def split_many_data(data):
        data_list = data.split(b'#@')
        if len(data_list) == 2:
            data_list[1] = b'@' + data_list[1]
        if len(data_list) > 2:
            for i in range(1, len(data_list) - 1):
                data_list[i] = b'@' + data_list[i] + b'#'
        if chr(data_list[len(data_list) - 1][-1]) == '#' and chr(data_list[len(data_list) - 1][0]) != '@':
            data_list[len(data_list) - 1] = b'@' + data_list[len(data_list) - 1]
        if chr(data_list[0][0]) == '@' and chr(data_list[0][-1]) != '#':
            data_list[0] = data_list[0] + b'#'


        return data_list


if __name__ == '__main__':
    # md = CangLan_MicroDsp()
    # var_manager = CangLan_VarManager()
    # md.add_new_command('com1', 0b00000001, (int, float, str), ['a1', 'b1', 'c1'])
    # md.add_new_command('com2', 0b00000010, (int, float, str, int), ['a2', 'b2', 'c2', 'd2'])
    # md.add_new_command('com3', 0b00000011, (float, float, str, str), ['a3', 'b3', 'c3', 'd3'])
    # md.add_new_command('com4', 0b00000100, (str, str), ['a4', 'b4'])
    # md.add_new_command('com5', 0b00000101, (int, int, int), ['a5', 'b5', 'c5'])
    # md.add_new_command('com6', 0b00000110, (str, float, float, str), ['a6', 'b6', 'c6', 'd6'])
    # md.add_new_command('com7', 0b00000111, (int, float, str), ['a7', 'b7', 'c7'])
    # # md.pack_data()
    # data1 = md.pack_data('com1', (20, -30.2, 'hello world'))
    # data2 = md.pack_data('com2', (-210, 430.22, '1hello world2', 6))
    # data3 = md.pack_data('com3', (114.514, 14.514, "awawawawa", "miku"))
    # data4 = md.pack_data('com4', ('hello world1', 'hello world2'))
    # data5 = md.pack_data('com5', (1003201, 320, -124))
    # data6 = md.pack_data('com6', ('hello world', 3.3, 4.3, 'a'))
    # data7 = md.pack_data('com7', (123, 123.456, "I'm HuangHe"))
    # print("编码后的数据")
    # for i in data4:
    #     print(i, end=" ")
    # print("\n", data7)
    # print("解码后的数据")
    # # data2 = b'@\x03\x17=B\xe3\x07+Ah9Xawawawawa\x00miku\x00\n#'
    # print(md.unpack_data(data4 + data5 + data6 + data4[:-5] + data7 + data2))
    # # 变量中存的数据
    #
    # # print("变量中存的数据")
    # # print(md.getvar("a3"))
    # # print(md.getvar("b3"))
    # # print(md.getvar("d3"))
    # # print(md.getvar("c5"))
    a = 0b00000000
    print(bin(a))
    a+=1
    print(str(bin(a)))
    a+=1
    print(bin(a))
    a+=1
    print(bin(a))

