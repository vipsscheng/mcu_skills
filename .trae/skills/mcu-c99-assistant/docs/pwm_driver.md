# PWM输出

## 概述

PWM（Pulse Width Modulation）是脉冲宽度调制的缩写，是一种通过改变脉冲宽度来控制模拟量的技术。在单片机中，PWM广泛应用于电机速度控制、LED亮度调节、蜂鸣器音调控制等场景。本文档将详细介绍国产单片机的PWM输出实现方法，包括初始化配置、占空比调整、频率设置等。

## 基本概念

- **PWM周期**：PWM信号的重复周期，单位为秒或毫秒
- **PWM频率**：PWM信号的频率，为周期的倒数，单位为Hz
- **占空比**：高电平时间占整个周期的百分比，范围通常为0-100%
- **分辨率**：PWM占空比的可调精度，由计数器位数决定

## STC系列PWM实现

### STC89C51软件PWM实现

STC89C51没有硬件PWM模块，需要使用定时器和软件模拟实现PWM。

```c
#include <reg51.h>

#define PWM_PIN P1_0

unsigned char pwm_duty = 50; // 占空比50%
unsigned int pwm_period = 1000; // PWM周期1ms

void Timer0_Init(void) {
    TMOD &= 0xF0;
    TMOD |= 0x01; // 定时器0工作在模式1
    TH0 = (65536 - 10) / 256; // 10us定时
    TL0 = (65536 - 10) % 256;
    ET0 = 1; // 允许定时器0中断
    EA = 1; // 允许总中断
    TR0 = 1; // 启动定时器0
}

unsigned int count = 0;

void Timer0_ISR() interrupt 1 {
    TH0 = (65536 - 10) / 256;
    TL0 = (65536 - 10) % 256;
    count++;
    
    if(count < pwm_duty * pwm_period / 100) {
        PWM_PIN = 1;
    } else if(count < pwm_period) {
        PWM_PIN = 0;
    } else {
        count = 0;
        PWM_PIN = 1;
    }
}

void main() {
    Timer0_Init();
    
    while(1) {
        // 可以在这里调整pwm_duty来改变占空比
    }
}
```

### STC12C5A60S2硬件PWM实现

STC12C5A60S2内置了PWM模块，支持多路PWM输出。

```c
#include <STC12C5A60S2.h>

void PWM_Init(void) {
    // 配置PWM引脚
    P1M1 &= ~0x03; // P1.0和P1.1设为推挽输出
    P1M0 |= 0x03;
    
    // 配置PWM
    PWM_CONTR = 0x80; // 使能PWM
    PWM_CSR = 0x00; // 自动重载模式
    
    // 设置PWM频率
    // PWM频率 = FOSC / (12 * (PWM_PSCR + 1) * (PWM_PERIOD + 1))
    PWM_PSCR = 0x00; // 预分频系数1
    PWM_PERIOD = 249; // 周期值，频率 = 24MHz / (12 * 1 * 250) = 8kHz
    
    // 设置占空比
    PWM0 = 125; // P1.0，占空比50%
    PWM1 = 62;  // P1.1，占空比25%
}

void main() {
    PWM_Init();
    
    while(1) {
        // 可以在这里调整PWM0和PWM1的值来改变占空比
    }
}
```

## GD32系列PWM实现

### GD32F103硬件PWM实现

GD32F103系列单片机的定时器支持PWM输出功能。

