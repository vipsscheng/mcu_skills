# 电机控制

## 概述

电机是嵌入式系统中常见的执行器，用于将电能转换为机械能。本文档将介绍常见电机的工作原理、控制方法以及在不同系列微控制器上的实现。

## 直流电机控制

### 1. 基本原理
- **特点**：结构简单、控制方便、成本低
- **控制方式**：PWM调速、方向控制
- **驱动电路**：H桥电路

### STC系列微控制器实现

```c
#include "stc8.h"

// 定义电机控制引脚
#define MOTOR_IN1 P2_0
#define MOTOR_IN2 P2_1
#define MOTOR_EN P2_2

// 初始化定时器0用于PWM
void Timer0_Init(void)
{
    TMOD &= 0xF0;  // 清除定时器0模式位
    TMOD |= 0x01;  // 定时器0为模式1（16位定时器）
    TH0 = 0xFC;    // 1ms定时
    TL0 = 0x67;
    ET0 = 1;       // 开启定时器0中断
    EA = 1;        // 开启总中断
    TR0 = 1;       // 启动定时器0
}

// PWM占空比
uint8_t pwm_duty = 0;

// 定时器0中断服务函数
void Timer0_ISR(void) interrupt 1
{
    static uint8_t count = 0;
    TH0 = 0xFC;    // 重新加载初值
    TL0 = 0x67;
    
    count++;
    if(count <= pwm_duty) {
        MOTOR_EN = 1;
    } else {
        MOTOR_EN = 0;
    }
    if(count >= 100) {
        count = 0;
    }
}

// 初始化电机
void Motor_Init(void)
{
    MOTOR_IN1 = 0;
    MOTOR_IN2 = 0;
    MOTOR_EN = 0;
    Timer0_Init();
}

// 设置电机速度和方向
void Motor_SetSpeed(int speed)  // speed: -100 ~ 100
{
    if(speed > 0) {
        // 正转
        MOTOR_IN1 = 1;
        MOTOR_IN2 = 0;
        pwm_duty = speed;
    } else if(speed < 0) {
        // 反转
        MOTOR_IN1 = 0;
        MOTOR_IN2 = 1;
        pwm_duty = -speed;
    } else {
        // 停止
        MOTOR_IN1 = 0;
        MOTOR_IN2 = 0;
        pwm_duty = 0;
    }
}

// 主函数
void main(void)
{
    Motor_Init();
    
    while(1) {
        // 加速
        for(int i = 0; i <= 100; i++) {
            Motor_SetSpeed(i);
            Delay10ms();
        }
        
        // 减速
        for(int i = 100; i >= 0; i--) {
            Motor_SetSpeed(i);
            Delay10ms();
        }
        
        // 反向加速
        for(int i = 0; i >= -100; i--) {
            Motor_SetSpeed(i);
            Delay10ms();
        }
        
        // 反向减速
        for(int i = -100; i <= 0; i++) {
            Motor_SetSpeed(i);
            Delay10ms();
        }
    }
}
```

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

// 定义电机控制引脚
#define MOTOR_IN1_PORT GPIOA
#define MOTOR_IN1_PIN GPIO_PIN_0
#define MOTOR_IN2_PORT GPIOA
#define MOTOR_IN2_PIN GPIO_PIN_1

// 初始化GPIO
void GPIO_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置MOTOR_IN1和MOTOR_IN2为输出
    gpio_mode_set(MOTOR_IN1_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, MOTOR_IN1_PIN);
    gpio_mode_set(MOTOR_IN2_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, MOTOR_IN2_PIN);
    
    // 配置PA8为TIM1_CH1（PWM输出）
    gpio_mode_set(GPIOA, GPIO_MODE_AF, GPIO_PUPD_PULLUP, GPIO_PIN_8);
    gpio_af_set(GPIOA, GPIO_AF_1, GPIO_PIN_8);
    gpio_output_options_set(GPIOA, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_8);
}

