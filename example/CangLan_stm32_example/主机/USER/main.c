#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "LED.h"
#include "KEY.h"
#include "ADC.h"
#include "SERIAL.h"
#include "CangLan.h"
 
 
/************************************************************
������ֻ��ѧϰʹ�ã�δ��������ɣ��������������κ���;
�޸�����:2023/2/24
�汾��V4.1
���ߣ�DG_JiuYuan
Gitee������ҳ:https://gitee.com/dugu-jiuyuan
All rights reserved
************************************************************/

SERIAL Serial2;

void USART2_Init(u32 bound)
{
    GPIO_InitTypeDef GPIO_InitStrue;
	USART_InitTypeDef USART_InitStrue;
	NVIC_InitTypeDef NVIC_InitStrue;
	
	// ����ʹ��ʱ��
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2 ,ENABLE );
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	USART_DeInit(USART2);  //��λ����2 -> ����û��
	
	// ��ʼ�� ���ڶ�ӦIO��  TX-PA2  RX-PA3
	GPIO_InitStrue.GPIO_Mode=GPIO_Mode_AF_PP;
	GPIO_InitStrue.GPIO_Pin=GPIO_Pin_2;
	GPIO_InitStrue.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStrue);
	
	GPIO_InitStrue.GPIO_Mode=GPIO_Mode_IN_FLOATING;
	GPIO_InitStrue.GPIO_Pin=GPIO_Pin_3;
    GPIO_Init(GPIOA,&GPIO_InitStrue);
	
	// ��ʼ�� ����ģʽ״̬
	USART_InitStrue.USART_BaudRate=bound; // ������
	USART_InitStrue.USART_HardwareFlowControl=USART_HardwareFlowControl_None; // Ӳ��������
	USART_InitStrue.USART_Mode=USART_Mode_Tx|USART_Mode_Rx; // ���� ���� ģʽ��ʹ��
	USART_InitStrue.USART_Parity=USART_Parity_No; // û����żУ��
	USART_InitStrue.USART_StopBits=USART_StopBits_1; // һλֹͣλ
	USART_InitStrue.USART_WordLength=USART_WordLength_8b; // ÿ�η������ݿ��Ϊ8λ
	USART_Init(USART2,&USART_InitStrue);
	
	// ��ʼ�� �ж����ȼ�
	NVIC_InitStrue.NVIC_IRQChannel=USART2_IRQn;
	NVIC_InitStrue.NVIC_IRQChannelCmd=ENABLE;
	NVIC_InitStrue.NVIC_IRQChannelPreemptionPriority=2;
	NVIC_InitStrue.NVIC_IRQChannelSubPriority=1;
	NVIC_Init(&NVIC_InitStrue);
    
//	USART_ITConfig(USART2,USART_IT_RXNE,ENABLE);//���������ж�
	
    USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);//�������ڽ����ж�
	USART_Cmd(USART2,ENABLE);//ʹ�ܴ���


}

void USART2_IRQHandler(void)
{
    Serial_RX_u8str(&Serial2);
    if(Serial_RXcheck(&Serial2)!=0)//����Ƿ���ܵ����������ַ���
    {
        CangLan_Resolver(&formatter, Serial2.RX_BUF, Serial2.length);
        printf("������������:\r\n");
        printf("i1 = %d,f1 = %f\r\n",i1,f1);
        printf("i2 = %d,f2 = %f\r\n",i2,f2);
    }
    
}

int main(void)
{
    int i,len;
    
    delay_init();	    //��ʱ������ʼ��	
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
    uart_init(115200);
    
    KEY_Init();
    
    LED0_Init();
    LEDGroup_Init();
    USART2_Init(115200);//��ʼ��USART2������������Ϊ9600
    
    Serial_Init(&Serial2,USART2,RX_MOOD_RN);//��Ӳ��USART2�󶨵�Serial2�ṹ��
    
    
    while(1)
    {
        if(KEY_Read(0))
        {
            LED0_Flash();
            i1+=1;
            f1+=1;
            len = CangLan_Compiler(&formatter, 0);
            Serial_TX_u8array(&Serial2,formatter.buffer,len);
            printf("i1 = %d,f1 = %f\r\n",i1,f1);
            
        }
        
        
    }

}

