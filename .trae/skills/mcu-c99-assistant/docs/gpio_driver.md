# GPIO控制

## 概述

GPIO（General Purpose Input/Output）是单片机最基本的外设之一，用于实现数字输入和输出功能。本文档将详细介绍国产单片机的GPIO控制方法，包括初始化、配置、输入输出操作等。

## 基本概念

### GPIO端口
- **端口**：一组GPIO引脚的集合，通常用字母表示（如PA、PB等）
- **引脚**：单个GPIO接口，通常用端口+数字表示（如PA0、PB1等）
- **模式**：GPIO的工作模式，包括输入、输出、复用功能等
- **速度**：输出速度，影响信号的上升和下降时间
- **上下拉**：输入模式下的内部电阻配置

## STC系列GPIO控制

### STC89C51 GPIO控制

#### 寄存器说明
- **P0-P3**：四个8位GPIO端口
- **P0**：漏极开路输出，需要外部上拉电阻
- **P1-P3**：准双向口，内部有上拉电阻

#### 基本操作

```c
// 输出操作
P1 = 0x55;      // 设置P1端口为01010101
P1 |= (1 << 0); // 设置P1.0为高电平
P1 &= ~(1 << 1); // 设置P1.1为低电平

// 输入操作
unsigned char value = P2; // 读取P2端口的值
bit pin_state = P3_2; // 读取P3.2引脚的状态
```

#### 示例：LED闪烁

```c
#include <reg51.h>

void delay(unsigned int ms) {
    unsigned int i, j;
    for (i = ms; i > 0; i--) {
        for (j = 110; j > 0; j--);
    }
}

void main() {
    while (1) {
        P1 = 0x00; // 所有LED亮
        delay(500);
        P1 = 0xFF; // 所有LED灭
        delay(500);
    }
}
```

### STC12C5A60S2 GPIO控制

#### 寄存器说明
- **P0-P5**：六个GPIO端口
- **P0M0/P0M1**：P0端口模式控制寄存器
- **P1M0/P1M1**：P1端口模式控制寄存器
- **P2M0/P2M1**：P2端口模式控制寄存器
- **P3M0/P3M1**：P3端口模式控制寄存器
- **P4M0/P4M1**：P4端口模式控制寄存器
- **P5M0/P5M1**：P5端口模式控制寄存器

#### 模式配置
- **00**：准双向口（传统8051端口模式）
- **01**：推挽输出
- **10**：高阻输入
- **11**：开漏输出

#### 示例：GPIO推挽输出配置

```c
#include <STC12C5A60S2.h>

void GPIO_Init() {
    // P1.0-P1.3 推挽输出
    P1M0 = 0x0F;
    P1M1 = 0x00;
    
    // P1.4-P1.7 高阻输入
    P1M0 &= 0x0F;
    P1M1 |= 0xF0;
}

void main() {
    GPIO_Init();
    
    while (1) {
        P1 = 0x0F; // P1.0-P1.3输出高电平
        delay(500);
        P1 = 0x00; // P1.0-P1.3输出低电平
        delay(500);
    }
}
```

## GD32系列GPIO控制

### GD32F103 GPIO控制

#### 寄存器说明
- **GPIOx_CTL0**：端口控制寄存器0（引脚0-7）
- **GPIOx_CTL1**：端口控制寄存器1（引脚8-15）
- **GPIOx_ISTAT**：端口输入状态寄存器
- **GPIOx_OCTL**：端口输出控制寄存器
- **GPIOx_BOP**：端口位操作寄存器
- **GPIOx_BC**：端口位清除寄存器
- **GPIOx_LOCK**：端口锁存寄存器

#### 模式配置
- **0000**：模拟输入
- **0001**：浮空输入
- **0010**：上拉输入
- **0011**：下拉输入
- **0100**：推挽输出，10MHz
- **0101**：推挽输出，2MHz
- **0110**：推挽输出，50MHz
- **0111**：开漏输出，10MHz
- **1000**：开漏输出，2MHz
- **1001**：开漏输出，50MHz
- **1010**：复用推挽输出，10MHz
- **1011**：复用推挽输出，2MHz
- **1100**：复用推挽输出，50MHz
- **1101**：复用开漏输出，10MHz
- **1110**：复用开漏输出，2MHz
- **1111**：复用开漏输出，50MHz

