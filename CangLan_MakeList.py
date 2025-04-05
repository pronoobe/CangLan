import os
import shutil

class Formatter:
    def __init__(self,name:str, variable_list: list, format_list: list):
        self.name = name
        self.HyperName = self.name.upper()
        self.variable_list = variable_list
        self.format_list = format_list
        self.variable_num = len(variable_list)
        self.format_num = len(format_list)
        self.variable_dict_byType = dict()
        self.namelist = list()
        self.Print()

        self.variable_dict_byType['int']=list()
        self.variable_dict_byType['float']=list()
        self.variable_dict_byType['string']=list()

        for v in variable_list:
            self.variable_dict_byType[v[0]].append(v[1])
            self.namelist.append(str(v[1]))

        print(self.variable_dict_byType)

    def Print(self):
        print(f"格式化对象名称:{self.name}----{self.HyperName}")
        print(f"变量列表({self.variable_num}):{self.variable_list}")
        print(f"格式列表({self.format_num}):{self.format_list}")
        print('')

    def search_v(self,v_name):
        v=None
        for v in range(len(self.variable_list)):
            # print(f"|{v_name}<>{self.variable_list[v][1]}|")
            if  v_name == self.variable_list[v][1]:
                break
        return v

    def output_HeaderFile(self):
        variable_string = '{' + str(self.namelist)[1:-1] + '}'
        HeaderFile_str = f'''
/****************************** FORMATTER: {self.name} ******************************************/\n
        \n'''
        if len(self.variable_dict_byType['int'])>0:
            _variable_string = str(self.variable_dict_byType['int'])[1:-1].replace('\'','')
            HeaderFile_str += f"//extern int {_variable_string};\n"
        if len(self.variable_dict_byType['float'])>0:
            _variable_string = str(self.variable_dict_byType['float'])[1:-1].replace('\'','')
            HeaderFile_str += f"//extern float {_variable_string};\n"
        
        for v in self.variable_dict_byType["string"]:
            HeaderFile_str += f"//extern char {v}[100];\n"

        HeaderFile_str += f'''
//extern char *{self.name}_variable_name_list[{len(self.variable_list)}];

#define CANGLAN_{self.HyperName}_FORMAT_NUM {self.format_num}
#define CANGLAN_{self.HyperName}_VARIABLE_NUM {self.variable_num}

extern CANGLAN_FORMATTER {self.name};
extern CANGLAN_FORMAT {self.name}_formatList[CANGLAN_{self.HyperName}_FORMAT_NUM];
extern CANGLAN_VARIABLE {self.name}_vpList[CANGLAN_{self.HyperName}_VARIABLE_NUM];


'''

        print(HeaderFile_str)

        return HeaderFile_str


    def output_C_format_array(self):
        _string = ""
        num=0
        for f in self.format_list:
            _string += f"u8 CangLan_{self.name}_format{num}[{len(f.split(','))}] = "+'{'
            f_buf = f.replace('[','').replace(']','').replace(' ','').split(',')
            for v in f_buf:
                _string+=f"{self.search_v(v)},"
            _string = _string[0:-1] + '};\n'
            num+=1

        # print(_string)
        return _string

    def output_C_vpList(self):
        _string = ""
        _string += f"CANGLAN_VARIABLE {self.name}_vpList[CANGLAN_{self.HyperName}_VARIABLE_NUM] = "+'{'
        for v in self.variable_list:
            if v[0]=='int':
                _string+='{'+f"0,&{v[1]}"+'},'
            elif v[0]=='float':
                _string+='{'+f"1,&{v[1]}"+'},'
            elif v[0]=='string':
                _string+='{'+f"2,{v[1]}"+'},'
            else:
                print(f'v={v}')
        _string = _string[0:-1]
        _string+='};\n'
        # print(_string)
        return _string

    def output_C_formatList(self):
        _string = f"CANGLAN_FORMAT {self.name}_formatList[CANGLAN_{self.HyperName}_FORMAT_NUM] ="+"{\n"
        for i in range(len(self.format_list)):
            _string += '\t{'+f"{len(self.format_list[i].split(','))},CangLan_{self.name}_format{i}"+'},\n'
        _string = _string[0:-2]
        _string+='\n};\n'

        # print(_string)
        return _string

    def output_C_variable(self):
        # variable_string = '{' + str(self.namelist)[1:-1] + '}'
        # _string += f"//char {self.name}_name_list[{len(self.variable_list)}][20] = {variable_string};\n"
        _string = ""
        for i in range(len(self.variable_list)):
            variable_name_str =  '\"' + self.namelist[i] +  '\"'
            _string += f"//char {self.name}_variable_name{i}[] = {variable_name_str};\n"
        _string += f"\n//char* {self.name}_variable_name_list[{len(self.variable_list)}]" + "={\n"
        for i in range(len(self.variable_list)):
            _string += f"//\t{self.name}_variable_name{i},\n"
        _string = _string[0:-2] + '\n//};\n\n'

        if len(self.variable_dict_byType['int'])>0:
            _variable_string = str(self.variable_dict_byType['int'])[1:-1].replace('\'','')
            _string += f"//int {_variable_string};\n"
        if len(self.variable_dict_byType['float'])>0:
            _variable_string = str(self.variable_dict_byType['float'])[1:-1].replace('\'','')
            _string += f"//float {_variable_string};\n"
        if len(self.variable_dict_byType['string'])>0:
            # _variable_string = str(self.variable_dict_byType['string'])[1:-1].replace('\'','')
            # _string += f"//char {_variable_string};\n"
            for v in self.variable_dict_byType["string"]:
                _string += f"//char {v}[100];\n"

        return _string

    def output_C_formatter(self):
        _string = ""
        _string += f"CANGLAN_FORMATTER {self.name }="+'{'+f"{self.format_num},{self.variable_num},{self.name}_vpList,{self.name}_formatList"+'};\n'
        # print(_string)
        return _string

    def output_C_File(self):
        _file = f"/****************************** FORMATTER: {self.name} ******************************************/\n\n"
        _file+=self.output_C_variable()+'\n'
        _file+=self.output_C_format_array()+'\n'
        _file+=self.output_C_vpList()+'\n'
        _file+=self.output_C_formatList()+'\n'
        _file+=self.output_C_formatter()+'\n'

        return _file

    def output_py_typelist_str(self,format_array):
        typelist = list()
        for f_name in format_array:
            # print(f_name)
            typelist.append(self.variable_list[self.search_v(f_name)][0])
        typelist_str = str(typelist)[0:-1]+',)'
        return typelist_str.replace('[','(').replace(']',')').replace('string','str').replace('\'','')

    def output_py_File(self):
        _string = f"    {self.name} = CangLan_MicroDsp()\n\n"
        num = 0
        for f in self.format_list:
            f=f.replace('[','').replace(']','').split(',')
            variablelist_str = str(f)[0:-1]+',]'
            _string += f"    {self.name}.add_new_command('cmd{num}', {str(bin(num))}, {self.output_py_typelist_str(f)}, {variablelist_str})\n"
            num+=1
        _string += "\n"
        return _string

    def ouput_py_debugger_File(self):
        _string = f"from Debugger import *\n\n{self.name} = CangLan_MicroDsp()\n\n"
        num = 0
        for f in self.format_list:
            f=f.replace('[','').replace(']','').split(',')
            variablelist_str = str(f)[0:-1]+',]'
            _string += f"{self.name}.add_new_command('cmd{num}', {str(bin(num))}, {self.output_py_typelist_str(f)}, {variablelist_str})\n"
            num+=1
        _string += "\n"
        _string +="""
if __name__ == "__main__":
    debugger = CangLan_Debugger(formatter)
    debugger.run()
        """
        return _string

