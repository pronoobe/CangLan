#include "CangLan_tool.h"
#include "CangLan.h"

#define CANGLAN_ASSERT 0
/*************** 格式说明 ***************/
//
//  @+FORMAT+LEN+=+BUF+CangLan_CRC+#
//
/***************************************/

void CangLan_default(void){
    ;
};

int CangLan_Compiler(CANGLAN_FORMATTER *formatter, u8 formatNum) {
    union {
        u8 _u8[4];
        int _i;
        float _f
    } zipper;
    u8 *format_buffer_pointer;
    u8 *format_pointer;
    u8 index, i, string_len, CangLan_CRC = 0;
    int length = 0;
    format_buffer_pointer = &(formatter->buffer[4]);
    format_pointer = formatter->format_pointer[formatNum].format_array_pointer;
#if CANGLAN_ASSERT == 1
    printf("************************************\r\n");
    printf("Prepare to Complie:\r\n");
    printf("Format:%d\r\n", formatNum);
    for (i = 0; i < formatter->format_pointer[formatNum].variable_num; i++) {
        printf("%d[%d],", formatter->format_pointer[formatNum].format_array_pointer[i],
               formatter->variable_pointer[format_pointer[i]].variable_type);
    }
    printf("\r\n");
#endif
    for (index = 0; index < formatter->format_pointer[formatNum].variable_num; index++) {
        if (formatter->variable_pointer[format_pointer[index]].variable_type == CANGLAN_VARIABLETYPE_INT) {
            zipper._i = *(formatter->variable_pointer[format_pointer[index]].__pointer.__int_pointer);
            *(format_buffer_pointer) = zipper._u8[0];
            CangLan_CRC += *(format_buffer_pointer);
            format_buffer_pointer++;
            *(format_buffer_pointer) = zipper._u8[1];
            CangLan_CRC += *(format_buffer_pointer);
            format_buffer_pointer++;
            *(format_buffer_pointer) = zipper._u8[2];
            CangLan_CRC += *(format_buffer_pointer);
            format_buffer_pointer++;
            *(format_buffer_pointer) = zipper._u8[3];
            CangLan_CRC += *(format_buffer_pointer);
            format_buffer_pointer++;
            length += 4;
#if CANGLAN_ASSERT == 1
            printf("[%d]add a new int:%d,now length = %d\r\n", index,
                   *(formatter->variable_pointer[format_pointer[index]].__pointer.__int_pointer), length);
#endif
        } else if (formatter->variable_pointer[format_pointer[index]].variable_type == CANGLAN_VARIABLETYPE_FLOAT) {
            zipper._f = *(formatter->variable_pointer[format_pointer[index]].__pointer.__float_pointer);
            *(format_buffer_pointer) = zipper._u8[0];
            CangLan_CRC += *(format_buffer_pointer);
            format_buffer_pointer++;
            *(format_buffer_pointer) = zipper._u8[1];
            CangLan_CRC += *(format_buffer_pointer);
            format_buffer_pointer++;
            *(format_buffer_pointer) = zipper._u8[2];
            CangLan_CRC += *(format_buffer_pointer);
            format_buffer_pointer++;
            *(format_buffer_pointer) = zipper._u8[3];
            CangLan_CRC += *(format_buffer_pointer);
            format_buffer_pointer++;
            length += 4;
#if CANGLAN_ASSERT == 1
            printf("[%d]add a new float:%f,now length = %d\r\n", index,
                   *(formatter->variable_pointer[format_pointer[index]].__pointer.__float_pointer), length);
#endif
        } else if (formatter->variable_pointer[format_pointer[index]].variable_type == CANGLAN_VARIABLETYPE_STRING) {
            string_len = 0;
            while (formatter->variable_pointer[format_pointer[index]].__pointer.__string_pointer[string_len] != '\0') {
                *(format_buffer_pointer) = formatter->variable_pointer[format_pointer[index]].__pointer.__string_pointer[string_len];
                CangLan_CRC += *(format_buffer_pointer);
                format_buffer_pointer++;
                length++;
                string_len++;
            }
            *(format_buffer_pointer) = '\0';
            CangLan_CRC += *(format_buffer_pointer);
            format_buffer_pointer++;
            length++;
#if CANGLAN_ASSERT == 1
            string_len++;
            printf("add[%d] a new string:%s,now length = %d\r\n", index,
                   format_buffer_pointer-string_len, length);
#endif
        }
    }
    formatter->buffer[0] = '@';
    formatter->buffer[1] = formatNum;
    formatter->buffer[2] = length;
    formatter->buffer[3] = '=';
    *(format_buffer_pointer) = CangLan_CRC;
    format_buffer_pointer++;
    *(format_buffer_pointer) = '#';

#if CANGLAN_ASSERT == 1
    printf("Comlile Out:\r\n");
    for (i = 0; i < length + 6; i++) {
        printf("%d,", formatter->buffer[i]);
    }
    printf("\r\n\r\n");
#endif
    return length+6;

}