```c
#include "gd32f10x.h"

void PWM_Init(void) {
    // 使能定时器0时钟
    rcu_periph_clock_enable(RCU_TIMER0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA8为TIMER0_CH0
    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_8);
    
    // 配置定时器0
    timer_deinit(TIMER0);
    timer_init(TIMER0, TIMER_MODE_PWM, TIMER_COUNT_UP, 1000, 72);
    // 解释：
    // 定时器时钟频率 = 72MHz
    // 预分频系数 = 72-1，所以计数频率 = 72MHz / 72 = 1MHz
    // 自动重载值 = 1000-1，所以PWM周期 = 1000 / 1MHz = 1ms，频率 = 1kHz
    
    // 配置PWM通道0
    timer_channel_output_mode_config(TIMER0, TIMER_CH_0, TIMER_OC_MODE_PWM0);
    timer_channel_output_pulse_value_config(TIMER0, TIMER_CH_0, 500); // 占空比50%
    timer_channel_output_shadow_config(TIMER0, TIMER_CH_0, TIMER_OC_SHADOW_DISABLE);
    timer_channel_output_enable(TIMER0, TIMER_CH_0);
    
    // 启动定时器
    timer_enable(TIMER0);
}

void PWM_SetDuty(uint16_t duty) {
    // duty范围：0-999
    timer_channel_output_pulse_value_config(TIMER0, TIMER_CH_0, duty);
}

int main(void) {
    PWM_Init();
    
    while(1) {
        // 可以在这里调用PWM_SetDuty来改变占空比
    }
}
```

## HC32系列PWM实现

### HC32F460硬件PWM实现

HC32F460系列单片机的定时器支持PWM输出功能。

```c
#include "hc32f460.h"

void PWM_Init(void) {
    // 使能定时器0时钟
    CLK_FcgPeriphClockCmd(CLK_FCG_TIM0, ENABLE);
    // 使能GPIOA时钟
    CLK_FcgPeriphClockCmd(CLK_FCG_GPIOA, ENABLE);
    
    // 配置PA0为TIM0_CH0
    GPIO_SetFunc(GPIO_PORT_A, GPIO_PIN_0, GPIO_FUNC_3);
    
    // 配置定时器0
    TIM0_DeInit(M0P_TIM0);
    TIM0_Init(M0P_TIM0, TIMER_MODE_PWM, 1000, 72);
    // 解释：
    // 定时器时钟频率 = 72MHz
    // 预分频系数 = 72-1，所以计数频率 = 72MHz / 72 = 1MHz
    // 自动重载值 = 1000-1，所以PWM周期 = 1000 / 1MHz = 1ms，频率 = 1kHz
    
    // 配置PWM通道0
    TIM0_OC0Init(M0P_TIM0, TIMER_OC_MODE_PWM2, 500, 0); // 占空比50%
    TIM0_OC0Cmd(M0P_TIM0, ENABLE);
    
    // 启动定时器
    TIM0_Cmd(M0P_TIM0, ENABLE);
}

void PWM_SetDuty(uint16_t duty) {
    // duty范围：0-999
    TIM0_OC0SetCompareValue(M0P_TIM0, duty);
}

int main(void) {
    PWM_Init();
    
    while(1) {
        // 可以在这里调用PWM_SetDuty来改变占空比
    }
}
```

## MM32系列PWM实现

### MM32F103硬件PWM实现

MM32F103系列单片机的定时器支持PWM输出功能。

```c
#include "MM32F103.h"

void PWM_Init(void) {
    // 使能定时器1时钟
    RCC->APB2ENR |= RCC_APB2ENR_TIM1EN;
    // 使能GPIOA时钟
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN;
    
    // 配置PA8为TIM1_CH1
    GPIOA->CRH &= ~(0xF << 0);
    GPIOA->CRH |= (0xB << 0); // 复用推挽输出
    
    // 配置定时器1
    TIM1->PSC = 71; // 预分频系数72-1，计数频率=72MHz/72=1MHz
    TIM1->ARR = 999; // 自动重载值，PWM周期=1000/1MHz=1ms
    TIM1->CCMR1 &= ~(0x0F << 4);
    TIM1->CCMR1 |= (0x06 << 4); // PWM模式1
    TIM1->CCER |= (1 << 0); // 使能通道1输出
    TIM1->CR1 |= (1 << 0); // 启动定时器
    TIM1->BDTR |= (1 << 15); // 主输出使能
    
    // 设置占空比50%
    TIM1->CCR1 = 500;
}

void PWM_SetDuty(uint16_t duty) {
    // duty范围：0-999
    TIM1->CCR1 = duty;
}

int main(void) {
    PWM_Init();
    
    while(1) {
        // 可以在这里调用PWM_SetDuty来改变占空比
    }
}
```

