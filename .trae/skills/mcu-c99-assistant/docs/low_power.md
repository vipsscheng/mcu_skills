# 低功耗设计

## 概述

低功耗设计是嵌入式系统开发中的重要考虑因素，特别是对于电池供电的设备。通过合理的硬件设计和软件优化，可以显著延长设备的电池寿命，提高系统的可靠性和稳定性。本文档将详细介绍国产单片机的低功耗设计方法，包括低功耗模式、电源管理、唤醒机制等。

## 基本概念

### 低功耗模式

- **休眠模式**：CPU停止工作，部分外设保持运行，可快速唤醒
- **停机模式**：CPU和大部分外设停止工作，功耗较低，唤醒时间较长
- **待机模式**：几乎所有电路停止工作，功耗最低，唤醒时间最长
- **掉电模式**：除了备份域，所有电路停止工作，需要外部唤醒

### 功耗来源

- **动态功耗**：CPU和外设运行时的功耗，与工作频率和电压相关
- **静态功耗**：电路处于空闲状态时的泄漏电流消耗
- **外设功耗**：各外设模块的功耗，如定时器、串口、ADC等
- **唤醒功耗**：从低功耗模式唤醒时的功耗

## STC系列低功耗设计

### STC89C51低功耗模式

STC89C51支持空闲模式和掉电模式。

#### 空闲模式

```c
#include <reg51.h>

void Enter_IdleMode(void) {
    PCON |= 0x01; // 进入空闲模式
}

void main() {
    // 主程序
    while(1) {
        // 执行任务
        
        // 进入空闲模式，可被任何中断唤醒
        Enter_IdleMode();
    }
}
```

#### 掉电模式

```c
#include <reg51.h>

void Enter_PowerDownMode(void) {
    PCON |= 0x02; // 进入掉电模式
}

void main() {
    // 主程序
    while(1) {
        // 执行任务
        
        // 进入掉电模式，只能被外部中断唤醒
        Enter_PowerDownMode();
    }
}

// 外部中断0中断服务程序
void External0_ISR() interrupt 0 {
    // 唤醒后执行的代码
}
```

### STC12C5A60S2低功耗模式

STC12C5A60S2支持空闲模式、掉电模式和停机模式。

#### 低功耗模式配置

```c
#include <STC12C5A60S2.h>

// 进入空闲模式
void Enter_IdleMode(void) {
    PCON |= 0x01;
}

// 进入掉电模式
void Enter_PowerDownMode(void) {
    PCON |= 0x02;
}

// 进入停机模式
void Enter_HaltMode(void) {
    PCON |= 0x04;
}

void main() {
    // 主程序
    while(1) {
        // 执行任务
        
        // 根据需要选择低功耗模式
        Enter_HaltMode();
    }
}
```

## GD32系列低功耗设计

### GD32F103低功耗模式

GD32F103支持睡眠模式、深度睡眠模式和待机模式。

#### 睡眠模式

```c
#include "gd32f10x.h"

void Enter_SleepMode(void) {
    // 进入睡眠模式
    SCB->SCR &= ~SCB_SCR_SLEEPDEEP_Msk;
    __WFI(); // 等待中断
}

int main(void) {
    // 主程序
    while(1) {
        // 执行任务
        
        // 进入睡眠模式，可被任何中断唤醒
        Enter_SleepMode();
    }
}
```

#### 深度睡眠模式

```c
#include "gd32f10x.h"

void Enter_DeepSleepMode(void) {
    // 进入深度睡眠模式
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;
    __WFI(); // 等待中断
}

int main(void) {
    // 主程序
    while(1) {
        // 执行任务
        
        // 进入深度睡眠模式，可被外部中断唤醒
        Enter_DeepSleepMode();
    }
}
```

#### 待机模式

```c
#include "gd32f10x.h"

void Enter_StandbyMode(void) {
    // 配置唤醒源
    rcu_periph_clock_enable(RCU_PMU);
    pmu_to_standby_mode(WFI_CMD);
}

int main(void) {
    // 主程序
    while(1) {
        // 执行任务
        
        // 进入待机模式，只能被WKUP引脚或RTC唤醒
        Enter_StandbyMode();
    }
}
```

## HC32系列低功耗设计

### HC32F460低功耗模式

HC32F460支持运行模式、睡眠模式、深度睡眠模式和停机模式。

#### 睡眠模式

```c
#include "hc32f460.h"

void Enter_SleepMode(void) {
    // 进入睡眠模式
    PWR_EnterSleepMode();
}

int main(void) {
    // 主程序
    while(1) {
        // 执行任务
        
        // 进入睡眠模式，可被任何中断唤醒
        Enter_SleepMode();
    }
}
```