int CangLan_Resolver(CANGLAN_FORMATTER *formatter, u8 *rxstr, int rxstr_len) {
    u8 *format_buffer_pointer = &(formatter->buffer[4]);
    u8 *format_pointer;
    u8 index, i, string_len;
    int formatNum = 255;
    union {
        u8 _u8[4];
        int _i;
        float _f;
    } zipper;

#if CANGLAN_ASSERT == 1
    printf("************************************\r\n");
    printf("Prepare to Resolve:\r\n");
#endif

    if (CangLan_RX_Check(formatter, rxstr, rxstr_len) == 0) {
        formatNum = formatter->buffer[1];
#if CANGLAN_ASSERT == 1
        for (i = 0; i < rxstr_len; i++) {
            printf("%d,", formatter->buffer[i]);
        }
        printf("\r\n");
        printf("Format:%d\r\n", formatNum);
#endif
        format_pointer = formatter->format_pointer[formatNum].format_array_pointer;
        for (index = 0; index < formatter->format_pointer[formatNum].variable_num; index++) {
            if (formatter->variable_pointer[format_pointer[index]].variable_type == CANGLAN_VARIABLETYPE_INT) {
                zipper._u8[0] = *(format_buffer_pointer);
                format_buffer_pointer++;
                zipper._u8[1] = *(format_buffer_pointer);
                format_buffer_pointer++;
                zipper._u8[2] = *(format_buffer_pointer);
                format_buffer_pointer++;
                zipper._u8[3] = *(format_buffer_pointer);
                format_buffer_pointer++;
                *(formatter->variable_pointer[format_pointer[index]].__pointer.__int_pointer) = zipper._i;

#if CANGLAN_ASSERT == 1
                printf("get a new int: %d(", zipper._i);
                for (i=0;i<4;i++)
                {
                    printf("%d,",zipper._u8[i]);
                }
                printf(")\r\n");
#endif
            } else if (formatter->variable_pointer[format_pointer[index]].variable_type == CANGLAN_VARIABLETYPE_FLOAT) {
                zipper._u8[0] = *(format_buffer_pointer);
                format_buffer_pointer++;
                zipper._u8[1] = *(format_buffer_pointer);
                format_buffer_pointer++;
                zipper._u8[2] = *(format_buffer_pointer);
                format_buffer_pointer++;
                zipper._u8[3] = *(format_buffer_pointer);
                format_buffer_pointer++;
                *(formatter->variable_pointer[format_pointer[index]].__pointer.__float_pointer) = zipper._f;
#if CANGLAN_ASSERT == 1
                printf("get a new float: %f(", zipper._f);
                for (i=0;i<4;i++)
                {
                    printf("%d,",zipper._u8[i]);
                }
                printf(")\r\n");
#endif
            } else if (formatter->variable_pointer[format_pointer[index]].variable_type ==
                       CANGLAN_VARIABLETYPE_STRING) {
                string_len = 0;
                while (*format_buffer_pointer !='\0') {
                    formatter->variable_pointer[format_pointer[index]].__pointer.__string_pointer[string_len] = *(format_buffer_pointer);
                    format_buffer_pointer++;
                    string_len++;
                }
                formatter->variable_pointer[format_pointer[index]].__pointer.__string_pointer[string_len] = '\0';
                format_buffer_pointer++;
#if CANGLAN_ASSERT == 1
                printf("get a new string: %s\r\n",
                       formatter->variable_pointer[format_pointer[index]].__pointer.__string_pointer);
#endif
            }
        }

    }

#if CANGLAN_ASSERT == 1
    printf("Resolve Out:\r\n");
    printf("Format:%d\r\n", formatNum);
    for (i = 0; i < formatter->format_pointer[formatNum].variable_num; i++) {
        printf("%d,", formatter->format_pointer[formatNum].format_array_pointer[i]);
    }
    printf("\r\n\r\n");
#endif

    return formatNum;

}