#### 示例：GPIO初始化

```c
#include "gd32f10x.h"

void GPIO_Init(void) {
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA0为推挽输出，50MHz
    gpio_init(GPIOA, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_0);
    
    // 配置PA1为上拉输入
    gpio_init(GPIOA, GPIO_MODE_IPU, GPIO_OSPEED_50MHZ, GPIO_PIN_1);
}

void main(void) {
    GPIO_Init();
    
    while(1) {
        // 读取PA1状态
        if(gpio_input_bit_get(GPIOA, GPIO_PIN_1)) {
            // PA1为高电平，设置PA0为高
            gpio_bit_set(GPIOA, GPIO_PIN_0);
        } else {
            // PA1为低电平，设置PA0为低
            gpio_bit_reset(GPIOA, GPIO_PIN_0);
        }
    }
}
```

## HC32系列GPIO控制

### HC32F460 GPIO控制

#### 寄存器说明
- **PnPC**：端口控制寄存器
- **PnDIR**：端口方向寄存器
- **PnOUT**：端口输出寄存器
- **PnIN**：端口输入寄存器
- **PnPU**：端口上拉寄存器
- **PnPD**：端口下拉寄存器
- **PnDRV**：端口驱动能力寄存器
- **PnOD**：端口开漏寄存器

#### 示例：GPIO配置

```c
#include "hc32f460.h"

void GPIO_Init(void) {
    // 使能GPIO时钟
    CLK_FcgPeriphClockCmd(CLK_FCG_GPIOA | CLK_FCG_GPIOB, ENABLE);
    
    // 配置PA0为输出
    GPIO_SetFunc(GPIO_PORT_A, GPIO_PIN_0, GPIO_FUNC_0);
    GPIO_DirectionConfig(GPIO_PORT_A, GPIO_PIN_0, GPIO_DIR_OUT);
    
    // 配置PB1为输入，带上拉
    GPIO_SetFunc(GPIO_PORT_B, GPIO_PIN_1, GPIO_FUNC_0);
    GPIO_DirectionConfig(GPIO_PORT_B, GPIO_PIN_1, GPIO_DIR_IN);
    GPIO_PullUpConfig(GPIO_PORT_B, GPIO_PIN_1, GPIO_PULLUP_EN);
}

void main(void) {
    GPIO_Init();
    
    while(1) {
        // 读取PB1状态
        if(GPIO_ReadInputPort(GPIO_PORT_B) & GPIO_PIN_1) {
            // PB1为高电平，设置PA0为高
            GPIO_SetOutputHigh(GPIO_PORT_A, GPIO_PIN_0);
        } else {
            // PB1为低电平，设置PA0为低
            GPIO_SetOutputLow(GPIO_PORT_A, GPIO_PIN_0);
        }
    }
}
```

## MM32系列GPIO控制

### MM32F103 GPIO控制

#### 寄存器说明
- **GPIOx_MODER**：端口模式寄存器
- **GPIOx_OTYPER**：端口输出类型寄存器
- **GPIOx_OSPEEDR**：端口输出速度寄存器
- **GPIOx_PUPDR**：端口上拉/下拉寄存器
- **GPIOx_IDR**：端口输入数据寄存器
- **GPIOx_ODR**：端口输出数据寄存器
- **GPIOx_BSRR**：端口位设置/清除寄存器
- **GPIOx_LCKR**：端口配置锁定寄存器
- **GPIOx_AFRL**：端口复用功能低位寄存器
- **GPIOx_AFRH**：端口复用功能高位寄存器

#### 示例：GPIO操作

```c
#include "MM32F103.h"

void GPIO_Init(void) {
    // 使能GPIOA时钟
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN;
    
    // 配置PA0为推挽输出
    GPIOA->MODER &= ~(3 << 0);
    GPIOA->MODER |= (1 << 0);
    GPIOA->OTYPER &= ~(1 << 0);
    GPIOA->OSPEEDR |= (3 << 0);
    
    // 配置PA1为上拉输入
    GPIOA->MODER &= ~(3 << 2);
    GPIOA->PUPDR &= ~(3 << 2);
    GPIOA->PUPDR |= (1 << 2);
}

void main(void) {
    GPIO_Init();
    
    while(1) {
        // 读取PA1状态
        if(GPIOA->IDR & (1 << 1)) {
            // PA1为高电平，设置PA0为高
            GPIOA->BSRR = (1 << 0);
        } else {
            // PA1为低电平，设置PA0为低
            GPIOA->BSRR = (1 << 16);
        }
    }
}
```