## 通用PWM应用示例

### LED亮度控制

```c
#include "gd32f10x.h"

void PWM_Init(void) {
    // 使能定时器0时钟
    rcu_periph_clock_enable(RCU_TIMER0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA8为TIMER0_CH0
    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_8);
    
    // 配置定时器0
    timer_deinit(TIMER0);
    timer_init(TIMER0, TIMER_MODE_PWM, TIMER_COUNT_UP, 1000, 72);
    
    // 配置PWM通道0
    timer_channel_output_mode_config(TIMER0, TIMER_CH_0, TIMER_OC_MODE_PWM0);
    timer_channel_output_pulse_value_config(TIMER0, TIMER_CH_0, 0); // 初始占空比0%
    timer_channel_output_shadow_config(TIMER0, TIMER_CH_0, TIMER_OC_SHADOW_DISABLE);
    timer_channel_output_enable(TIMER0, TIMER_CH_0);
    
    // 启动定时器
    timer_enable(TIMER0);
}

void LED_BrightnessControl(uint8_t brightness) {
    // brightness范围：0-100
    uint16_t duty = (uint16_t)(brightness * 999 / 100);
    timer_channel_output_pulse_value_config(TIMER0, TIMER_CH_0, duty);
}

int main(void) {
    PWM_Init();
    
    uint8_t brightness = 0;
    uint8_t step = 5;
    
    while(1) {
        LED_BrightnessControl(brightness);
        brightness += step;
        if(brightness >= 100) {
            step = -5;
        } else if(brightness <= 0) {
            step = 5;
        }
        delay_ms(50);
    }
}
```

### 电机速度控制

```c
#include "gd32f10x.h"

#define MOTOR_PIN1 PA9
#define MOTOR_PIN2 PA10

void PWM_Init(void) {
    // 使能定时器1时钟
    rcu_periph_clock_enable(RCU_TIMER1);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA9为TIMER1_CH2
    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_9);
    // 配置PA10为普通输出
    gpio_init(GPIOA, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_10);
    
    // 配置定时器1
    timer_deinit(TIMER1);
    timer_init(TIMER1, TIMER_MODE_PWM, TIMER_COUNT_UP, 1000, 72);
    
    // 配置PWM通道2
    timer_channel_output_mode_config(TIMER1, TIMER_CH_2, TIMER_OC_MODE_PWM0);
    timer_channel_output_pulse_value_config(TIMER1, TIMER_CH_2, 0); // 初始占空比0%
    timer_channel_output_shadow_config(TIMER1, TIMER_CH_2, TIMER_OC_SHADOW_DISABLE);
    timer_channel_output_enable(TIMER1, TIMER_CH_2);
    
    // 启动定时器
    timer_enable(TIMER1);
}

void Motor_Control(int8_t speed) {
    // speed范围：-100到100
    if(speed > 0) {
        // 正转
        gpio_bit_set(GPIOA, GPIO_PIN_10);
        uint16_t duty = (uint16_t)(speed * 999 / 100);
        timer_channel_output_pulse_value_config(TIMER1, TIMER_CH_2, duty);
    } else if(speed < 0) {
        // 反转
        gpio_bit_reset(GPIOA, GPIO_PIN_10);
        uint16_t duty = (uint16_t)(-speed * 999 / 100);
        timer_channel_output_pulse_value_config(TIMER1, TIMER_CH_2, duty);
    } else {
        // 停止
        timer_channel_output_pulse_value_config(TIMER1, TIMER_CH_2, 0);
    }
}

int main(void) {
    PWM_Init();
    
    int8_t speed = 0;
    int8_t step = 5;
    
    while(1) {
        Motor_Control(speed);
        speed += step;
        if(speed >= 100) {
            step = -5;
        } else if(speed <= -100) {
            step = 5;
        }
        delay_ms(100);
    }
}
```

