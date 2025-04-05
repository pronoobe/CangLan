#include "sys.h"
#include "KEY.h"
#include "delay.h"

void KEY_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;
 
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);//使能GPIOA时钟

	GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_4|GPIO_Pin_5;//待配置GPIO为改组的第4、5号
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU; //将GPIO配置为上拉输入模式
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;//GPIO最大工作频率为50Mhz
    
 	GPIO_Init(GPIOA, &GPIO_InitStructure);//初始化GPIOA
    

}   

//读取按键，检查按键是否被按下。
u8 KEY_Read(u8 key)
{
    u8 key_value=0;//默认按键没被按下
    if(PAin((4+key))==0)//因为是上拉输入，结合原理图，读取到低电平时，按键被按下
    {
        delay_ms(10);//延时10毫秒消除按键抖动
        if(PAin((4+key))==0)//再次判定按键情况
            key_value=1;//如果按键被按下，则返回1
    }
    
    return key_value;//

}
