# 定时器与中断

## 概述

定时器是单片机中用于计时、计数和生成周期性信号的重要外设，而中断是单片机处理紧急事件的机制。两者结合使用，可以实现精确的时间控制、事件响应和系统调度。本文档将详细介绍国产单片机的定时器与中断实现方法，包括初始化配置、中断处理、定时器应用等。

## 基本概念

### 定时器

- **定时器**：用于测量时间间隔或生成周期性信号的外设
- **计数器**：定时器的核心，用于累计时钟脉冲
- **预分频器**：用于降低定时器的计数频率
- **自动重载寄存器**：存储定时器的周期值
- **比较寄存器**：用于生成比较事件或PWM信号

### 中断

- **中断**：当特定事件发生时，CPU暂停当前任务转而处理该事件的机制
- **中断源**：产生中断请求的硬件或软件事件
- **中断优先级**：中断处理的优先顺序
- **中断向量**：中断服务程序的入口地址
- **中断服务程序**：处理中断事件的代码

## STC系列定时器与中断实现

### STC89C51定时器与中断

STC89C51有3个定时器/计数器：T0、T1和T2。

#### 定时器0初始化

```c
#include <reg51.h>

void Timer0_Init(void) {
    TMOD &= 0xF0; // 清除T0的模式位
    TMOD |= 0x01; // T0工作在模式1（16位定时器）
    TH0 = (65536 - 50000) / 256; // 50ms定时
    TL0 = (65536 - 50000) % 256;
    ET0 = 1; // 允许T0中断
    EA = 1; // 允许总中断
    TR0 = 1; // 启动T0
}

unsigned int count = 0;

void Timer0_ISR() interrupt 1 {
    TH0 = (65536 - 50000) / 256;
    TL0 = (65536 - 50000) % 256;
    count++;
    if(count >= 20) { // 1秒
        count = 0;
        // 在这里执行定时任务
    }
}

void main() {
    Timer0_Init();
    while(1) {
        // 主循环
    }
}
```

#### 外部中断0初始化

```c
#include <reg51.h>

void External0_Init(void) {
    IT0 = 1; // 下降沿触发
    EX0 = 1; // 允许外部中断0
    EA = 1; // 允许总中断
}

void External0_ISR() interrupt 0 {
    // 外部中断0处理
}

void main() {
    External0_Init();
    while(1) {
        // 主循环
    }
}
```

### STC12C5A60S2定时器与中断

STC12C5A60S2有4个定时器/计数器：T0、T1、T2和T3。

#### 定时器1初始化（1T模式）

```c
#include <STC12C5A60S2.h>

void Timer1_Init(void) {
    TMOD &= 0x0F; // 清除T1的模式位
    TMOD |= 0x10; // T1工作在模式1（16位定时器）
    AUXR |= 0x40; // T1工作在1T模式
    TH1 = (65536 - 10000) / 256; // 10ms定时
    TL1 = (65536 - 10000) % 256;
    ET1 = 1; // 允许T1中断
    EA = 1; // 允许总中断
    TR1 = 1; // 启动T1
}

unsigned int count = 0;

void Timer1_ISR() interrupt 3 {
    TH1 = (65536 - 10000) / 256;
    TL1 = (65536 - 10000) % 256;
    count++;
    if(count >= 100) { // 1秒
        count = 0;
        // 在这里执行定时任务
    }
}

void main() {
    Timer1_Init();
    while(1) {
        // 主循环
    }
}
```

## GD32系列定时器与中断实现

### GD32F103定时器与中断

GD32F103系列单片机有多个定时器，包括高级定时器（TIMER0）、通用定时器（TIMER1-TIMER4）和基本定时器（TIMER5-TIMER6）。

#### 定时器2初始化

```c
#include "gd32f10x.h"

void Timer2_Init(void) {
    // 使能定时器2时钟
    rcu_periph_clock_enable(RCU_TIMER2);
    
    // 配置定时器2
    timer_deinit(TIMER2);
    timer_init(TIMER2, TIMER_MODE_UP, 1000, 7200);
    // 解释：
    // 定时器时钟频率 = 72MHz
    // 预分频系数 = 7200-1，所以计数频率 = 72MHz / 7200 = 10kHz
    // 自动重载值 = 1000-1，所以定时周期 = 1000 / 10kHz = 100ms
    
    // 使能定时器2更新中断
    timer_interrupt_enable(TIMER2, TIMER_INT_UP);
    
    // 配置NVIC
    nvic_irq_enable(TIMER2_IRQn, 2U, 0U);
    
    // 启动定时器2
    timer_enable(TIMER2);
}

unsigned int count = 0;

void TIMER2_IRQHandler(void) {
    if(timer_flag_get(TIMER2, TIMER_FLAG_UP)) {
        timer_flag_clear(TIMER2, TIMER_FLAG_UP);
        count++;
        if(count >= 10) { // 1秒
            count = 0;
            // 在这里执行定时任务
        }
    }
}

int main(void) {
    Timer2_Init();
    while(1) {
        // 主循环
    }
}
```

