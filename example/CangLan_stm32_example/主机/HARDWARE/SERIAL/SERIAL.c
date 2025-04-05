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


//�����ڽṹ����USARTӲ����
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

//�øô��ڽṹ��󶨵�USART���͵����ַ�
void Serial_TX_u8(SERIAL *Serial, u8 c)
{

    USART_ClearFlag(Serial->USARTx, USART_FLAG_TC);//�����־λ����ֹ��һ���ֽڶ�ʧ
    USART_SendData(Serial->USARTx, c);
    while(USART_GetFlagStatus(Serial->USARTx,USART_FLAG_TC)!=SET);

}

//�øô��ڽṹ��󶨵�USART����u8�ַ���
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


//�øô��ڽṹ��󶨵�USART����u8�ַ�����
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


//�øô��ڽṹ��󶨵�USART������printf����ʽ�����ַ���
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



//���յ��ĵ����ַ����봮�ڽṹ��Ľ��ջ���
void Serial_RX_u8str(SERIAL *Serial)
{
    u8 Res;
    if(USART_GetITStatus(Serial->USARTx, USART_IT_RXNE) != RESET)  
    {
        Res =USART_ReceiveData(Serial->USARTx);	//��ȡ���յ�������
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
                Serial->STA=1;//�Ѿ��յ���'\r'
            }
            else if( Res == '\n' && Serial->STA==1)
            {
                Serial->STA=2;//�Ѿ��յ���'\r'֮���յ���'\n'
            }
            else
            {
                Serial->STA=0;
            }
                
        }
        
        //������������
        if(Serial->RX_u8_num>SERIAL_RX_LEN)
        {
            Serial->RX_u8_num=0;
            Serial->STA=0;
            
        }
        
    }
}
        


//����Ƿ���յ������ַ����������յ������ַ������򷵻��ַ������ȣ����򷵻�0��
u16 Serial_RXcheck(SERIAL *Serial)
{
    u16 flag;
    if(Serial->STA==Serial->mood&&Serial->RX_u8_num!=0)
    {
        Serial->RX_BUF[Serial->RX_u8_num-2] = '\0';//ʹ���ջ�����ֹ
        Serial->length = Serial->RX_u8_num-2;//��¼���յ����ַ�������
        
        Serial->STA = 0;//���ý���״̬
        Serial->RX_u8_num = 0;//���ü�����
        flag = 1;
    }
    else
    {
        flag = 0;
    }
    return flag;  

}