// 初始化TIM1用于PWM
void TIM1_Init(void)
{
    // 使能TIM1时钟
    rcu_periph_clock_enable(RCU_TIM1);
    
    // 配置TIM1
    timer_deinit(TIM1);
    timer_prescaler_config(TIM1, 107, TIMER_PSC_RELOAD_NOW);  // 1MHz
    timer_autoreload_value_config(TIM1, 99);  // 10kHz PWM
    
    // 配置CH1为PWM模式
    timer_channel_output_mode_config(TIM1, TIMER_CH_1, TIMER_OC_MODE_PWM0);
    timer_channel_output_pulse_value_config(TIM1, TIMER_CH_1, 0);
    timer_channel_output_shadow_config(TIM1, TIMER_CH_1, TIMER_OC_SHADOW_DISABLE);
    timer_channel_output_enable(TIM1, TIMER_CH_1);
    
    // 启动TIM1
    timer_enable(TIM1);
}

// 初始化电机
void Motor_Init(void)
{
    GPIO_Init();
    TIM1_Init();
}

// 设置电机速度和方向
void Motor_SetSpeed(int speed)  // speed: -100 ~ 100
{
    if(speed > 0) {
        // 正转
        gpio_bit_set(MOTOR_IN1_PORT, MOTOR_IN1_PIN);
        gpio_bit_reset(MOTOR_IN2_PORT, MOTOR_IN2_PIN);
        timer_channel_output_pulse_value_config(TIM1, TIMER_CH_1, speed);
    } else if(speed < 0) {
        // 反转
        gpio_bit_reset(MOTOR_IN1_PORT, MOTOR_IN1_PIN);
        gpio_bit_set(MOTOR_IN2_PORT, MOTOR_IN2_PIN);
        timer_channel_output_pulse_value_config(TIM1, TIMER_CH_1, -speed);
    } else {
        // 停止
        gpio_bit_reset(MOTOR_IN1_PORT, MOTOR_IN1_PIN);
        gpio_bit_reset(MOTOR_IN2_PORT, MOTOR_IN2_PIN);
        timer_channel_output_pulse_value_config(TIM1, TIMER_CH_1, 0);
    }
}

// 主函数
int main(void)
{
    // 系统初始化
    SystemInit();
    
    // 初始化电机
    Motor_Init();
    
    while(1) {
        // 加速
        for(int i = 0; i <= 100; i++) {
            Motor_SetSpeed(i);
            delay_ms(10);
        }
        
        // 减速
        for(int i = 100; i >= 0; i--) {
            Motor_SetSpeed(i);
            delay_ms(10);
        }
        
        // 反向加速
        for(int i = 0; i >= -100; i--) {
            Motor_SetSpeed(i);
            delay_ms(10);
        }
        
        // 反向减速
        for(int i = -100; i <= 0; i++) {
            Motor_SetSpeed(i);
            delay_ms(10);
        }
    }
}
```

## 步进电机控制

### 1. 基本原理
- **特点**：精度高、控制准确、无累积误差
- **控制方式**：脉冲控制、方向控制
- **类型**：二相、四相、五相步进电机

### STC系列微控制器实现

```c
#include "stc8.h"

// 定义步进电机引脚
#define STEP_IN1 P2_0
#define STEP_IN2 P2_1
#define STEP_IN3 P2_2
#define STEP_IN4 P2_3

// 四相步进电机励磁序列（全步）
uint8_t step_sequence[4] = {
    0x01,  // 1000
    0x02,  // 0100
    0x04,  // 0010
    0x08   // 0001
};

// 初始化步进电机
void Stepper_Init(void)
{
    STEP_IN1 = 0;
    STEP_IN2 = 0;
    STEP_IN3 = 0;
    STEP_IN4 = 0;
}