int CangLan_RX_Check(CANGLAN_FORMATTER *formatter, u8 *rxstr, int rxstr_len) {
    int chech_resuelt = 0;
    int index;
    u8 CangLan_CRC;
    
    if (rxstr[0] == '@' && rxstr[3] == '=' && rxstr[rxstr_len - 1] == '#') {
        if (rxstr[2] == rxstr_len - 6) {
            if (rxstr[1] >= 0 && rxstr[1] <= formatter->format_num) {
                for (index = 0; index < rxstr[2]; index++) {
                    formatter->buffer[index + 4] = rxstr[index + 4];
                    CangLan_CRC += rxstr[index + 4];
                }
                if (CangLan_CRC != rxstr[rxstr_len - 2]) {
#if CANGLAN_ASSERT == 1
                    printf("Check ERROR!!  CangLan_CRC=%d is not %d\r\r\n", CangLan_CRC, rxstr[rxstr_len - 2]);
#endif
                    chech_resuelt = 3;
                }
                else
                {
                    formatter->buffer[0] = rxstr[0];
                    formatter->buffer[1] = rxstr[1];
                    formatter->buffer[2] = rxstr[2];
                    formatter->buffer[3] = rxstr[3];
                    formatter->buffer[rxstr_len-2] = rxstr[rxstr_len-2];
                    formatter->buffer[rxstr_len-1] = rxstr[rxstr_len-1];

#if CANGLAN_ASSERT == 1
                    printf("Check CORRECT !!!\r\r\n");
#endif
                }
            } else {
#if CANGLAN_ASSERT == 1
                printf("Out of format_array!! Format=%d\r\n", rxstr[1]);
#endif
                chech_resuelt = 3;
            }
        } else {
#if CANGLAN_ASSERT == 1
            printf("Check ERROR!! Length=%d is not %d\r\r\n", rxstr_len - 6, rxstr[2]);
#endif
            chech_resuelt = 2;
        }
    } else {
#if CANGLAN_ASSERT == 1
        printf("KEY_WORDS Check ERROR!!   (%c,%c,%c)\r\r\n",rxstr[0],rxstr[3],rxstr[rxstr_len-1]);
#endif
        chech_resuelt = 1;

    }
    printf(""); /*If this function is not called, this piece of code will not be executed, and I don't know why.*/
    return chech_resuelt;
}



void CangLan_Print(CANGLAN_FORMATTER *formatter) {
    u8 i;
    for (i = 0; i < formatter->variable_num; i++) {
        if (formatter->variable_pointer[i].variable_type == CANGLAN_VARIABLETYPE_INT) {
            printf("Var%d=%d\r\n", i, *(formatter->variable_pointer[i].__pointer.__int_pointer));
        } else if (formatter->variable_pointer[i].variable_type == CANGLAN_VARIABLETYPE_FLOAT) {
            printf("Var%d=%f\r\n", i, *(formatter->variable_pointer[i].__pointer.__float_pointer));
        } else if (formatter->variable_pointer[i].variable_type == CANGLAN_VARIABLETYPE_STRING) {
            printf("Var%d=%s\r\n", i, formatter->variable_pointer[i].__pointer.__string_pointer);
        }
    }
}
