#ifndef __CANGLAN_H
#define __CANGLAN_H

#include "CangLan_tool.h"



/****************************** FORMATTER: formatter ******************************************/

        
//extern int i1, i2, i3, i4;
//extern float f1, f2;
//extern char s1[100];
//extern char s2[100];

//extern char *formatter_variable_name_list[8];

#define CANGLAN_FORMATTER_FORMAT_NUM 6
#define CANGLAN_FORMATTER_VARIABLE_NUM 8

extern CANGLAN_FORMATTER formatter;
extern CANGLAN_FORMAT formatter_formatList[CANGLAN_FORMATTER_FORMAT_NUM];
extern CANGLAN_VARIABLE formatter_vpList[CANGLAN_FORMATTER_VARIABLE_NUM];



#endif

