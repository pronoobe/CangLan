#ifndef __SERIAL_H
#define __SERIAL_H

#include "sys.h" 

/************************************************************
本程序只供学习使用，未经作者许可，不得用于其它任何用途
作者：DG_JiuYuan
修改日期:2022/12/9
版本：V2.0
All rights reserved
************************************************************/

#define SERIAL_RX_LEN 400
#define SERIAL_TX_LEN 400

#define RX_MOOD_N  1
#define RX_MOOD_RN  2


typedef struct{
    u8 mood;
    u8 usart_num;
    u8 RX_BUF[SERIAL_RX_LEN];
    u8 TX_BUF[SERIAL_TX_LEN];
    u16 STA;
    u16 RX_u8_num;
    u16 length;
    USART_TypeDef* USARTx;
}SERIAL;


void Serial_Init(SERIAL *Serial, USART_TypeDef* USARTx, u8 mood);
void Serial_TX_u8(SERIAL *Serial, u8 c);
void Serial_TX_u8str(SERIAL *Serial, u8 *str);
void Serial_TX_u8array(SERIAL *Serial, u8 *str, u32 len);
void Serial_printf(SERIAL *Serial, char *fmt, ...);
void Serial_RX_u8str(SERIAL *Serial);
u16 Serial_RXcheck(SERIAL *Serial);
 
#endif
 