// 单步控制
void Stepper_Step(uint8_t direction)  // 0: 正转, 1: 反转
{
    static uint8_t step_index = 0;
    
    if(direction == 0) {
        // 正转
        step_index = (step_index + 1) % 4;
    } else {
        // 反转
        step_index = (step_index + 3) % 4;
    }
    
    // 设置引脚状态
    STEP_IN1 = (step_sequence[step_index] & 0x01) ? 1 : 0;
    STEP_IN2 = (step_sequence[step_index] & 0x02) ? 1 : 0;
    STEP_IN3 = (step_sequence[step_index] & 0x04) ? 1 : 0;
    STEP_IN4 = (step_sequence[step_index] & 0x08) ? 1 : 0;
}

// 转动指定步数
void Stepper_Rotate(int steps, uint8_t direction, uint16_t delay_ms)
{
    for(int i = 0; i < steps; i++) {
        Stepper_Step(direction);
        Delay1ms(delay_ms);
    }
}

// 主函数
void main(void)
{
    Stepper_Init();
    
    while(1) {
        // 正转100步
        Stepper_Rotate(100, 0, 5);
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        
        // 反转100步
        Stepper_Rotate(100, 1, 5);
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
    }
}
```

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

// 定义步进电机引脚
#define STEP_PORT GPIOA
#define STEP_PIN1 GPIO_PIN_0
#define STEP_PIN2 GPIO_PIN_1
#define STEP_PIN3 GPIO_PIN_2
#define STEP_PIN4 GPIO_PIN_3

// 四相步进电机励磁序列（全步）
uint8_t step_sequence[4] = {
    0x01,  // 1000
    0x02,  // 0100
    0x04,  // 0010
    0x08   // 0001
};

// 初始化GPIO
void GPIO_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置步进电机引脚为输出
    gpio_mode_set(STEP_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, 
                  STEP_PIN1 | STEP_PIN2 | STEP_PIN3 | STEP_PIN4);
    gpio_output_options_set(STEP_PORT, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, 
                           STEP_PIN1 | STEP_PIN2 | STEP_PIN3 | STEP_PIN4);
}

// 初始化步进电机
void Stepper_Init(void)
{
    GPIO_Init();
    // 初始状态
    gpio_bit_reset(STEP_PORT, STEP_PIN1 | STEP_PIN2 | STEP_PIN3 | STEP_PIN4);
}

// 单步控制
void Stepper_Step(uint8_t direction)  // 0: 正转, 1: 反转
{
    static uint8_t step_index = 0;
    
    if(direction == 0) {
        // 正转
        step_index = (step_index + 1) % 4;
    } else {
        // 反转
        step_index = (step_index + 3) % 4;
    }
    
    // 设置引脚状态
    gpio_bit_write(STEP_PORT, STEP_PIN1, (step_sequence[step_index] & 0x01) ? SET : RESET);
    gpio_bit_write(STEP_PORT, STEP_PIN2, (step_sequence[step_index] & 0x02) ? SET : RESET);
    gpio_bit_write(STEP_PORT, STEP_PIN3, (step_sequence[step_index] & 0x04) ? SET : RESET);
    gpio_bit_write(STEP_PORT, STEP_PIN4, (step_sequence[step_index] & 0x08) ? SET : RESET);
}

// 转动指定步数
void Stepper_Rotate(int steps, uint8_t direction, uint16_t delay_ms)
{
    for(int i = 0; i < steps; i++) {
        Stepper_Step(direction);
        delay_ms(delay_ms);
    }
}

// 主函数
int main(void)
{
    // 系统初始化
    SystemInit();
    
    // 初始化步进电机
    Stepper_Init();
    
    while(1) {
        // 正转100步
        Stepper_Rotate(100, 0, 5);
        delay_ms(500);
        
        // 反转100步
        Stepper_Rotate(100, 1, 5);
        delay_ms(500);
    }
}
```

## 伺服电机控制

### 1. 基本原理
- **特点**：精度高、响应快、可控性好
- **控制方式**：PWM信号控制（脉冲宽度决定位置）
- **角度范围**：通常为0-180度

### STC系列微控制器实现

