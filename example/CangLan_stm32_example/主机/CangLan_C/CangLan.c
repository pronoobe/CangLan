#include "CangLan.h"
#include "CangLan_tool.h"

/****************************** FORMATTER: formatter ******************************************/

//char formatter_variable_name0[] = "i1";
//char formatter_variable_name1[] = "i2";
//char formatter_variable_name2[] = "f1";
//char formatter_variable_name3[] = "f2";
//char formatter_variable_name4[] = "s1";
//char formatter_variable_name5[] = "s2";

//char* formatter_variable_name_list[6]={
//	formatter_variable_name0,
//	formatter_variable_name1,
//	formatter_variable_name2,
//	formatter_variable_name3,
//	formatter_variable_name4,
//	formatter_variable_name5
//};

int i1, i2;
float f1, f2;
char s1[100];
char s2[100];

u8 CangLan_formatter_format0[2] = {0,2};
u8 CangLan_formatter_format1[2] = {1,3};
u8 CangLan_formatter_format2[1] = {4};
u8 CangLan_formatter_format3[1] = {5};

CANGLAN_VARIABLE formatter_vpList[CANGLAN_FORMATTER_VARIABLE_NUM] = {{0,&i1},{0,&i2},{1,&f1},{1,&f2},{2,s1},{2,s2}};

CANGLAN_FORMAT formatter_formatList[CANGLAN_FORMATTER_FORMAT_NUM] ={
	{2,CangLan_formatter_format0},
	{2,CangLan_formatter_format1},
	{1,CangLan_formatter_format2},
	{1,CangLan_formatter_format3}
};

CANGLAN_FORMATTER formatter={4,6,formatter_vpList,formatter_formatList};


