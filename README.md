# README

## 一、简介

### 1.概述

为了方便电子设备竞赛期间多个设备的通信与控制，设计如下通信系统。

考虑到绝大多数情况下，发送时通信传输的数据读取自变量，收到格式化的字节串后解析除的数据也将存入变量中，因此本通信系统将数据发送/接收与数据读写的过程合在一起，减少配置代码，提高开发效率。

### 2.格式说明

通信的字节串格式如下：

<mark>'@' + 格式编号 + 数据段长度 + '=' + 数据段 + 数据段CRC校验值 + '#'</mark>

 其中@,=.#三个符号作为关键字方便快速校验

同时，格式也有“数据编译格式”的意思，包含本次传输的变量名称、顺序的信息。发送/接收数据时按照格式编号指定的方式编译/解析数据与变量。发送时只需传入格式编号，即可自动编译待发送的字节串。接收时，可根据接收到的字节串中的格式编号信息自动解析内容。

### 3.支持的数据类型

通信系统支持三种数据类型的收发与解析：

- 有符号整数：长度为4字节，类型记作int

- 有符号单精度浮点数：长度为4字节，类型记作float

- 无符号字符数组：长度为n字节，类型记作string

## 二、使用方法

为了开发，设置了自动工具生成配置文件。

使用如下步骤：

1. 配置 **CangLan_List.txt**，配置方法在下文介绍。

2. 运行 **CangLan_MakeList.py** ，在 **OBJ** 文件夹生成C，python两种语言的配置文件。

3. 将配置文件复制到工程文件夹中，导入添加文件路径。

4. 在需要使用"沧澜"通信系统的文件中引入`"CangLan.h"`,即可调用API。

5. 对于python文件，再**OBJ** 文件中提取`CangLan.py`文件即可使用，配置的格式信息存储在了文件末尾。

### CangLan_List填写方法:

```c
include_path:
xxx.h
/*****************************************
在这里填写变量引用的.h文件，
例如：引用自variable.h,就在这里填写文件名即可
******************************************/
##INC_OVER
```

```c
NAME:name//formatter的名字
VARIABLE:
    []
/*****************************************
在这里填写引用的变量，按照 类型:变量名 的格式填写
例如：
int:_i
float:_f
string:str
******************************************/
FORMAT:
    []
/*****************************************
在这里填写每种格式的具体内容，填写格式为：[变量1,变量2,...]
例如：
[_i]
[_i,_f]
[_i,str]
[_f,str]
[_i,_f,str]
注意，不支持换行填写，每一种格式必须在一行内填写完成
******************************************/
##END
```

完整示例：

```c++
include_path:
    variable.h
##INC_OVER

NAME:ChangJiang
VARIABLE:
    int:c_i1
    int:c_i2
    float:c_f1
    float:c_f2
    string:c_str1
    string:c_str2
FORMAT:
    [c_i1, c_i2]
    [c_f1, c_f2]
    [c_str1, c_str2]
    [c_i1, c_f1, c_str1]
    [c_i2, c_f2, c_str2]
##END


NAME:HuangHe
VARIABLE:
    int:h_i1
    int:h_i2
    float:h_f1
    float:h_f2
    string:h_str1
    string:h_str2
FORMAT:
    [h_i1, h_i2]
    [h_f1, h_f2]
    [h_str1, h_str2]
    [h_i1, h_f1, h_str1]
    [h_i2, h_f2, h_str2]
##END
```

## 三、API说明

#### 1.C语言API：

- `extern CANGLAN_FORMATTER formatter`
  
  可以被所有导入了`"CangLan.h"`文件的文件引用的格式化工具结构体

- `int CangLan_Compiler(CANGLAN_FORMATTER *formatter, u8 formatNum);``
  
  编译指令，可以根据格式编号将变量编译为字节串，存储在字符数组`formatter->buffer`中。
  
  `*formatter`:格式化工具结构体的指针
  
  `formatNum`:格式编号
  
  返回值：编译后字节串，即`formatter->buffer`的长度

- `int CangLan_Resolver(CANGLAN_FORMATTER *formatter, u8 *rxstr, int rxstr_len);`
  
  `*formatter`:格式化工具结构体的指针
  
  `rxstr`:接收到的字节串的指针
  
  `rxstr`待解析内容的长度
  
  返回值：格式编号

- `void CangLan_Print(CANGLAN_FORMATTER *formatter);`
  
  打印该格式化工具可处理的全部变量

#### 2.python API

```python
# 初始化CangLan_MicroDsp对象
md = CangLan_MicroDsp()
# 可以在CangLan_MicroDsp初始化时传入一个字典作为参数
# 新传入的字典将用来存储int与float类型的变量，可以与其他数据管理工具交叉使用

# 添加格式:格式名称，序号，格式的内容情况，每一个变量对应的名字
md.add_new_command('com1', 0b00000001, (int, float, str), ['a1', 'b1', 'c1'])
md.add_new_command('com2', 0b00000010, (int, float, str, int), ['a2', 'b2', 'c2', 'd2'])
md.add_new_command('com3', 0b00000011, (float, float, str, str), ['a3', 'b3', 'c3', 'd3'])

# 将数据按照目标格式打包，返回一个格式化之后的字节串
data1 = md.pack_data('com1', (20, -30.2, 'hello world'))
data2 = md.pack_data('com2', (-210, 430.22, '1hello world2', 6))
data3 = md.pack_data('com3', (114.514, 14.514, "awawawawa", "miku"))

# 将格式化后的字节串解析成字典列表
md.unpack_data(data1 + data2 + data3)
# return:[{'com1': [20, -30.2, 'hello world']}, {'com2': [-210, 430.22, '1hello world2', 6]}, {'com3': [114.514, 14.514, 'awawawawa', 'miku']}]
```

## 四、注意事项：

1. example文件夹中提供了三个样例程序与其对应的CangLan_List.txt文件，可供参考使用

2. lib为库文件夹，不要乱改

3. C语言文件中默认的printf配置为"sys.h"与"usart.h"，如需修改为其他输出方式（例如在PC测试通信协议）可以前往"CangLan_tool.h"文件中修改引用的头文件。

4. STM32使用Keil MDK编译时应在魔术棒的c/c++选项卡中开启GNU选项。
