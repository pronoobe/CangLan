#include "SERIAL.h" 
#include "sys.h"
#include "stdarg.h"
#include "stdio.h"


u8 Get_USART_Num(USART_TypeDef* usart)
{
    u8 num;
    if(usart == USART1){num = 0;}
    else if(usart == USART2){num = 1;}
    
#ifdef STM32F10X_MD
    else if(usart == USART3){num = 2;}
#endif    
    
#ifdef STM32F10X_HD
    else if(usart == USART3){num = 2;}
    else if(usart == UART4){num = 3;}
    else if(usart == UART5){num = 4;}
#endif
    else {num = 255;}
    return num;
}


//将串口结构体与USART硬件绑定
void Serial_Init(SERIAL *Serial, USART_TypeDef* USARTx, u8 mood)
{
    u8 usart_num;
    usart_num = Get_USART_Num(USARTx);
    if(usart_num!=255)
    {
        Serial->USARTx=USARTx;
        Serial->usart_num = usart_num;
        Serial->mood = mood;
        
    }
}

//用该串口结构体绑定的USART发送单个字符
void Serial_TX_u8(SERIAL *Serial, u8 c)
{

    USART_ClearFlag(Serial->USARTx, USART_FLAG_TC);//清除标志位，防止第一个字节丢失
    USART_SendData(Serial->USARTx, c);
    while(USART_GetFlagStatus(Serial->USARTx,USART_FLAG_TC)!=SET);

}

//用该串口结构体绑定的USART发送u8字符串
void Serial_TX_u8str(SERIAL *Serial, u8 *str)
{
    while(*str!='\0')
    {
        Serial_TX_u8(Serial, *str);
        str++;
    }
    Serial_TX_u8(Serial, '\r');
    Serial_TX_u8(Serial, '\n');    
}


//用该串口结构体绑定的USART发送u8字符数组
void Serial_TX_u8array(SERIAL *Serial, u8 *str, u32 len)
{
    u32 i;
    for(i=0;i<len;i++)
    {
        Serial_TX_u8(Serial, *str);
        str++;
    }
    Serial_TX_u8(Serial, '\r');
    Serial_TX_u8(Serial, '\n');    
}


//用该串口结构体绑定的USART发送以printf的形式发送字符串
void Serial_printf(SERIAL *Serial, char *fmt, ...)
{
    u8 *str;
	va_list ap;
    va_start(ap,fmt);
    vsprintf((char*)(Serial->TX_BUF),fmt,ap);
    va_end(ap);
    
    str = Serial->TX_BUF;
    
    while(*str!='\0')
    {
        Serial_TX_u8(Serial, *str);
        str++;
    }
    Serial_TX_u8(Serial, '\r');
    Serial_TX_u8(Serial, '\n');    
}



//将收到的单个字符存入串口结构体的接收缓存
void Serial_RX_u8str(SERIAL *Serial)
{
    u8 Res;
    if(USART_GetITStatus(Serial->USARTx, USART_IT_RXNE) != RESET)  
    {
        Res =USART_ReceiveData(Serial->USARTx);	//读取接收到的数据
        Serial->RX_BUF[Serial->RX_u8_num]=Res;
        Serial->RX_u8_num++;
        // printf("%c",Res);

        if (Serial->mood==RX_MOOD_N)
        {
            if(Res == '\n')
            {
                Serial->STA=1;
            }
            else
            {
                Serial->STA=0;
            }
        }
        else if (Serial->mood==RX_MOOD_RN)
        {
            if(Res == '\r')
            {
                Serial->STA=1;//已经收到了'\r'
            }
            else if( Res == '\n' && Serial->STA==1)
            {
                Serial->STA=2;//已经收到了'\r'之后收到了'\n'
            }
            else
            {
                Serial->STA=0;
            }
                
        }
        
        //超长，重置零
        if(Serial->RX_u8_num>SERIAL_RX_LEN)
        {
            Serial->RX_u8_num=0;
            Serial->STA=0;
            
        }
        
    }
}
        


//检查是否接收到完整字符串，若接收到完整字符串，则返回字符串长度，否则返回0；
u16 Serial_RXcheck(SERIAL *Serial)
{
    u16 flag;
    if(Serial->STA==Serial->mood&&Serial->RX_u8_num!=0)
    {
        Serial->RX_BUF[Serial->RX_u8_num-2] = '\0';//使接收缓存休止
        Serial->length = Serial->RX_u8_num-2;//记录接收到的字符串长度
        
        Serial->STA = 0;//重置接收状态
        Serial->RX_u8_num = 0;//重置计数器
        flag = 1;
    }
    else
    {
        flag = 0;
    }
    return flag;  

}
