#include "CangLan.h"
#include "CangLan_tool.h"

/****************************** FORMATTER: formatter ******************************************/

//char formatter_variable_name0[] = "i1";
//char formatter_variable_name1[] = "i2";
//char formatter_variable_name2[] = "i3";
//char formatter_variable_name3[] = "i4";
//char formatter_variable_name4[] = "f1";
//char formatter_variable_name5[] = "f2";
//char formatter_variable_name6[] = "s1";
//char formatter_variable_name7[] = "s2";

//char* formatter_variable_name_list[8]={
//	formatter_variable_name0,
//	formatter_variable_name1,
//	formatter_variable_name2,
//	formatter_variable_name3,
//	formatter_variable_name4,
//	formatter_variable_name5,
//	formatter_variable_name6,
//	formatter_variable_name7
//};

//int i1, i2, i3, i4;
//float f1, f2;
//char s1[100];
//char s2[100];

u8 CangLan_formatter_format0[4] = {0,1,2,3};
u8 CangLan_formatter_format1[2] = {4,5};
u8 CangLan_formatter_format2[2] = {0,4};
u8 CangLan_formatter_format3[2] = {1,5};
u8 CangLan_formatter_format4[1] = {6};
u8 CangLan_formatter_format5[1] = {7};

CANGLAN_VARIABLE formatter_vpList[CANGLAN_FORMATTER_VARIABLE_NUM] = {{0,&i1},{0,&i2},{0,&i3},{0,&i4},{1,&f1},{1,&f2},{2,s1},{2,s2}};

CANGLAN_FORMAT formatter_formatList[CANGLAN_FORMATTER_FORMAT_NUM] ={
	{4,CangLan_formatter_format0},
	{2,CangLan_formatter_format1},
	{2,CangLan_formatter_format2},
	{2,CangLan_formatter_format3},
	{1,CangLan_formatter_format4},
	{1,CangLan_formatter_format5}
};

CANGLAN_FORMATTER formatter={6,8,formatter_vpList,formatter_formatList};