### 蜂鸣器音调控制

```c
#include "gd32f10x.h"

void PWM_Init(void) {
    // 使能定时器2时钟
    rcu_periph_clock_enable(RCU_TIMER2);
    // 使能GPIOB时钟
    rcu_periph_clock_enable(RCU_GPIOB);
    
    // 配置PB10为TIMER2_CH3
    gpio_init(GPIOB, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_10);
    
    // 配置定时器2
    timer_deinit(TIMER2);
    // 默认配置，后续通过函数调整频率
    timer_init(TIMER2, TIMER_MODE_PWM, TIMER_COUNT_UP, 1000, 72);
    
    // 配置PWM通道3
    timer_channel_output_mode_config(TIMER2, TIMER_CH_3, TIMER_OC_MODE_PWM0);
    timer_channel_output_pulse_value_config(TIMER2, TIMER_CH_3, 500); // 占空比50%
    timer_channel_output_shadow_config(TIMER2, TIMER_CH_3, TIMER_OC_SHADOW_DISABLE);
    timer_channel_output_enable(TIMER2, TIMER_CH_3);
    
    // 启动定时器
    timer_enable(TIMER2);
}

void Buzzer_SetFrequency(uint16_t frequency) {
    // frequency范围：100Hz到10kHz
    uint16_t period = 1000000 / frequency; // 周期（微秒）
    uint16_t arr = period - 1;
    uint16_t psc = 72 - 1; // 预分频系数
    
    timer_deinit(TIMER2);
    timer_init(TIMER2, TIMER_MODE_PWM, TIMER_COUNT_UP, arr, psc);
    timer_channel_output_mode_config(TIMER2, TIMER_CH_3, TIMER_OC_MODE_PWM0);
    timer_channel_output_pulse_value_config(TIMER2, TIMER_CH_3, arr / 2); // 占空比50%
    timer_channel_output_shadow_config(TIMER2, TIMER_CH_3, TIMER_OC_SHADOW_DISABLE);
    timer_channel_output_enable(TIMER2, TIMER_CH_3);
    timer_enable(TIMER2);
}

void Buzzer_PlayTone(uint16_t frequency, uint32_t duration) {
    Buzzer_SetFrequency(frequency);
    delay_ms(duration);
    // 停止蜂鸣器
    timer_channel_output_pulse_value_config(TIMER2, TIMER_CH_3, 0);
    delay_ms(50);
}

int main(void) {
    PWM_Init();
    
    while(1) {
        // 播放do re mi fa sol la si do
        Buzzer_PlayTone(262, 500); // do
        Buzzer_PlayTone(294, 500); // re
        Buzzer_PlayTone(330, 500); // mi
        Buzzer_PlayTone(349, 500); // fa
        Buzzer_PlayTone(392, 500); // sol
        Buzzer_PlayTone(440, 500); // la
        Buzzer_PlayTone(494, 500); // si
        Buzzer_PlayTone(523, 500); // do
        
        delay_ms(1000);
    }
}
```

## 常见问题与解决方案

### 问题1：PWM输出没有波形
- **原因**：可能是定时器没有使能，或者GPIO配置错误
- **解决方案**：检查定时器使能状态，确认GPIO配置为正确的复用功能

### 问题2：PWM频率不正确
- **原因**：定时器时钟配置错误，或者预分频系数和自动重载值计算错误
- **解决方案**：检查时钟源配置，重新计算预分频系数和自动重载值

### 问题3：PWM占空比调节不线性
- **原因**：可能是PWM模式选择错误，或者占空比计算错误
- **解决方案**：确认使用正确的PWM模式，检查占空比计算方法