#### 外部中断初始化

```c
#include "gd32f10x.h"

void EXTINT_Init(void) {
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    // 使能SYSCFG时钟
    rcu_periph_clock_enable(RCU_AF);
    
    // 配置PA0为输入
    gpio_init(GPIOA, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_50MHZ, GPIO_PIN_0);
    
    // 配置外部中断线0
    syscfg_exti_line_config(EXTI_SOURCE_GPIOA, EXTI_SOURCE_PIN0);
    
    // 配置外部中断线0为下降沿触发
    exti_init(EXTI_0, EXTI_INTERRUPT, EXTI_TRIG_FALLING);
    exti_interrupt_flag_clear(EXTI_0);
    
    // 配置NVIC
    nvic_irq_enable(EXTI0_IRQn, 2U, 0U);
}

void EXTI0_IRQHandler(void) {
    if(exti_flag_get(EXTI_0)) {
        // 外部中断0处理
        exti_flag_clear(EXTI_0);
    }
}

int main(void) {
    EXTINT_Init();
    while(1) {
        // 主循环
    }
}
```

## HC32系列定时器与中断实现

### HC32F460定时器与中断

HC32F460系列单片机有多个定时器，包括通用定时器（TIM0-TIM3）和实时时钟（RTC）。

#### 定时器0初始化

```c
#include "hc32f460.h"

void Timer0_Init(void) {
    // 使能定时器0时钟
    CLK_FcgPeriphClockCmd(CLK_FCG_TIM0, ENABLE);
    
    // 配置定时器0
    TIM0_DeInit(M0P_TIM0);
    TIM0_Init(M0P_TIM0, TIMER_MODE_UP, 1000, 7200);
    // 解释：
    // 定时器时钟频率 = 72MHz
    // 预分频系数 = 7200-1，所以计数频率 = 72MHz / 7200 = 10kHz
    // 自动重载值 = 1000-1，所以定时周期 = 1000 / 10kHz = 100ms
    
    // 使能定时器0更新中断
    TIM0_IntCmd(M0P_TIM0, TIMER_INT_UP, ENABLE);
    
    // 配置NVIC
    NVIC_ClearPendingIRQ(TIM0_IRQn);
    NVIC_SetPriority(TIM0_IRQn, 2U);
    NVIC_EnableIRQ(TIM0_IRQn);
    
    // 启动定时器0
    TIM0_Cmd(M0P_TIM0, ENABLE);
}

unsigned int count = 0;

void TIM0_IRQHandler(void) {
    if(TIM0_GetIntFlag(M0P_TIM0, TIMER_INT_UP)) {
        TIM0_ClearIntFlag(M0P_TIM0, TIMER_INT_UP);
        count++;
        if(count >= 10) { // 1秒
            count = 0;
            // 在这里执行定时任务
        }
    }
}

int main(void) {
    Timer0_Init();
    while(1) {
        // 主循环
    }
}
```

## MM32系列定时器与中断实现

### MM32F103定时器与中断

MM32F103系列单片机有多个定时器，包括高级定时器（TIM1）、通用定时器（TIM2-TIM4）和基本定时器（TIM6-TIM7）。

#### 定时器3初始化

```c
#include "MM32F103.h"

void Timer3_Init(void) {
    // 使能定时器3时钟
    RCC->APB1ENR |= RCC_APB1ENR_TIM3EN;
    
    // 配置定时器3
    TIM3->PSC = 7199; // 预分频系数7200-1，计数频率=72MHz/7200=10kHz
    TIM3->ARR = 999; // 自动重载值1000-1，定时周期=1000/10kHz=100ms
    TIM3->DIER |= TIM_DIER_UIE; // 使能更新中断
    
    // 配置NVIC
    NVIC_EnableIRQ(TIM3_IRQn);
    NVIC_SetPriority(TIM3_IRQn, 2U);
    
    // 启动定时器3
    TIM3->CR1 |= TIM_CR1_CEN;
}

unsigned int count = 0;

void TIM3_IRQHandler(void) {
    if(TIM3->SR & TIM_SR_UIF) {
        TIM3->SR &= ~TIM_SR_UIF;
        count++;
        if(count >= 10) { // 1秒
            count = 0;
            // 在这里执行定时任务
        }
    }
}

int main(void) {
    Timer3_Init();
    while(1) {
        // 主循环
    }
}
```