```c
#include "stc8.h"

// 定义伺服电机引脚
#define SERVO_PIN P2_0

// 初始化定时器0用于PWM
void Timer0_Init(void)
{
    TMOD &= 0xF0;  // 清除定时器0模式位
    TMOD |= 0x01;  // 定时器0为模式1（16位定时器）
    TH0 = 0xFF;    // 20ms定时（20000us）
    TL0 = 0x40;
    ET0 = 1;       // 开启定时器0中断
    EA = 1;        // 开启总中断
    TR0 = 1;       // 启动定时器0
}

// PWM脉宽（单位：10us）
uint16_t pwm_pulse = 150;  // 1.5ms，中间位置

// 定时器0中断服务函数
void Timer0_ISR(void) interrupt 1
{
    static uint16_t count = 0;
    TH0 = 0xFF;    // 重新加载初值
    TL0 = 0x40;
    
    count += 10;  // 每次中断10us
    
    if(count <= pwm_pulse) {
        SERVO_PIN = 1;
    } else {
        SERVO_PIN = 0;
    }
    
    if(count >= 2000) {  // 20ms周期
        count = 0;
    }
}

// 初始化伺服电机
void Servo_Init(void)
{
    SERVO_PIN = 0;
    Timer0_Init();
}

// 设置伺服电机角度
void Servo_SetAngle(uint8_t angle)  // 0-180度
{
    // 脉宽范围：0.5ms-2.5ms
    pwm_pulse = 50 + (angle * 100) / 90;  // 转换为10us单位
}

// 主函数
void main(void)
{
    Servo_Init();
    
    while(1) {
        // 从0度到180度
        for(uint8_t i = 0; i <= 180; i++) {
            Servo_SetAngle(i);
            Delay10ms();
        }
        
        // 从180度到0度
        for(uint8_t i = 180; i >= 0; i--) {
            Servo_SetAngle(i);
            Delay10ms();
        }
    }
}
```

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

// 定义伺服电机引脚
#define SERVO_PORT GPIOA
#define SERVO_PIN GPIO_PIN_0

// 初始化TIM2用于PWM
void TIM2_Init(void)
{
    // 使能TIM2时钟
    rcu_periph_clock_enable(RCU_TIM2);
    
    // 配置TIM2
    timer_deinit(TIM2);
    timer_prescaler_config(TIM2, 107, TIMER_PSC_RELOAD_NOW);  // 1MHz
    timer_autoreload_value_config(TIM2, 19999);  // 20ms周期
    
    // 配置CH1为PWM模式
    timer_channel_output_mode_config(TIM2, TIMER_CH_1, TIMER_OC_MODE_PWM0);
    timer_channel_output_pulse_value_config(TIM2, TIMER_CH_1, 1500);  // 1.5ms，中间位置
    timer_channel_output_shadow_config(TIM2, TIMER_CH_1, TIMER_OC_SHADOW_DISABLE);
    timer_channel_output_enable(TIM2, TIMER_CH_1);
    
    // 启动TIM2
    timer_enable(TIM2);
}

// 初始化GPIO
void GPIO_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA0为TIM2_CH1（PWM输出）
    gpio_mode_set(SERVO_PORT, GPIO_MODE_AF, GPIO_PUPD_PULLUP, SERVO_PIN);
    gpio_af_set(SERVO_PORT, GPIO_AF_1, SERVO_PIN);
    gpio_output_options_set(SERVO_PORT, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, SERVO_PIN);
}

// 初始化伺服电机
void Servo_Init(void)
{
    GPIO_Init();
    TIM2_Init();
}

// 设置伺服电机角度
void Servo_SetAngle(uint8_t angle)  // 0-180度
{
    // 脉宽范围：0.5ms-2.5ms
    uint16_t pulse = 500 + (angle * 1000) / 90;  // 转换为us单位
    timer_channel_output_pulse_value_config(TIM2, TIMER_CH_1, pulse);
}

