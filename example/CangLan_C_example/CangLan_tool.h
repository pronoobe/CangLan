#ifndef __CANGLAN_TOOL_H
#define __CANGLAN_TOOL_H

#include "string.h"
#include "stdio.h"

#define u8 unsigned char


#define CANGLAN_VARIABLETYPE_INT 0
#define CANGLAN_VARIABLETYPE_FLOAT 1
#define CANGLAN_VARIABLETYPE_STRING 2

#define CANGLAN_BUFFER_LEN 300

typedef union{
	int *__int_pointer;
	float *__float_pointer;
	char *__string_pointer;
}CANGLAN_VARIABLE_POINTER;

typedef struct{
	u8 variable_type;
    CANGLAN_VARIABLE_POINTER __pointer;
}CANGLAN_VARIABLE;


typedef struct{
	u8 variable_num;
	u8 *format_array_pointer;

}CANGLAN_FORMAT;

typedef struct{
	u8 format_num;
    u8 variable_num;
	CANGLAN_VARIABLE *variable_pointer;
	CANGLAN_FORMAT *format_pointer;
	unsigned char buffer[CANGLAN_BUFFER_LEN];
}CANGLAN_FORMATTER;

#define CangLan_Set_VariablePointer_Int(__vp,__int_pointer) {__vp->variable_type=CANGLAN_VARIABLETYPE_INT;vp->__pointer.__int_pointer=(__int_pointer)}
#define CangLan_Set_VariablePointer_Float(__vp,__float_pointer) {__vp->variable_type=CANGLAN_VARIABLETYPE_FLOAT;vp->__pointer.__float_pointer=(__float_pointer)}
#define CangLan_Set_VariablePointer_String(__vp,__string_pointer) {__vp->variable_type=CANGLAN_VARIABLETYPE_STRING;vp->__pointer.__string_pointer=(__string_pointer)}


int CangLan_Compiler(CANGLAN_FORMATTER *formatter, u8 formatNum);
int CangLan_Resolver(CANGLAN_FORMATTER *formatter, unsigned char *rxstr, int rxstr_len);

int CangLan_RX_Check(CANGLAN_FORMATTER *formatter, unsigned char *rxstr, int rxstr_len);
void CangLan_Print(CANGLAN_FORMATTER *formatter);


#endif