## 通用GPIO操作函数

### 位操作宏定义

```c
// 位设置
#define GPIO_SET(port, pin)    (port->BSRR = (1 << pin))

// 位清除
#define GPIO_RESET(port, pin)  (port->BSRR = (1 << (pin + 16)))

// 位读取
#define GPIO_READ(port, pin)   ((port->IDR & (1 << pin)) ? 1 : 0)

// 位翻转
#define GPIO_TOGGLE(port, pin) (port->ODR ^= (1 << pin))
```

### 延时函数

```c
// 简单延时函数
void delay_us(uint32_t us) {
    uint32_t i;
    for(i = 0; i < us * 8; i++);
}

void delay_ms(uint32_t ms) {
    uint32_t i;
    for(i = 0; i < ms; i++) {
        delay_us(1000);
    }
}
```

## 常见问题与解决方案

### 问题1：GPIO输出没有反应
- **原因**：可能是时钟没有使能，或者模式配置错误
- **解决方案**：检查时钟使能，确认GPIO模式配置正确

### 问题2：GPIO输入信号不稳定
- **原因**：可能是没有配置上下拉电阻，或者信号干扰
- **解决方案**：配置适当的上下拉电阻，增加硬件去耦电容

### 问题3：GPIO输出电流不足
- **原因**：可能是驱动能力配置不足，或者负载过大
- **解决方案**：增加驱动能力，或使用外部驱动电路

## 最佳实践

1. **初始化顺序**：先使能时钟，再配置GPIO
2. **端口复用**：注意GPIO的复用功能，避免冲突
3. **电源管理**：不用的GPIO可以配置为输入模式，以降低功耗
4. **信号完整性**：高频信号需要考虑走线长度和阻抗匹配
5. **抗干扰**：关键信号需要增加滤波和屏蔽措施

## 示例项目

### 项目：按键控制LED

#### 硬件连接
- **按键**：连接到PA0（上拉输入）
- **LED**：连接到PA1（推挽输出）

#### 代码实现

```c
#include "gd32f10x.h"

void GPIO_Init(void) {
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA0为上拉输入
    gpio_init(GPIOA, GPIO_MODE_IPU, GPIO_OSPEED_50MHZ, GPIO_PIN_0);
    
    // 配置PA1为推挽输出
    gpio_init(GPIOA, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_1);
}

int main(void) {
    GPIO_Init();
    
    while(1) {
        // 读取按键状态
        if(!gpio_input_bit_get(GPIOA, GPIO_PIN_0)) {
            // 按键按下，点亮LED
            gpio_bit_set(GPIOA, GPIO_PIN_1);
        } else {
            // 按键释放，熄灭LED
            gpio_bit_reset(GPIOA, GPIO_PIN_1);
        }
    }
}
```

### 项目：LED流水灯

#### 硬件连接
- **LED**：连接到P1端口（P1.0-P1.7）

#### 代码实现

```c
#include <STC12C5A60S2.h>

void delay_ms(uint16_t ms) {
    uint16_t i, j;
    for(i = ms; i > 0; i--) {
        for(j = 110; j > 0; j--);
    }
}

void main() {
    // 配置P1端口为推挽输出
    P1M0 = 0xFF;
    P1M1 = 0x00;
    
    uint8_t led = 0x01;
    
    while(1) {
        P1 = led;
        delay_ms(200);
        
        // 左移
        led <<= 1;
        if(led == 0x00) {
            led = 0x01;
        }
    }
}
```

## 总结

GPIO控制是单片机开发的基础，掌握不同系列单片机的GPIO配置方法对于嵌入式系统开发至关重要。本文档提供了STC、GD32、HC32、MM32等国产单片机的GPIO控制方法，包括寄存器配置、代码示例和最佳实践。

在实际开发中，应根据具体的单片机型号和应用场景选择合适的GPIO配置方案，同时注意信号完整性和抗干扰设计，以确保系统的稳定性和可靠性。