// 主函数
int main(void)
{
    // 系统初始化
    SystemInit();
    
    // 初始化伺服电机
    Servo_Init();
    
    while(1) {
        // 从0度到180度
        for(uint8_t i = 0; i <= 180; i++) {
            Servo_SetAngle(i);
            delay_ms(10);
        }
        
        // 从180度到0度
        for(uint8_t i = 180; i >= 0; i--) {
            Servo_SetAngle(i);
            delay_ms(10);
        }
    }
}
```

## 电机控制应用示例

### 1. 智能小车控制系统

**功能说明**：使用直流电机控制小车的前进、后退、左转、右转。

**硬件需求**：
- 微控制器开发板
- 直流电机（2个）
- L298N电机驱动模块
-  wheels and chassis

**软件设计**：
- 初始化电机驱动
- 实现基本运动控制函数
- 响应用户输入或传感器数据

**实现代码**：

```c
#include "stc8.h"

// 定义电机控制引脚
#define MOTOR1_IN1 P2_0
#define MOTOR1_IN2 P2_1
#define MOTOR1_EN P2_2
#define MOTOR2_IN1 P2_3
#define MOTOR2_IN2 P2_4
#define MOTOR2_EN P2_5

// 初始化定时器0用于PWM
void Timer0_Init(void)
{
    TMOD &= 0xF0;  // 清除定时器0模式位
    TMOD |= 0x01;  // 定时器0为模式1（16位定时器）
    TH0 = 0xFC;    // 1ms定时
    TL0 = 0x67;
    ET0 = 1;       // 开启定时器0中断
    EA = 1;        // 开启总中断
    TR0 = 1;       // 启动定时器0
}

// PWM占空比
uint8_t pwm_duty1 = 0;
uint8_t pwm_duty2 = 0;

// 定时器0中断服务函数
void Timer0_ISR(void) interrupt 1
{
    static uint8_t count = 0;
    TH0 = 0xFC;    // 重新加载初值
    TL0 = 0x67;
    
    count++;
    if(count <= pwm_duty1) {
        MOTOR1_EN = 1;
    } else {
        MOTOR1_EN = 0;
    }
    if(count <= pwm_duty2) {
        MOTOR2_EN = 1;
    } else {
        MOTOR2_EN = 0;
    }
    if(count >= 100) {
        count = 0;
    }
}

// 初始化电机
void Motor_Init(void)
{
    MOTOR1_IN1 = 0;
    MOTOR1_IN2 = 0;
    MOTOR1_EN = 0;
    MOTOR2_IN1 = 0;
    MOTOR2_IN2 = 0;
    MOTOR2_EN = 0;
    Timer0_Init();
}

// 设置电机速度
void SetMotorSpeed(int speed1, int speed2)
{
    // 电机1
    if(speed1 > 0) {
        MOTOR1_IN1 = 1;
        MOTOR1_IN2 = 0;
        pwm_duty1 = speed1;
    } else if(speed1 < 0) {
        MOTOR1_IN1 = 0;
        MOTOR1_IN2 = 1;
        pwm_duty1 = -speed1;
    } else {
        MOTOR1_IN1 = 0;
        MOTOR1_IN2 = 0;
        pwm_duty1 = 0;
    }
    
    // 电机2
    if(speed2 > 0) {
        MOTOR2_IN1 = 1;
        MOTOR2_IN2 = 0;
        pwm_duty2 = speed2;
    } else if(speed2 < 0) {
        MOTOR2_IN1 = 0;
        MOTOR2_IN2 = 1;
        pwm_duty2 = -speed2;
    } else {
        MOTOR2_IN1 = 0;
        MOTOR2_IN2 = 0;
        pwm_duty2 = 0;
    }
}

// 前进
void Car_Forward(uint8_t speed)
{
    SetMotorSpeed(speed, speed);
}

// 后退
void Car_Backward(uint8_t speed)
{
    SetMotorSpeed(-speed, -speed);
}

// 左转
void Car_Left(uint8_t speed)
{
    SetMotorSpeed(-speed, speed);
}

// 右转
void Car_Right(uint8_t speed)
{
    SetMotorSpeed(speed, -speed);
}

