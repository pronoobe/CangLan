#include "CangLan.h"
#include "stdio.h"


int main(void)
{
    int i,length;
//    strcpy(c_str1,"I'm ChangJang");
//    strcpy(c_str2,"Hello HuangHe");
//    strcpy(h_str1,"I'm HuangHe");
//    strcpy(h_str2,"Hello ChangJang");
    strcpy(c_str1,"1");
    strcpy(c_str2,"2");
    strcpy(h_str1,"hello world1");
    strcpy(h_str2,"hello world2");

//    printf(">>HuangHe:\n");
//    CangLan_Print(&HuangHe);
//    printf(">>ChangJiang:\n");
//    CangLan_Print(&ChangJiang);
//    printf("************************************\n");

    length=CangLan_Compiler(&HuangHe,2);
    CangLan_Resolver(&ChangJiang,HuangHe.buffer,length);

//    printf("Result:\n");
//    printf(">>HuangHe:\n");
//    CangLan_Print(&HuangHe);
//    printf(">>ChangJiang:\n");
//    CangLan_Print(&ChangJiang);

//    for(i=0;i<15;i++)
//    {
//        printf("%d,",HuangHe.buffer[i]);
//    }

    return 0;
}