#### 深度睡眠模式

```c
#include "hc32f460.h"

void Enter_DeepSleepMode(void) {
    // 进入深度睡眠模式
    PWR_EnterDeepSleepMode();
}

int main(void) {
    // 主程序
    while(1) {
        // 执行任务
        
        // 进入深度睡眠模式，可被外部中断唤醒
        Enter_DeepSleepMode();
    }
}
```

#### 停机模式

```c
#include "hc32f460.h"

void Enter_StopMode(void) {
    // 进入停机模式
    PWR_EnterStopMode();
}

int main(void) {
    // 主程序
    while(1) {
        // 执行任务
        
        // 进入停机模式，只能被特定唤醒源唤醒
        Enter_StopMode();
    }
}
```

## MM32系列低功耗设计

### MM32F103低功耗模式

MM32F103支持睡眠模式、停止模式和待机模式。

#### 睡眠模式

```c
#include "MM32F103.h"

void Enter_SleepMode(void) {
    // 进入睡眠模式
    SCB->SCR &= ~SCB_SCR_SLEEPDEEP_Msk;
    __WFI(); // 等待中断
}

int main(void) {
    // 主程序
    while(1) {
        // 执行任务
        
        // 进入睡眠模式，可被任何中断唤醒
        Enter_SleepMode();
    }
}
```

#### 停止模式

```c
#include "MM32F103.h"

void Enter_StopMode(void) {
    // 进入停止模式
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;
    PWR->CR |= PWR_CR_PDDS;
    __WFI(); // 等待中断
}

int main(void) {
    // 主程序
    while(1) {
        // 执行任务
        
        // 进入停止模式，可被外部中断唤醒
        Enter_StopMode();
    }
}
```

#### 待机模式

```c
#include "MM32F103.h"

void Enter_StandbyMode(void) {
    // 进入待机模式
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;
    PWR->CR |= PWR_CR_PDDS | PWR_CR_CSBF;
    __WFI(); // 等待中断
}

int main(void) {
    // 主程序
    while(1) {
        // 执行任务
        
        // 进入待机模式，只能被WKUP引脚或RTC唤醒
        Enter_StandbyMode();
    }
}
```

## 通用低功耗设计技巧

### 时钟管理

```c
#include "gd32f10x.h"

void Clock_Optimize(void) {
    // 降低系统时钟频率
    rcu_system_clock_config(RCU_CKSYSCONFIG_HXTAL_8M_PLL_72M); // 可以根据需要选择更低的频率
    
    // 关闭不需要的外设时钟
    rcu_periph_clock_disable(RCU_ADC0);
    rcu_periph_clock_disable(RCU_SPI0);
    rcu_periph_clock_disable(RCU_TIMER0);
}

int main(void) {
    Clock_Optimize();
    
    while(1) {
        // 主程序
    }
}
```

### GPIO管理

```c
#include "gd32f10x.h"

void GPIO_Optimize(void) {
    // 配置未使用的GPIO为输入模式，以降低功耗
    gpio_init(GPIOA, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_2MHZ, GPIO_PIN_ALL);
    gpio_init(GPIOB, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_2MHZ, GPIO_PIN_ALL);
    gpio_init(GPIOC, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_2MHZ, GPIO_PIN_ALL);
    
    // 对于输出GPIO，设置为低电平
    gpio_bit_reset(GPIOA, GPIO_PIN_0);
    gpio_bit_reset(GPIOB, GPIO_PIN_0);
    gpio_bit_reset(GPIOC, GPIO_PIN_0);
}

int main(void) {
    GPIO_Optimize();
    
    while(1) {
        // 主程序
    }
}
```

### 外设管理

```c
#include "gd32f10x.h"

void Peripheral_Optimize(void) {
    // 关闭不需要的外设
    usart_disable(USART0);
    spi_disable(SPI0);
    i2c_disable(I2C0);
    timer_disable(TIMER0);
    adc_disable(ADC0);
}

int main(void) {
    Peripheral_Optimize();
    
    while(1) {
        // 主程序
    }
}
```

### 唤醒机制