// 停止
void Car_Stop(void)
{
    SetMotorSpeed(0, 0);
}

// 主函数
void main(void)
{
    Motor_Init();
    
    while(1) {
        // 前进
        Car_Forward(80);
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        
        // 停止
        Car_Stop();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        
        // 后退
        Car_Backward(80);
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        
        // 停止
        Car_Stop();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        
        // 左转
        Car_Left(80);
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        
        // 停止
        Car_Stop();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        
        // 右转
        Car_Right(80);
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        
        // 停止
        Car_Stop();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
    }
}
```

### 2. 机械臂控制系统

**功能说明**：使用伺服电机控制机械臂的多个关节，实现抓取和放置物体的功能。

**硬件需求**：
- 微控制器开发板
- 伺服电机（多个）
- 机械臂结构

**软件设计**：
- 初始化伺服电机
- 实现关节控制函数
- 定义抓取和放置动作

**实现代码**：

```c
#include "gd32f4xx.h"

// 定义伺服电机引脚
#define SERVO1_PORT GPIOA
#define SERVO1_PIN GPIO_PIN_0
#define SERVO2_PORT GPIOA
#define SERVO2_PIN GPIO_PIN_1
#define SERVO3_PORT GPIOA
#define SERVO3_PIN GPIO_PIN_2

// 初始化TIM2用于PWM
void TIM2_Init(void)
{
    // 使能TIM2时钟
    rcu_periph_clock_enable(RCU_TIM2);
    
    // 配置TIM2
    timer_deinit(TIM2);
    timer_prescaler_config(TIM2, 107, TIMER_PSC_RELOAD_NOW);  // 1MHz
    timer_autoreload_value_config(TIM2, 19999);  // 20ms周期
    
    // 配置CH1为PWM模式
    timer_channel_output_mode_config(TIM2, TIMER_CH_1, TIMER_OC_MODE_PWM0);
    timer_channel_output_pulse_value_config(TIM2, TIMER_CH_1, 1500);  // 1.5ms，中间位置
    timer_channel_output_shadow_config(TIM2, TIMER_CH_1, TIMER_OC_SHADOW_DISABLE);
    timer_channel_output_enable(TIM2, TIMER_CH_1);
    
    // 配置CH2为PWM模式
    timer_channel_output_mode_config(TIM2, TIMER_CH_2, TIMER_OC_MODE_PWM0);
    timer_channel_output_pulse_value_config(TIM2, TIMER_CH_2, 1500);  // 1.5ms，中间位置
    timer_channel_output_shadow_config(TIM2, TIMER_CH_2, TIMER_OC_SHADOW_DISABLE);
    timer_channel_output_enable(TIM2, TIMER_CH_2);
    
    // 配置CH3为PWM模式
    timer_channel_output_mode_config(TIM2, TIMER_CH_3, TIMER_OC_MODE_PWM0);
    timer_channel_output_pulse_value_config(TIM2, TIMER_CH_3, 1500);  // 1.5ms，中间位置
    timer_channel_output_shadow_config(TIM2, TIMER_CH_3, TIMER_OC_SHADOW_DISABLE);
    timer_channel_output_enable(TIM2, TIMER_CH_3);
    
    // 启动TIM2
    timer_enable(TIM2);
}

// 初始化GPIO
void GPIO_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA0为TIM2_CH1（PWM输出）
    gpio_mode_set(SERVO1_PORT, GPIO_MODE_AF, GPIO_PUPD_PULLUP, SERVO1_PIN);
    gpio_af_set(SERVO1_PORT, GPIO_AF_1, SERVO1_PIN);
    
    // 配置PA1为TIM2_CH2（PWM输出）
    gpio_mode_set(SERVO2_PORT, GPIO_MODE_AF, GPIO_PUPD_PULLUP, SERVO2_PIN);
    gpio_af_set(SERVO2_PORT, GPIO_AF_1, SERVO2_PIN);
    
    // 配置PA2为TIM2_CH3（PWM输出）
    gpio_mode_set(SERVO3_PORT, GPIO_MODE_AF, GPIO_PUPD_PULLUP, SERVO3_PIN);
    gpio_af_set(SERVO3_PORT, GPIO_AF_1, SERVO3_PIN);
    
    // 配置GPIO输出速度
    gpio_output_options_set(GPIOA, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, 
                           SERVO1_PIN | SERVO2_PIN | SERVO3_PIN);
}