### 问题4：PWM输出有抖动
- **原因**：可能是电源不稳定，或者定时器中断被其他中断干扰
- **解决方案**：增加电源滤波，优化中断优先级

## 最佳实践

1. **频率选择**：根据应用场景选择合适的PWM频率，如LED控制一般使用1kHz以上，电机控制根据电机特性选择
2. **分辨率**：根据需要的精度选择合适的PWM分辨率，分辨率越高，控制精度越高
3. **占空比范围**：确保占空比在合理范围内，避免极端值（如0%或100%）导致的问题
4. **电源管理**：在不需要PWM输出时，关闭定时器以降低功耗
5. **干扰防护**：对于电机等感性负载，需要添加续流二极管以保护电路
6. **多通道协调**：在使用多个PWM通道时，注意通道间的同步和相位关系

## 示例项目

### 项目：呼吸灯

#### 功能描述
- 使用PWM控制LED亮度，实现呼吸效果
- 亮度从暗到亮再从亮到暗循环变化

#### 代码实现

```c
#include "gd32f10x.h"

void PWM_Init(void) {
    // 使能定时器0时钟
    rcu_periph_clock_enable(RCU_TIMER0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA8为TIMER0_CH0
    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_8);
    
    // 配置定时器0
    timer_deinit(TIMER0);
    timer_init(TIMER0, TIMER_MODE_PWM, TIMER_COUNT_UP, 1000, 72);
    
    // 配置PWM通道0
    timer_channel_output_mode_config(TIMER0, TIMER_CH_0, TIMER_OC_MODE_PWM0);
    timer_channel_output_pulse_value_config(TIMER0, TIMER_CH_0, 0);
    timer_channel_output_shadow_config(TIMER0, TIMER_CH_0, TIMER_OC_SHADOW_DISABLE);
    timer_channel_output_enable(TIMER0, TIMER_CH_0);
    
    // 启动定时器
    timer_enable(TIMER0);
}

void delay_ms(uint32_t ms) {
    uint32_t i, j;
    for(i = ms; i > 0; i--) {
        for(j = 110; j > 0; j--);
    }
}

int main(void) {
    PWM_Init();
    
    uint16_t duty = 0;
    uint8_t direction = 1; // 1: 增加, 0: 减少
    
    while(1) {
        if(direction) {
            duty += 10;
            if(duty >= 1000) {
                direction = 0;
            }
        } else {
            duty -= 10;
            if(duty <= 0) {
                direction = 1;
            }
        }
        
        timer_channel_output_pulse_value_config(TIMER0, TIMER_CH_0, duty);
        delay_ms(20);
    }
}
```

### 项目：直流电机速度控制器

#### 功能描述
- 使用PWM控制直流电机速度
- 通过串口接收命令调整电机速度
- 支持正转、反转和停止功能

#### 代码实现