```c
#include "gd32f10x.h"

void Wakeup_Init(void) {
    // 配置外部中断作为唤醒源
    rcu_periph_clock_enable(RCU_GPIOA);
    rcu_periph_clock_enable(RCU_AF);
    
    // 配置PA0为输入，带上拉
    gpio_init(GPIOA, GPIO_MODE_IPU, GPIO_OSPEED_50MHZ, GPIO_PIN_0);
    
    // 配置外部中断线0
    syscfg_exti_line_config(EXTI_SOURCE_GPIOA, EXTI_SOURCE_PIN0);
    exti_init(EXTI_0, EXTI_INTERRUPT, EXTI_TRIG_FALLING);
    exti_interrupt_flag_clear(EXTI_0);
    
    // 配置NVIC
    nvic_irq_enable(EXTI0_IRQn, 2U, 0U);
}

void EXTI0_IRQHandler(void) {
    if(exti_flag_get(EXTI_0)) {
        // 唤醒处理
        exti_flag_clear(EXTI_0);
    }
}

int main(void) {
    Wakeup_Init();
    
    while(1) {
        // 执行任务
        
        // 进入低功耗模式
        SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;
        __WFI();
    }
}
```

## 常见问题与解决方案

### 问题1：低功耗模式下无法唤醒
- **原因**：唤醒源未正确配置，或者唤醒中断未使能
- **解决方案**：检查唤醒源配置，确保中断已使能

### 问题2：低功耗模式功耗仍然较高
- **原因**：可能是某些外设未关闭，或者时钟频率过高
- **解决方案**：关闭不需要的外设，降低系统时钟频率

### 问题3：唤醒后系统状态异常
- **原因**：唤醒后某些外设需要重新初始化，或者时钟配置丢失
- **解决方案**：在唤醒后重新初始化必要的外设，恢复时钟配置

### 问题4：低功耗模式切换时间过长
- **原因**：进入低功耗模式前的准备工作过多，或者唤醒后恢复工作过多
- **解决方案**：优化进入和退出低功耗模式的代码，减少不必要的操作

### 问题5：电池寿命仍然不理想
- **原因**：可能是低功耗模式选择不当，或者唤醒频率过高
- **解决方案**：选择更适合的低功耗模式，优化唤醒策略，减少唤醒频率

## 最佳实践

1. **模式选择**：根据应用需求选择合适的低功耗模式，平衡功耗和唤醒速度
2. **时钟管理**：在不需要高性能时，降低系统时钟频率
3. **外设管理**：关闭不需要的外设，只在需要时开启
4. **GPIO管理**：将未使用的GPIO配置为输入模式，减少泄漏电流
5. **唤醒策略**：优化唤醒源和唤醒频率，减少不必要的唤醒
6. **电源管理**：使用合适的电源管理芯片，提高电源转换效率
7. **硬件设计**：选择低功耗的外围器件，优化硬件电路
8. **软件优化**：优化算法和代码结构，减少CPU运行时间

## 示例项目

### 项目：电池供电的环境监测节点

#### 功能描述
- 使用低功耗模式延长电池寿命
- 定期采集温度和湿度数据
- 通过串口发送监测数据
- 支持外部中断唤醒

#### 代码实现

