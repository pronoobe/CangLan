#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "LED.h"
#include "KEY.h"
#include "ADC.h"
#include "SERIAL.h"
#include "CangLan.h"
 
 
/************************************************************
本程序只供学习使用，未经作者许可，不得用于其它任何用途
修改日期:2023/2/24
版本：V4.1
作者：DG_JiuYuan
Gitee个人主页:https://gitee.com/dugu-jiuyuan
All rights reserved
************************************************************/

SERIAL Serial2;

void USART2_Init(u32 bound)
{
    GPIO_InitTypeDef GPIO_InitStrue;
	USART_InitTypeDef USART_InitStrue;
	NVIC_InitTypeDef NVIC_InitStrue;
	
	// 外设使能时钟
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2 ,ENABLE );
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	USART_DeInit(USART2);  //复位串口2 -> 可以没有
	
	// 初始化 串口对应IO口  TX-PA2  RX-PA3
	GPIO_InitStrue.GPIO_Mode=GPIO_Mode_AF_PP;
	GPIO_InitStrue.GPIO_Pin=GPIO_Pin_2;
	GPIO_InitStrue.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStrue);
	
	GPIO_InitStrue.GPIO_Mode=GPIO_Mode_IN_FLOATING;
	GPIO_InitStrue.GPIO_Pin=GPIO_Pin_3;
    GPIO_Init(GPIOA,&GPIO_InitStrue);
	
	// 初始化 串口模式状态
	USART_InitStrue.USART_BaudRate=bound; // 波特率
	USART_InitStrue.USART_HardwareFlowControl=USART_HardwareFlowControl_None; // 硬件流控制
	USART_InitStrue.USART_Mode=USART_Mode_Tx|USART_Mode_Rx; // 发送 接收 模式都使用
	USART_InitStrue.USART_Parity=USART_Parity_No; // 没有奇偶校验
	USART_InitStrue.USART_StopBits=USART_StopBits_1; // 一位停止位
	USART_InitStrue.USART_WordLength=USART_WordLength_8b; // 每次发送数据宽度为8位
	USART_Init(USART2,&USART_InitStrue);
	
	// 初始化 中断优先级
	NVIC_InitStrue.NVIC_IRQChannel=USART2_IRQn;
	NVIC_InitStrue.NVIC_IRQChannelCmd=ENABLE;
	NVIC_InitStrue.NVIC_IRQChannelPreemptionPriority=2;
	NVIC_InitStrue.NVIC_IRQChannelSubPriority=1;
	NVIC_Init(&NVIC_InitStrue);
    
//	USART_ITConfig(USART2,USART_IT_RXNE,ENABLE);//开启接收中断
	
    USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);//开启串口接受中断
	USART_Cmd(USART2,ENABLE);//使能串口


}

void USART2_IRQHandler(void)
{
    Serial_RX_u8str(&Serial2);
    if(Serial_RXcheck(&Serial2)!=0)//检查是否接受到了完整的字符串
    {
        CangLan_Resolver(&formatter, Serial2.RX_BUF, Serial2.length);
        printf("主机解析数据:\r\n");
        printf("i1 = %d,f1 = %f\r\n",i1,f1);
        printf("i2 = %d,f2 = %f\r\n",i2,f2);
    }
    
}

int main(void)
{
    int i,len;
    
    delay_init();	    //延时函数初始化	
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
    uart_init(115200);
    
    KEY_Init();
    
    LED0_Init();
    LEDGroup_Init();
    USART2_Init(115200);//初始化USART2，波特率设置为9600
    
    Serial_Init(&Serial2,USART2,RX_MOOD_RN);//将硬件USART2绑定到Serial2结构体
    
    
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

