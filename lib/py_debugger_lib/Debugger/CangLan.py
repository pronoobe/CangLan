try:
    import ustruct as struct
except ModuleNotFoundError:
    import struct


class VarManager(object):
    def __init__(self, dataDict: dict):
        self.string_dict = dict()
        self.var_dict = dataDict

    def setvar(self, name, value):
        if type(value) != str:
            self.var_dict[name] = value
        else:
            self.string_dict[name] = value

        # setattr(self, name, value)

    def getvar(self, name):
        try:
            return self.var_dict[name]
        except KeyError:
            try:
                return self.string_dict[name]
            except:
                return None
        # return getattr(self, name)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.getvar(item)

    def __setitem__(self, key, value):
        if isinstance(key, str):
            self.setvar(key, value)

    def __lshift__(self, other):
        if isinstance(other, dict):
            self.var_dict = other
        return self


class CangLan_MicroDsp(VarManager):
    def __init__(self, dataDict={}):
        """
        @+FORMAT+LEN+=+BUF+CRC+#
        """
        super().__init__(dataDict)
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
        self.crc_num = 0

    def add_new_command(self, name, command_u8, command_type, var_name):
        """
        添加新的命令
        例如:add_new_command('com1', 0b00000001, (int, float, int), ('a', 'b', 'c'))
        """
        self.command_form_dict.update({command_u8: command_type})
        self.name_command_dict.update({name: command_u8})
        self.command_name_dict.update({command_u8: name})
        self.command_var_dict.update({name: var_name})
        for i in range(len(var_name)):
            if command_type[i] == str:
                self.setvar(var_name[i], 'null')
            elif command_type[i] == int:
                self.setvar(var_name[i], 0)
            elif command_type[i] == float:
                self.setvar(var_name[i], 0.0)

    @staticmethod
    def crc(data) -> bytes:
        res_sum = 0
        for i in data:
            res_sum += int(i)
        return (res_sum % 256).to_bytes(1, 'big')

    def pack_data(self, data_type_name, data=None):
        # 发送数据，例如发送名字为‘com1’，格式为(int, float, int)的数据时
        # 应该发送：pack_data('com1', (20, 30.3, 2))

        if data is None:
            data = list()
            for var in self.command_var_dict[data_type_name]:
                data.append(self.getvar(var))

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
            data_pack) + b'#' + b'\r\n'  # @+FORMAT+LEN+=+BUF+CRC+#
        return res

    def unpack_data(self, data):
        data_list = self.split_many_data(data)
        # print(data_list)
        final_res = []
        for data in data_list:
            if len(data) <= 5:
                continue
            res = []
            if chr(data[0]) != '@' or chr(data[-1]) != '#':
                # print("数据{}接收出现问题".format(data))
                continue
            data_real = data[1:-1]
            data_info = data_real[:self.info_len]
            data_content = data_real[self.eq_loc:-1]  # 跳过等号和CRC
            try:
                data_form, data_len = self.command_form_dict[data_info[0]], data_info[1]
            except:
                # print(data_info[0], data_info[1])
                continue
            data_crc = data_real[3 + data_len:]  # 取crc
            if data_crc != self.crc(data_content):
                print("数据 {} 未能成功进行crc校验".format(data_content))
                self.crc_num += 1
                continue

            # 获取长度和格式 (例如0b00000001对应(int, int, float))

            data_name = self.command_name_dict[data_info[0]]

            for data_type in data_form:
                if data_type != str:  # 非字符串接收
                    now_data_len = self.type_len[data_type]
                    now_data_content = data_content[:now_data_len]
                    struct_type = self.type_dict_recv[data_type]
                    now_data = struct.unpack(struct_type, now_data_content)[0]
                    data_content = data_content[now_data_len:]
                    if isinstance(now_data, float):
                        now_data = round(now_data, 2)
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
            ...
            # print('命令 {command_name} 没有对应的绑定变量'.format(command_name))

    @staticmethod
    def split_many_data(data):
        try:
            data_list = data.split(b'\r\n')

            return data_list
        except:
            return b""


if __name__ == '__main__':
    formatter = CangLan_MicroDsp()

    formatter.add_new_command('cmd0', 0b0, (int, int, int,), ['M1_CCR1', 'M1_CCR2', 'M1_CCR3', ])
    formatter.add_new_command('cmd1', 0b1, (int, int, int,), ['M2_CCR1', 'M2_CCR2', 'M2_CCR3', ])
    formatter.add_new_command('cmd2', 0b10, (float, float, float,), ['M1_moment', 'M1_angle', 'M1_speed', ])
    formatter.add_new_command('cmd3', 0b11, (float, float, float,), ['M2_moment', 'M2_angle', 'M2_speed', ])
    formatter.add_new_command('cmd4', 0b100, (float, float, float, float, float, float,),
                              ['M1_moment', 'M1_angle', 'M1_speed', 'M2_moment', 'M2_angle', 'M2_speed', ])
    formatter.add_new_command('cmd5', 0b101, (float, float, float, float, float, float, float, float,),
                              ['M1_Iq_Kp', 'M1_Iq_Ki', 'M1_Id_Kp', 'M1_Id_Ki', 'M1_v_Kp', 'M1_v_Ki', 'M1_p_Kp',
                               'M1_p_Ki', ])
    formatter.add_new_command('cmd6', 0b110, (float, float, float, float, float, float, float, float,),
                              ['M2_Iq_Kp', 'M2_Iq_Ki', 'M2_Id_Kp', 'M2_Id_Ki', 'M2_v_Kp', 'M2_v_Ki', 'M2_p_Kp',
                               'M2_p_Ki', ])
    formatter.add_new_command('cmd7', 0b111, (float, float, float, float,),
                              ['M1_U_amp', 'M1_U_phi', 'M2_U_amp', 'M2_U_phi', ])
    formatter.add_new_command('cmd8', 0b1000, (float, float, float, float,), ['M1_Ia', 'M1_Ib', 'M2_Ia', 'M2_Ib', ])