```c
#include "gd32f10x.h"
#include <stdio.h>

#define MEASURE_INTERVAL 60 // 测量间隔（秒）

void System_Init(void) {
    // 时钟配置
    rcu_system_clock_config(RCU_CKSYSCONFIG_HXTAL_8M_PLL_36M); // 降低系统时钟
    
    // GPIO配置
    rcu_periph_clock_enable(RCU_GPIOA);
    gpio_init(GPIOA, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_2MHZ, GPIO_PIN_ALL);
    
    // 串口配置
    rcu_periph_clock_enable(RCU_USART0);
    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_9);
    gpio_init(GPIOA, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_50MHZ, GPIO_PIN_10);
    usart_deinit(USART0);
    usart_baudrate_set(USART0, 9600);
    usart_word_length_set(USART0, USART_WL_8BIT);
    usart_stop_bit_set(USART0, USART_STB_1BIT);
    usart_parity_config(USART0, USART_PM_NONE);
    usart_hardware_flow_cts_config(USART0, USART_CTS_DISABLE);
    usart_hardware_flow_rts_config(USART0, USART_RTS_DISABLE);
    usart_receive_config(USART0, USART_RECEIVE_ENABLE);
    usart_transmit_config(USART0, USART_TRANSMIT_ENABLE);
    usart_enable(USART0);
    
    // ADC配置
    rcu_periph_clock_enable(RCU_ADC0);
    gpio_init(GPIOA, GPIO_MODE_AIN, GPIO_OSPEED_50MHZ, GPIO_PIN_0 | GPIO_PIN_1);
    adc_deinit(ADC0);
    adc_mode_config(ADC_MODE_FREE);
    adc_special_function_config(ADC0, ADC_SCAN_MODE, ENABLE);
    adc_data_alignment_config(ADC0, ADC_DATAALIGN_RIGHT);
    adc_channel_length_config(ADC0, ADC_REGULAR_CHANNEL, 2);
    adc_regular_channel_config(ADC0, 0, ADC_CHANNEL_0, ADC_SAMPLETIME_13POINT5);
    adc_regular_channel_config(ADC0, 1, ADC_CHANNEL_1, ADC_SAMPLETIME_13POINT5);
    adc_enable(ADC0);
    adc_calibration_enable(ADC0);
    
    // 定时器配置
    rcu_periph_clock_enable(RCU_TIMER2);
    timer_deinit(TIMER2);
    timer_init(TIMER2, TIMER_MODE_UP, 1000, 36000); // 1秒定时
    timer_interrupt_enable(TIMER2, TIMER_INT_UP);
    nvic_irq_enable(TIMER2_IRQn, 2U, 0U);
    
    // 外部中断配置
    rcu_periph_clock_enable(RCU_AF);
    syscfg_exti_line_config(EXTI_SOURCE_GPIOA, EXTI_SOURCE_PIN2);
    exti_init(EXTI_2, EXTI_INTERRUPT, EXTI_TRIG_FALLING);
    exti_interrupt_flag_clear(EXTI_2);
    nvic_irq_enable(EXTI2_IRQn, 1U, 0U);
}

void UART_SendString(uint8_t *str) {
    while(*str) {
        usart_data_transmit(USART0, *str++);
        while(RESET == usart_flag_get(USART0, USART_FLAG_TBE));
    }
}

void Measure_Environment(void) {
    // 启动ADC转换
    adc_software_trigger_enable(ADC0, ADC_REGULAR_CHANNEL);
    while(!adc_flag_get(ADC0, ADC_FLAG_EOC));
    adc_flag_clear(ADC0, ADC_FLAG_EOC);
    
    // 读取ADC值
    uint16_t temp_value = adc_regular_data_read(ADC0);
    uint16_t humi_value = adc_regular_data_read(ADC0);
    
    // 转换为实际值
    float temperature = (float)temp_value * 3.3 / 4096 * 100;
    float humidity = (float)humi_value * 3.3 / 4096 * 100;
    
    // 发送数据
    char buffer[64];
    sprintf(buffer, "Temperature: %.1f°C, Humidity: %.1f%%\r\n", temperature, humidity);
    UART_SendString((uint8_t *)buffer);
    
    // 关闭ADC以降低功耗
    adc_disable(ADC0);
    rcu_periph_clock_disable(RCU_ADC0);
}

unsigned int measure_count = 0;

void TIMER2_IRQHandler(void) {
    if(timer_flag_get(TIMER2, TIMER_FLAG_UP)) {
        timer_flag_clear(TIMER2, TIMER_FLAG_UP);
        measure_count++;
        if(measure_count >= MEASURE_INTERVAL) {
            measure_count = 0;
            // 重新开启ADC时钟
            rcu_periph_clock_enable(RCU_ADC0);
            adc_enable(ADC0);
            // 测量环境数据
            Measure_Environment();
        }
    }
}

void EXTI2_IRQHandler(void) {
    if(exti_flag_get(EXTI_2)) {
        // 外部中断唤醒，立即测量
        measure_count = MEASURE_INTERVAL;
        exti_flag_clear(EXTI_2);
    }
}

void Enter_DeepSleep(void) {
    // 关闭不需要的外设
    usart_disable(USART0);
    rcu_periph_clock_disable(RCU_USART0);
    
    // 进入深度睡眠模式
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;
    __WFI();
    
    // 唤醒后重新初始化
    rcu_periph_clock_enable(RCU_USART0);
    usart_enable(USART0);
}

int main(void) {
    System_Init();
    
    UART_SendString((uint8_t *)"Environment monitoring node ready\r\n");
    
    // 第一次测量
    Measure_Environment();
    
    while(1) {
        // 进入低功耗模式
        Enter_DeepSleep();
    }
}
```

### 项目：低功耗遥控器

#### 功能描述
- 使用低功耗模式延长电池寿命
- 检测按键按下
- 通过红外发送控制信号
- 支持自动休眠

#### 代码实现

