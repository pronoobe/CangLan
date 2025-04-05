#include "sys.h"
#include "LED.h"
#include "delay.h"

void LED0_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;
 
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC,ENABLE);//ʹ��GPIOCʱ��

	GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_13;//������GPIOΪ����ĵ�13��
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; //��GPIO����Ϊ�������ģʽ
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;//GPIO�����Ƶ��Ϊ50Mhz
    
 	GPIO_Init(GPIOC, &GPIO_InitStructure);//��ʼ��GPIOC
    
    GPIO_SetBits(GPIOC,GPIO_Pin_13);//����PC13Ĭ�������ƽΪ��
    
    //��һ�еȼ���������䣺PCout(13)=1;
    
}   

void LEDGroup_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;
 
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE);//ʹ��GPIOBʱ��

	GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_12|GPIO_Pin_13|GPIO_Pin_14|GPIO_Pin_15;//������GPIOΪ����ĵ�12��13��14��15��
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; //��GPIO����Ϊ�������ģʽ
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;//GPIO�����Ƶ��Ϊ50Mhz
    
 	GPIO_Init(GPIOB, &GPIO_InitStructure);//��ʼ��GPIOC
    
    GPIO_SetBits(GPIOB,GPIO_Pin_12|GPIO_Pin_13|GPIO_Pin_14|GPIO_Pin_15);//����Ĭ�������ƽΪ��
    
    //��һ�еȼ���������䣺GPIO_SetBits(1<<13|1<<13|1<<14|1<<15);
    
}   

void LED0_Flash(void)
{
	PCout(13)=0;
	delay_ms(200);
	PCout(13)=1;
	delay_ms(200);
}


//mood:��ˮ�����е����Ʒ��򣬿��������ֵΪ1��2
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