```c
#include "gd32f10x.h"
#include <string.h>

#define MOTOR_PIN1 PA9
#define MOTOR_PIN2 PA10

void PWM_Init(void) {
    // 使能定时器1时钟
    rcu_periph_clock_enable(RCU_TIMER1);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA9为TIMER1_CH2
    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_9);
    // 配置PA10为普通输出
    gpio_init(GPIOA, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_10);
    
    // 配置定时器1
    timer_deinit(TIMER1);
    timer_init(TIMER1, TIMER_MODE_PWM, TIMER_COUNT_UP, 1000, 72);
    
    // 配置PWM通道2
    timer_channel_output_mode_config(TIMER1, TIMER_CH_2, TIMER_OC_MODE_PWM0);
    timer_channel_output_pulse_value_config(TIMER1, TIMER_CH_2, 0);
    timer_channel_output_shadow_config(TIMER1, TIMER_CH_2, TIMER_OC_SHADOW_DISABLE);
    timer_channel_output_enable(TIMER1, TIMER_CH_2);
    
    // 启动定时器
    timer_enable(TIMER1);
}

void UART_Init(void) {
    // 使能USART0时钟
    rcu_periph_clock_enable(RCU_USART0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA9为USART0_TX
    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_9);
    // 配置PA10为USART0_RX
    gpio_init(GPIOA, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_50MHZ, GPIO_PIN_10);
    
    // 配置USART0
    usart_deinit(USART0);
    usart_baudrate_set(USART0, 115200);
    usart_word_length_set(USART0, USART_WL_8BIT);
    usart_stop_bit_set(USART0, USART_STB_1BIT);
    usart_parity_config(USART0, USART_PM_NONE);
    usart_hardware_flow_cts_config(USART0, USART_CTS_DISABLE);
    usart_hardware_flow_rts_config(USART0, USART_RTS_DISABLE);
    usart_receive_config(USART0, USART_RECEIVE_ENABLE);
    usart_transmit_config(USART0, USART_TRANSMIT_ENABLE);
    usart_enable(USART0);
}

void UART_SendString(uint8_t *str) {
    while(*str) {
        usart_data_transmit(USART0, *str++);
        while(RESET == usart_flag_get(USART0, USART_FLAG_TBE));
    }
}

uint8_t UART_ReceiveByte(void) {
    while(RESET == usart_flag_get(USART0, USART_FLAG_RBNE));
    return usart_data_receive(USART0);
}

void Motor_Control(int8_t speed) {
    // speed范围：-100到100
    if(speed > 0) {
        // 正转
        gpio_bit_set(GPIOA, GPIO_PIN_10);
        uint16_t duty = (uint16_t)(speed * 999 / 100);
        timer_channel_output_pulse_value_config(TIMER1, TIMER_CH_2, duty);
    } else if(speed < 0) {
        // 反转
        gpio_bit_reset(GPIOA, GPIO_PIN_10);
        uint16_t duty = (uint16_t)(-speed * 999 / 100);
        timer_channel_output_pulse_value_config(TIMER1, TIMER_CH_2, duty);
    } else {
        // 停止
        timer_channel_output_pulse_value_config(TIMER1, TIMER_CH_2, 0);
    }
}

int main(void) {
    PWM_Init();
    UART_Init();
    
    UART_SendString((uint8_t *)"Motor speed controller ready\r\n");
    UART_SendString((uint8_t *)"Usage: +<speed> for forward, -<speed> for reverse, 0 for stop\r\n");
    
    char buffer[10];
    uint8_t index = 0;
    
    while(1) {
        if(RESET != usart_flag_get(USART0, USART_FLAG_RBNE)) {
            uint8_t data = UART_ReceiveByte();
            
            if(data == '\r' || data == '\n') {
                buffer[index] = '\0';
                index = 0;
                
                int8_t speed = atoi(buffer);
                if(speed > 100) speed = 100;
                if(speed < -100) speed = -100;
                
                Motor_Control(speed);
                
                char response[32];
                sprintf(response, "Motor speed set to: %d\r\n", speed);
                UART_SendString((uint8_t *)response);
            } else {
                if(index < 9) {
                    buffer[index++] = data;
                }
            }
        }
    }
}
```

## 总结

PWM是一种非常重要的技术，在嵌入式系统中有着广泛的应用。本文档提供了STC、GD32、HC32、MM32等国产单片机的PWM实现方法，包括软件模拟和硬件实现两种方式。

在实际开发中，应根据具体的应用场景选择合适的PWM实现方式：
- **软件PWM**：适用于没有硬件PWM模块的单片机，或需要灵活控制的场景
- **硬件PWM**：适用于需要高精度、高频率PWM输出的场景

同时，应注意PWM的频率、占空比、分辨率等参数的选择，以满足具体应用的需求。通过本文档的学习，开发者可以掌握国产单片机的PWM输出技术，为嵌入式系统开发打下坚实的基础。