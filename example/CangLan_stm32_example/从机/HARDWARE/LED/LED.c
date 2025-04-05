#include "sys.h"
#include "LED.h"
#include "delay.h"

void LED0_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;
 
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC,ENABLE);//使能GPIOC时钟

	GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_13;//待配置GPIO为改组的第13号
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; //将GPIO配置为推挽输出模式
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;//GPIO最大工作频率为50Mhz
    
 	GPIO_Init(GPIOC, &GPIO_InitStructure);//初始化GPIOC
    
    GPIO_SetBits(GPIOC,GPIO_Pin_13);//设置PC13默认输出电平为高
    
    //上一行等价与这条语句：PCout(13)=1;
    
}   

void LEDGroup_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;
 
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE);//使能GPIOB时钟

	GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_12|GPIO_Pin_13|GPIO_Pin_14|GPIO_Pin_15;//待配置GPIO为该组的第12、13、14、15号
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; //将GPIO配置为推挽输出模式
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;//GPIO最大工作频率为50Mhz
    
 	GPIO_Init(GPIOB, &GPIO_InitStructure);//初始化GPIOC
    
    GPIO_SetBits(GPIOB,GPIO_Pin_12|GPIO_Pin_13|GPIO_Pin_14|GPIO_Pin_15);//设置默认输出电平为高
    
    //上一行等价于这条语句：GPIO_SetBits(1<<13|1<<13|1<<14|1<<15);
    
}   

void LED0_Flash(void)
{
	PCout(13)=0;
	delay_ms(200);
	PCout(13)=1;
	delay_ms(200);
}


//mood:流水灯阵列的闪灯方向，可以输入的值为1和2
void LEDGroup_Flash(u16 mood)
{
    static int i;

    PBout((u16)(12+i))=1;
    
    if(mood==1)
    {
        i++;
        if(i==4)
        {
            i=0;
        }
    }
    else if(mood == 2)
    {
        i--;
        if(i<0)
        {
            i=3;
        }        
    }
    
    PBout((u16)(12+i))=0;
    delay_ms(200);
    
}
