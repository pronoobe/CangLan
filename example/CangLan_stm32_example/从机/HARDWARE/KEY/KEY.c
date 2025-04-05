#include "sys.h"
#include "KEY.h"
#include "delay.h"

void KEY_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;
 
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);//ʹ��GPIOAʱ��

	GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_4|GPIO_Pin_5;//������GPIOΪ����ĵ�4��5��
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU; //��GPIO����Ϊ��������ģʽ
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;//GPIO�����Ƶ��Ϊ50Mhz
    
 	GPIO_Init(GPIOA, &GPIO_InitStructure);//��ʼ��GPIOA
    

}   

//��ȡ��������鰴���Ƿ񱻰��¡�
u8 KEY_Read(u8 key)
{
    u8 key_value=0;//Ĭ�ϰ���û������
    if(PAin((4+key))==0)//��Ϊ���������룬���ԭ��ͼ����ȡ���͵�ƽʱ������������
    {
        delay_ms(10);//��ʱ10����������������
        if(PAin((4+key))==0)//�ٴ��ж��������
            key_value=1;//������������£��򷵻�1
    }
    
    return key_value;//

}