## 通用定时器应用示例

### 精确延时函数

```c
#include "gd32f10x.h"

void delay_us(uint32_t us) {
    uint32_t ticks = us * (SystemCoreClock / 1000000);
    uint32_t start = SysTick->VAL;
    while((SysTick->VAL - start) < ticks);
}

void delay_ms(uint32_t ms) {
    for(uint32_t i = 0; i < ms; i++) {
        delay_us(1000);
    }
}

void SysTick_Init(void) {
    // 配置SysTick时钟为系统时钟
    SysTick->CTRL = SysTick_CTRL_CLKSOURCE_Msk | SysTick_CTRL_ENABLE_Msk;
}

int main(void) {
    SysTick_Init();
    
    while(1) {
        // 使用延时函数
        delay_ms(1000);
    }
}
```

### 定时器计数

```c
#include "gd32f10x.h"

void Timer1_Init(void) {
    // 使能定时器1时钟
    rcu_periph_clock_enable(RCU_TIMER1);
    
    // 配置定时器1为计数模式
    timer_deinit(TIMER1);
    timer_init(TIMER1, TIMER_MODE_UP, 65535, 72);
    // 解释：
    // 定时器时钟频率 = 72MHz
    // 预分频系数 = 72-1，所以计数频率 = 72MHz / 72 = 1MHz
    // 自动重载值 = 65535，所以最大计数值为65536
    
    // 启动定时器1
    timer_enable(TIMER1);
}

uint32_t Get_Tick(void) {
    return timer_counter_read(TIMER1);
}

int main(void) {
    Timer1_Init();
    
    uint32_t start = Get_Tick();
    // 执行一些操作
    uint32_t end = Get_Tick();
    uint32_t elapsed = end - start;
    
    while(1) {
        // 主循环
    }
}
```

### 中断优先级管理

```c
#include "gd32f10x.h"

void NVIC_Config(void) {
    // 配置定时器2中断优先级
    nvic_irq_enable(TIMER2_IRQn, 2U, 0U);
    
    // 配置外部中断0中断优先级
    nvic_irq_enable(EXTI0_IRQn, 1U, 0U); // 更高优先级
    
    // 配置USART0中断优先级
    nvic_irq_enable(USART0_IRQn, 3U, 0U); // 更低优先级
}

int main(void) {
    NVIC_Config();
    
    while(1) {
        // 主循环
    }
}
```

## 常见问题与解决方案

### 问题1：定时器中断不触发
- **原因**：可能是定时器没有使能，或者中断没有正确配置
- **解决方案**：检查定时器使能状态，确认中断配置和NVIC设置

### 问题2：定时器定时不准确
- **原因**：可能是时钟频率配置错误，或者预分频系数和自动重载值计算错误
- **解决方案**：检查系统时钟配置，重新计算预分频系数和自动重载值

### 问题3：中断嵌套问题
- **原因**：中断优先级设置不当，导致高优先级中断被低优先级中断打断
- **解决方案**：合理设置中断优先级，避免不必要的中断嵌套

### 问题4：中断处理函数执行时间过长
- **原因**：中断处理函数中执行了耗时操作，影响系统响应
- **解决方案**：中断处理函数应尽量简短，将耗时操作移到主循环中执行

### 问题5：外部中断触发不稳定
- **原因**：可能是外部信号噪声干扰，或者触发方式设置不当
- **解决方案**：增加硬件去抖电路，选择合适的触发方式（上升沿、下降沿或双边沿）

## 最佳实践

1. **定时器选择**：根据应用需求选择合适的定时器，如需要PWM输出选择高级定时器，需要基本定时选择基本定时器
2. **中断优先级**：合理设置中断优先级，确保重要中断能够及时响应
3. **中断处理**：中断处理函数应尽量简短，避免在中断中执行耗时操作
4. **定时器精度**：根据需要的精度选择合适的预分频系数和自动重载值
5. **时钟源选择**：选择稳定的时钟源作为定时器时钟，以确保定时精度
6. **资源管理**：在不需要定时器时，关闭定时器以降低功耗
7. **错误处理**：在中断处理中添加错误检测和处理机制
8. **代码组织**：将定时器和中断相关代码模块化，提高代码可维护性

## 示例项目

### 项目：秒表

#### 功能描述
- 使用定时器实现秒表功能
- 记录经过的时间（时:分:秒.毫秒）
- 通过串口发送时间数据

#### 代码实现