```c
#include "gd32f10x.h"

#define KEY_PORT GPIOA
#define KEY_PIN GPIO_PIN_0
#define IR_PORT GPIOB
#define IR_PIN GPIO_PIN_0

void System_Init(void) {
    // 时钟配置
    rcu_system_clock_config(RCU_CKSYSCONFIG_HXTAL_8M_PLL_16M); // 降低系统时钟
    
    // GPIO配置
    rcu_periph_clock_enable(RCU_GPIOA);
    rcu_periph_clock_enable(RCU_GPIOB);
    
    // 按键引脚配置
    gpio_init(KEY_PORT, GPIO_MODE_IPU, GPIO_OSPEED_2MHZ, KEY_PIN);
    
    // 红外发射引脚配置
    gpio_init(IR_PORT, GPIO_MODE_OUT_PP, GPIO_OSPEED_2MHZ, IR_PIN);
    gpio_bit_reset(IR_PORT, IR_PIN);
    
    // 外部中断配置
    rcu_periph_clock_enable(RCU_AF);
    syscfg_exti_line_config(EXTI_SOURCE_GPIOA, EXTI_SOURCE_PIN0);
    exti_init(EXTI_0, EXTI_INTERRUPT, EXTI_TRIG_FALLING);
    exti_interrupt_flag_clear(EXTI_0);
    nvic_irq_enable(EXTI0_IRQn, 1U, 0U);
    
    // 定时器配置（用于红外发送）
    rcu_periph_clock_enable(RCU_TIMER0);
    timer_deinit(TIMER0);
    timer_init(TIMER0, TIMER_MODE_UP, 56, 16); // 38kHz载波
    timer_disable(TIMER0);
}

void IR_SendByte(uint8_t byte) {
    // 发送起始位
    gpio_bit_set(IR_PORT, IR_PIN);
    delay_us(9000);
    gpio_bit_reset(IR_PORT, IR_PIN);
    delay_us(4500);
    
    // 发送数据位
    for(uint8_t i = 0; i < 8; i++) {
        if(byte & 0x01) {
            // 逻辑1
            gpio_bit_set(IR_PORT, IR_PIN);
            delay_us(560);
            gpio_bit_reset(IR_PORT, IR_PIN);
            delay_us(1690);
        } else {
            // 逻辑0
            gpio_bit_set(IR_PORT, IR_PIN);
            delay_us(560);
            gpio_bit_reset(IR_PORT, IR_PIN);
            delay_us(560);
        }
        byte >>= 1;
    }
    
    // 发送结束位
    gpio_bit_set(IR_PORT, IR_PIN);
    delay_us(560);
    gpio_bit_reset(IR_PORT, IR_PIN);
}

void IR_SendCommand(uint8_t command) {
    // 发送引导码
    gpio_bit_set(IR_PORT, IR_PIN);
    delay_us(9000);
    gpio_bit_reset(IR_PORT, IR_PIN);
    delay_us(4500);
    
    // 发送地址码
    IR_SendByte(0xFF);
    IR_SendByte(0x00);
    
    // 发送命令码
    IR_SendByte(command);
    IR_SendByte(~command);
    
    // 发送结束码
    gpio_bit_set(IR_PORT, IR_PIN);
    delay_us(560);
    gpio_bit_reset(IR_PORT, IR_PIN);
}

void EXTI0_IRQHandler(void) {
    if(exti_flag_get(EXTI_0)) {
        // 按键按下，发送红外命令
        IR_SendCommand(0x01); // 示例命令
        
        // 软件去抖
        delay_ms(200);
        
        exti_flag_clear(EXTI_0);
    }
}

void Enter_DeepSleep(void) {
    // 关闭不需要的外设
    timer_disable(TIMER0);
    rcu_periph_clock_disable(RCU_TIMER0);
    
    // 进入深度睡眠模式
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;
    __WFI();
    
    // 唤醒后重新初始化
    rcu_periph_clock_enable(RCU_TIMER0);
    timer_init(TIMER0, TIMER_MODE_UP, 56, 16);
}

int main(void) {
    System_Init();
    
    while(1) {
        // 进入低功耗模式
        Enter_DeepSleep();
    }
}
```

## 总结

低功耗设计是嵌入式系统开发中的重要环节，特别是对于电池供电的设备。本文档提供了STC、GD32、HC32、MM32等国产单片机的低功耗实现方法，包括不同低功耗模式的配置、唤醒机制、功耗优化技巧等。

在实际开发中，应根据具体的应用场景选择合适的低功耗策略：
- **模式选择**：根据唤醒速度和功耗要求选择合适的低功耗模式
- **时钟管理**：在不需要高性能时降低系统时钟频率
- **外设管理**：只在需要时开启外设
- **唤醒策略**：优化唤醒源和唤醒频率

通过合理的低功耗设计，可以显著延长设备的电池寿命，提高系统的可靠性和用户体验。通过本文档的学习，开发者可以掌握国产单片机的低功耗设计技术，为嵌入式系统开发打下坚实的基础。