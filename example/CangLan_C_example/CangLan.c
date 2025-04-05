#include "CangLan.h"
#include "CangLan_tool.h"

/****************************** FORMATTER: ChangJiang ******************************************/

u8 CangLan_ChangJiang_format0[2] = {0,1};
u8 CangLan_ChangJiang_format1[2] = {2,3};
u8 CangLan_ChangJiang_format2[2] = {4,5};
u8 CangLan_ChangJiang_format3[3] = {0,2,4};
u8 CangLan_ChangJiang_format4[3] = {1,3,5};

CANGLAN_VARIABLE ChangJiang_vpList[CANGLAN_CHANGJIANG_VARIABLE_NUM] = {{0,&c_i1},{0,&c_i2},{1,&c_f1},{1,&c_f2},{2,c_str1},{2,c_str2}};

CANGLAN_FORMAT ChangJiang_formatList[CANGLAN_CHANGJIANG_FORMAT_NUM] ={
	{2,CangLan_ChangJiang_format0},
	{2,CangLan_ChangJiang_format1},
	{2,CangLan_ChangJiang_format2},
	{3,CangLan_ChangJiang_format3},
	{3,CangLan_ChangJiang_format4}
};

CANGLAN_FORMATTER ChangJiang={5,6,ChangJiang_vpList,ChangJiang_formatList};

/****************************** FORMATTER: HuangHe ******************************************/

u8 CangLan_HuangHe_format0[2] = {0,1};
u8 CangLan_HuangHe_format1[2] = {2,3};
u8 CangLan_HuangHe_format2[2] = {4,5};
u8 CangLan_HuangHe_format3[3] = {0,2,4};
u8 CangLan_HuangHe_format4[3] = {1,3,5};

CANGLAN_VARIABLE HuangHe_vpList[CANGLAN_HUANGHE_VARIABLE_NUM] = {{0,&h_i1},{0,&h_i2},{1,&h_f1},{1,&h_f2},{2,h_str1},{2,h_str2}};

CANGLAN_FORMAT HuangHe_formatList[CANGLAN_HUANGHE_FORMAT_NUM] ={
	{2,CangLan_HuangHe_format0},
	{2,CangLan_HuangHe_format1},
	{2,CangLan_HuangHe_format2},
	{3,CangLan_HuangHe_format3},
	{3,CangLan_HuangHe_format4}
};

CANGLAN_FORMATTER HuangHe={5,6,HuangHe_vpList,HuangHe_formatList};