```c
#include "gd32f10x.h"
#include <stdio.h>

typedef struct {
    uint8_t hour;
    uint8_t minute;
    uint8_t second;
    uint16_t millisecond;
} Time;

Time stopwatch = {0, 0, 0, 0};

void Timer2_Init(void) {
    // 使能定时器2时钟
    rcu_periph_clock_enable(RCU_TIMER2);
    
    // 配置定时器2
    timer_deinit(TIMER2);
    timer_init(TIMER2, TIMER_MODE_UP, 10, 7200);
    // 解释：
    // 定时器时钟频率 = 72MHz
    // 预分频系数 = 7200-1，所以计数频率 = 72MHz / 7200 = 10kHz
    // 自动重载值 = 10-1，所以定时周期 = 10 / 10kHz = 1ms
    
    // 使能定时器2更新中断
    timer_interrupt_enable(TIMER2, TIMER_INT_UP);
    
    // 配置NVIC
    nvic_irq_enable(TIMER2_IRQn, 2U, 0U);
    
    // 启动定时器2
    timer_enable(TIMER2);
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

void TIMER2_IRQHandler(void) {
    if(timer_flag_get(TIMER2, TIMER_FLAG_UP)) {
        timer_flag_clear(TIMER2, TIMER_FLAG_UP);
        
        // 更新秒表
        stopwatch.millisecond += 1;
        if(stopwatch.millisecond >= 1000) {
            stopwatch.millisecond = 0;
            stopwatch.second += 1;
            if(stopwatch.second >= 60) {
                stopwatch.second = 0;
                stopwatch.minute += 1;
                if(stopwatch.minute >= 60) {
                    stopwatch.minute = 0;
                    stopwatch.hour += 1;
                    if(stopwatch.hour >= 24) {
                        stopwatch.hour = 0;
                    }
                }
            }
        }
    }
}

int main(void) {
    char buffer[32];
    
    Timer2_Init();
    UART_Init();
    
    while(1) {
        // 每秒发送一次时间
        if(stopwatch.millisecond == 0) {
            sprintf(buffer, "Time: %02d:%02d:%02d.%03d\r\n", 
                    stopwatch.hour, stopwatch.minute, stopwatch.second, stopwatch.millisecond);
            UART_SendString((uint8_t *)buffer);
            delay_ms(1); // 避免重复发送
        }
    }
}
```

### 项目：外部中断触发计数

#### 功能描述
- 使用外部中断检测按键按下
- 每次按键按下时计数器加1
- 通过串口发送计数值

#### 代码实现

```c
#include "gd32f10x.h"
#include <stdio.h>

unsigned int counter = 0;

void EXTINT_Init(void) {
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    // 使能SYSCFG时钟
    rcu_periph_clock_enable(RCU_AF);
    
    // 配置PA0为输入，带上拉
    gpio_init(GPIOA, GPIO_MODE_IPU, GPIO_OSPEED_50MHZ, GPIO_PIN_0);
    
    // 配置外部中断线0
    syscfg_exti_line_config(EXTI_SOURCE_GPIOA, EXTI_SOURCE_PIN0);
    
    // 配置外部中断线0为下降沿触发
    exti_init(EXTI_0, EXTI_INTERRUPT, EXTI_TRIG_FALLING);
    exti_interrupt_flag_clear(EXTI_0);
    
    // 配置NVIC
    nvic_irq_enable(EXTI0_IRQn, 2U, 0U);
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

void EXTI0_IRQHandler(void) {
    if(exti_flag_get(EXTI_0)) {
        // 按键按下，计数器加1
        counter++;
        
        // 发送计数值
        char buffer[32];
        sprintf(buffer, "Counter: %u\r\n", counter);
        UART_SendString((uint8_t *)buffer);
        
        // 清除中断标志
        exti_flag_clear(EXTI_0);
        
        // 简单的软件去抖
        delay_ms(20);
    }
}

int main(void) {
    EXTINT_Init();
    UART_Init();
    
    UART_SendString((uint8_t *)"External interrupt counter ready\r\n");
    
    while(1) {
        // 主循环
    }
}
```

## 总结

定时器与中断是单片机系统中非常重要的组成部分，它们共同实现了系统的时间管理和事件响应。本文档提供了STC、GD32、HC32、MM32等国产单片机的定时器与中断实现方法，包括初始化配置、中断处理、优先级管理等内容。

在实际开发中，应根据具体的应用场景选择合适的定时器和中断配置：
- **定时器选择**：根据需要的功能和精度选择合适的定时器
- **中断优先级**：根据事件的紧急程度设置合适的中断优先级
- **中断处理**：保持中断处理函数简洁高效
- **定时精度**：根据应用需求调整定时器参数

通过本文档的学习，开发者可以掌握国产单片机的定时器与中断技术，为嵌入式系统开发打下坚实的基础。