#ifndef __LED_H
#define __LED_H

#include "sys.h"

void LED0_Init(void);
void LED0_Flash(void);

void LEDGroup_Init(void);
void LEDGroup_Flash(u16 mood);

#endif