class CangLan():
    def __init__(self):
        self.include_path = list()
        self.import_path = list()
        self.formatter_list = list()
        shutil.rmtree("OBJ")
        self.load()
    def Print(self):
        for f in self.formatter_list:
            f.Print()

    def load(self):

        formatter_name =[]
        variable_list = []
        format_list = []
        endlist=[]
        include_line = 0
        include_list = []
        inc_over_line = 0

        with open('CangLan_List.txt') as f:
            s = f.readlines()
            for i in range(len(s)):
                if 'include' in s[i]:
                    include_line = i
                elif 'INC_OVER' in s[i]:
                    inc_over_line = i
                elif 'NAME'  in s[i]:
                    formatter_name.append(i)
                elif 'VARIABLE'  in s[i]:
                    variable_list.append(i)
                elif 'FORMAT'  in s[i]:
                    format_list.append(i)
                elif 'END'  in s[i]:
                    endlist.append(i)
            # print(formatter_name)
            # print(variable_list)
            # print(format_list)
            # print(endlist)

        for l in range(include_line+1,inc_over_line):
            s_buf = s[l].replace('\t','')
            s_buf = s_buf.replace('\n','')
            s_buf = s_buf.replace(' ','')
            if len(s_buf)!=0:
                self.include_path.append(s_buf)
        print(f"include_path:{self.include_path}")

        for n in range(len(formatter_name)):
            s_buf = s[formatter_name[n]].replace('\t','')
            s_buf = s_buf.replace('\n','')
            s_buf = s_buf.replace(' ','')
            name = s_buf.split(':')[1]
            v_list = []
            f_list = []

            for l in range(variable_list[n]+1,format_list[n]):
                s_buf = s[l].replace('\t','')
                s_buf = s_buf.replace('\n','')
                s_buf = s_buf.replace(' ','')
                if len(s_buf)!=0:
                    v_list.append(s_buf.split(':'))

            for l in range(format_list[n]+1,endlist[n]):
                s_buf = s[l].replace('\t','')
                s_buf = s_buf.replace('\n','')
                s_buf = s_buf.replace(' ','')
                if len(s_buf)!=0:
                    f_list.append(s_buf)
            self.formatter_list.append(Formatter(name,v_list,f_list))

    def output_C_folder(self):
        if not os.path.exists("OBJ"):
            os.mkdir("OBJ")
        if not os.path.exists("OBJ/CangLan_C"):
            os.mkdir("OBJ/CangLan_C")

        #复制工具文件
        with open("lib/clib/CangLan_tool.c", 'r') as f_r:
            with open("OBJ/CangLan_C/CangLan_tool.c",'w+') as f_w:
                f_w.write(f_r.read())
        with open("lib/clib/CangLan_tool.h",'r') as f_r:
            with open("OBJ/CangLan_C/CangLan_tool.h",'w+') as f_w:
                f_w.write(f_r.read())

        #写CangLan.h文件
        with open("OBJ/CangLan_C/CangLan.h",'w+') as f_w:
            _string = """#ifndef __CANGLAN_H
#define __CANGLAN_H

#include "CangLan_tool.h"
"""
            for include_path in self.include_path:
                _string+=f"#include \"{include_path}\"\n"

            _string+='\n\n'
            for formatter in self.formatter_list:
                _string += formatter.output_HeaderFile()

            _string+='\n#endif\n'
            
            f_w.write(_string+'\n')

        # 写CangLan.h文件
        with open("OBJ/CangLan_C/CangLan.c", 'w+') as f_w:
            _string = """#include "CangLan.h"
#include "CangLan_tool.h"

"""
            for formatter in self.formatter_list:
                _string += formatter.output_C_File()

            f_w.write(_string+'\n')

    def output_py_folder(self):
        if not os.path.exists("OBJ"):
            os.mkdir("OBJ")

        with open("OBJ/CangLan.py",'w+', encoding='utf-8') as f_w:
            _string = ""
            with open("lib/pylib/CangLan_tool.py", 'r', encoding='utf-8') as lib_f:
                _string += lib_f.read()
            _file = "if __name__ == '__main__':\n"
            for f in self.formatter_list:
                _file += f.output_py_File()

            f_w.write(_string+_file)
        print(_file)

    def output_py_debugger_folder(self):
        if not os.path.exists("OBJ"):
            os.mkdir("OBJ")
        if os.path.exists("OBJ/CangLan_Debugger"):
            shutil.rmtree("OBJ/CangLan_Debugger")
        src = "lib/py_debugger_lib"
        dst = "OBJ/CangLan_Debugger"
        shutil.copytree(src, dst)

        for formatter in self.formatter_list:
            with open(f"OBJ/CangLan_Debugger/{formatter.name}_debugger.py", 'w+', encoding='utf-8') as f:
                print(f"{formatter.name}_debugger.py")
                f.write(formatter.ouput_py_debugger_File())


if __name__ == '__main__':
    cl = CangLan()
    print("\n***************************** C语言配置文件 ******************************\n")
    cl.output_C_folder()
    print("\n**************************** Python配置文件 *****************************\n")
    cl.output_py_folder()
    print("\n*************************** Debugger 配置文件 ***************************\n")
    cl.output_py_debugger_folder()
    print("\n\n************************************************************************\n\n\n")

    input("配置文件生成完毕！输入任意文字退出脚本")

    pass