// 初始化伺服电机
void Servo_Init(void)
{
    GPIO_Init();
    TIM2_Init();
}

// 设置伺服电机角度
void Servo_SetAngle(uint8_t servo, uint8_t angle)  // 0-180度
{
    // 脉宽范围：0.5ms-2.5ms
    uint16_t pulse = 500 + (angle * 1000) / 90;  // 转换为us单位
    
    switch(servo) {
        case 1:
            timer_channel_output_pulse_value_config(TIM2, TIMER_CH_1, pulse);
            break;
        case 2:
            timer_channel_output_pulse_value_config(TIM2, TIMER_CH_2, pulse);
            break;
        case 3:
            timer_channel_output_pulse_value_config(TIM2, TIMER_CH_3, pulse);
            break;
    }
}

// 机械臂抓取动作
void Arm_Grab(void)
{
    // 移动到抓取位置
    Servo_SetAngle(1, 90);  // 底座
    delay_ms(500);
    Servo_SetAngle(2, 45);  // 大臂
    delay_ms(500);
    Servo_SetAngle(3, 180); // 爪子打开
    delay_ms(500);
    
    // 抓取
    Servo_SetAngle(2, 90);  // 大臂下降
    delay_ms(500);
    Servo_SetAngle(3, 0);    // 爪子闭合
    delay_ms(500);
    Servo_SetAngle(2, 45);  // 大臂上升
    delay_ms(500);
}

// 机械臂放置动作
void Arm_Place(void)
{
    // 移动到放置位置
    Servo_SetAngle(1, 180); // 底座旋转
    delay_ms(500);
    Servo_SetAngle(2, 90);  // 大臂下降
    delay_ms(500);
    Servo_SetAngle(3, 180); // 爪子打开
    delay_ms(500);
    
    // 复位
    Servo_SetAngle(2, 45);  // 大臂上升
    delay_ms(500);
    Servo_SetAngle(1, 90);  // 底座复位
    delay_ms(500);
}

// 主函数
int main(void)
{
    // 系统初始化
    SystemInit();
    
    // 初始化伺服电机
    Servo_Init();
    
    while(1) {
        // 抓取动作
        Arm_Grab();
        delay_ms(1000);
        
        // 放置动作
        Arm_Place();
        delay_ms(1000);
    }
}
```

## 常见问题与解决方案

### 1. 电机不转
- **症状**：电机没有任何反应
- **解决方案**：检查电源、检查接线、检查驱动电路、检查控制信号

### 2. 电机转速不稳定
- **症状**：电机转速忽快忽慢
- **解决方案**：检查电源稳定性、优化PWM控制、检查机械负载

### 3. 步进电机失步
- **症状**：步进电机转动角度不准确
- **解决方案**：降低转速、增加驱动电流、检查机械负载

### 4. 伺服电机抖动
- **症状**：伺服电机在目标位置附近抖动
- **解决方案**：检查PWM信号质量、调整控制参数、检查电源稳定性

### 5. 电机发热严重
- **症状**：电机温度过高
- **解决方案**：检查负载是否过大、检查驱动电流是否合适、增加散热措施

## 总结

电机控制是嵌入式系统中的重要组成部分，不同类型的电机适用于不同的应用场景。本文档介绍了直流电机、步进电机和伺服电机的工作原理、控制方法以及在不同系列微控制器上的实现。

通过本章节的学习，您应该能够：
1. 了解常见电机的基本原理和特点
2. 在不同系列微控制器上实现电机控制
3. 设计基于电机的控制系统
4. 解决电机控制过程中的常见问题
5. 开发完整的电机应用系统