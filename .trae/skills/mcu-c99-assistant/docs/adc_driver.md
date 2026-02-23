# ADC采集

## 概述

ADC（Analog-to-Digital Converter）是模数转换器的缩写，用于将模拟信号转换为数字信号。在单片机中，ADC广泛应用于传感器数据采集、信号处理、电池电压监测等场景。本文档将详细介绍国产单片机的ADC采集实现方法，包括初始化配置、采样模式、数据读取等。

## 基本概念

- **分辨率**：ADC能够区分的最小电压变化，通常以位为单位，如12位ADC的分辨率为1/4096
- **参考电压**：ADC转换的基准电压，决定了输入电压的测量范围
- **采样率**：ADC每秒能够完成的采样次数，单位为Hz
- **转换时间**：完成一次ADC转换所需的时间
- **通道**：ADC可以采集的输入通道数量

## STC系列ADC实现

### STC12C5A60S2 ADC实现

STC12C5A60S2内置了8通道10位ADC。

```c
#include <STC12C5A60S2.h>

void ADC_Init(void) {
    // 配置ADC引脚
    P1M0 &= ~0xFF; // P1口设为准双向口
    P1M1 &= ~0xFF;
    
    // 配置ADC
    ADC_CONTR = 0x80; // 使能ADC
    ADC_CONTR |= 0x00; // 速度控制，00: 90个时钟周期
}

unsigned int ADC_Read(uint8_t channel) {
    // 选择通道（0-7对应P1.0-P1.7）
    ADC_CONTR &= 0xF8; // 清除通道选择
    ADC_CONTR |= channel & 0x07;
    
    // 启动AD转换
    ADC_CONTR |= 0x08;
    
    // 等待转换完成
    while(!(ADC_CONTR & 0x10));
    
    // 清除转换完成标志
    ADC_CONTR &= ~0x10;
    
    // 返回转换结果（10位）
    return (ADC_RES << 2) | (ADC_RESL & 0x03);
}

void main() {
    unsigned int adc_value;
    ADC_Init();
    
    while(1) {
        // 读取P1.0通道的ADC值
        adc_value = ADC_Read(0);
        // 可以在这里处理ADC值
    }
}
```

## GD32系列ADC实现

### GD32F103 ADC实现

GD32F103系列单片机内置了12位ADC，支持多通道采集。

```c
#include "gd32f10x.h"

void ADC_Init(void) {
    // 使能ADC0时钟
    rcu_periph_clock_enable(RCU_ADC0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA0为模拟输入
    gpio_init(GPIOA, GPIO_MODE_AIN, GPIO_OSPEED_50MHZ, GPIO_PIN_0);
    
    // 配置ADC0
    adc_deinit(ADC0);
    adc_mode_config(ADC_MODE_FREE);
    adc_special_function_config(ADC0, ADC_SCAN_MODE, DISABLE);
    adc_data_alignment_config(ADC0, ADC_DATAALIGN_RIGHT);
    adc_channel_length_config(ADC0, ADC_REGULAR_CHANNEL, 1);
    
    // 配置ADC0的通道0，采样时间为13.5个周期
    adc_regular_channel_config(ADC0, 0, ADC_CHANNEL_0, ADC_SAMPLETIME_13POINT5);
    
    // 使能ADC0
    adc_enable(ADC0);
    
    // 校准ADC0
    adc_calibration_enable(ADC0);
}

unsigned int ADC_Read(void) {
    // 启动ADC转换
    adc_software_trigger_enable(ADC0, ADC_REGULAR_CHANNEL);
    
    // 等待转换完成
    while(!adc_flag_get(ADC0, ADC_FLAG_EOC));
    
    // 清除转换完成标志
    adc_flag_clear(ADC0, ADC_FLAG_EOC);
    
    // 返回转换结果
    return adc_regular_data_read(ADC0);
}

int main(void) {
    unsigned int adc_value;
    ADC_Init();
    
    while(1) {
        adc_value = ADC_Read();
        // 可以在这里处理ADC值
    }
}
```

## HC32系列ADC实现

### HC32F460 ADC实现

HC32F460系列单片机内置了12位ADC，支持多通道采集。

```c
#include "hc32f460.h"

void ADC_Init(void) {
    // 使能ADC时钟
    CLK_FcgPeriphClockCmd(CLK_FCG_ADC, ENABLE);
    // 使能GPIOA时钟
    CLK_FcgPeriphClockCmd(CLK_FCG_GPIOA, ENABLE);
    
    // 配置PA0为模拟输入
    GPIO_SetFunc(GPIO_PORT_A, GPIO_PIN_0, GPIO_FUNC_1);
    
    // 配置ADC
    ADC_DeInit();
    ADC_TriggerConfig(ADC_TRIG_SOFTWARE);
    ADC_SampleTimeConfig(ADC_SAMPLE_TIME_128);
    ADC_DataAlignConfig(ADC_DATAALIGN_RIGHT);
    ADC_ChannelConfig(ADC_REGULAR_CHANNEL, ADC_CH_0, ENABLE);
    
    // 使能ADC
    ADC_Cmd(ENABLE);
    
    // 校准ADC
    ADC_Calibration();
}

unsigned int ADC_Read(void) {
    // 启动ADC转换
    ADC_SoftwareTriggerCmd(ENABLE);
    
    // 等待转换完成
    while(!ADC_GetFlagStatus(ADC_FLAG_EOC));
    
    // 清除转换完成标志
    ADC_ClearFlagStatus(ADC_FLAG_EOC);
    
    // 返回转换结果
    return ADC_GetConversionValue();
}

int main(void) {
    unsigned int adc_value;
    ADC_Init();
    
    while(1) {
        adc_value = ADC_Read();
        // 可以在这里处理ADC值
    }
}
```

## MM32系列ADC实现

### MM32F103 ADC实现

MM32F103系列单片机内置了12位ADC，支持多通道采集。

```c
#include "MM32F103.h"

void ADC_Init(void) {
    // 使能ADC1时钟
    RCC->APB2ENR |= RCC_APB2ENR_ADC1EN;
    // 使能GPIOA时钟
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN;
    
    // 配置PA0为模拟输入
    GPIOA->CRL &= ~(0xF << 0);
    GPIOA->CRL |= (0x0 << 0); // 模拟输入
    
    // 配置ADC1
    ADC1->CR2 |= ADC_CR2_ADON; // 使能ADC1
    
    // 校准ADC1
    ADC1->CR2 |= ADC_CR2_CAL;
    while(ADC1->CR2 & ADC_CR2_CAL); // 等待校准完成
    
    // 配置通道0
    ADC1->SQR3 &= ~(0x1F);
    ADC1->SQR3 |= 0x00; // 通道0
    ADC1->SMPR2 &= ~(0x7);
    ADC1->SMPR2 |= (0x3); // 采样时间15个周期
}

unsigned int ADC_Read(void) {
    // 启动ADC转换
    ADC1->CR2 |= ADC_CR2_SWSTART;
    
    // 等待转换完成
    while(!(ADC1->SR & ADC_SR_EOC));
    
    // 返回转换结果
    return ADC1->DR;
}

int main(void) {
    unsigned int adc_value;
    ADC_Init();
    
    while(1) {
        adc_value = ADC_Read();
        // 可以在这里处理ADC值
    }
}
```

## 通用ADC应用示例

### 电压测量

```c
#include "gd32f10x.h"

#define VREF 3.3 // 参考电压3.3V
#define ADC_RESOLUTION 4096 // 12位ADC

void ADC_Init(void) {
    // 使能ADC0时钟
    rcu_periph_clock_enable(RCU_ADC0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA0为模拟输入
    gpio_init(GPIOA, GPIO_MODE_AIN, GPIO_OSPEED_50MHZ, GPIO_PIN_0);
    
    // 配置ADC0
    adc_deinit(ADC0);
    adc_mode_config(ADC_MODE_FREE);
    adc_special_function_config(ADC0, ADC_SCAN_MODE, DISABLE);
    adc_data_alignment_config(ADC0, ADC_DATAALIGN_RIGHT);
    adc_channel_length_config(ADC0, ADC_REGULAR_CHANNEL, 1);
    
    // 配置ADC0的通道0，采样时间为13.5个周期
    adc_regular_channel_config(ADC0, 0, ADC_CHANNEL_0, ADC_SAMPLETIME_13POINT5);
    
    // 使能ADC0
    adc_enable(ADC0);
    
    // 校准ADC0
    adc_calibration_enable(ADC0);
}

float ADC_ReadVoltage(void) {
    // 启动ADC转换
    adc_software_trigger_enable(ADC0, ADC_REGULAR_CHANNEL);
    
    // 等待转换完成
    while(!adc_flag_get(ADC0, ADC_FLAG_EOC));
    
    // 清除转换完成标志
    adc_flag_clear(ADC0, ADC_FLAG_EOC);
    
    // 读取ADC值
    unsigned int adc_value = adc_regular_data_read(ADC0);
    
    // 计算电压
    float voltage = (float)adc_value * VREF / ADC_RESOLUTION;
    
    return voltage;
}

int main(void) {
    float voltage;
    ADC_Init();
    
    while(1) {
        voltage = ADC_ReadVoltage();
        // 可以在这里处理电压值
    }
}
```

### 温度传感器采集

```c
#include "gd32f10x.h"

// 假设使用NTC热敏电阻
#define NTC_R1 10000 // 串联电阻10kΩ
#define NTC_B 3950   // B值
#define NTC_R25 10000 // 25℃时的电阻10kΩ

void ADC_Init(void) {
    // 使能ADC0时钟
    rcu_periph_clock_enable(RCU_ADC0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA0为模拟输入
    gpio_init(GPIOA, GPIO_MODE_AIN, GPIO_OSPEED_50MHZ, GPIO_PIN_0);
    
    // 配置ADC0
    adc_deinit(ADC0);
    adc_mode_config(ADC_MODE_FREE);
    adc_special_function_config(ADC0, ADC_SCAN_MODE, DISABLE);
    adc_data_alignment_config(ADC0, ADC_DATAALIGN_RIGHT);
    adc_channel_length_config(ADC0, ADC_REGULAR_CHANNEL, 1);
    
    // 配置ADC0的通道0，采样时间为13.5个周期
    adc_regular_channel_config(ADC0, 0, ADC_CHANNEL_0, ADC_SAMPLETIME_13POINT5);
    
    // 使能ADC0
    adc_enable(ADC0);
    
    // 校准ADC0
    adc_calibration_enable(ADC0);
}

float ADC_ReadTemperature(void) {
    // 启动ADC转换
    adc_software_trigger_enable(ADC0, ADC_REGULAR_CHANNEL);
    
    // 等待转换完成
    while(!adc_flag_get(ADC0, ADC_FLAG_EOC));
    
    // 清除转换完成标志
    adc_flag_clear(ADC0, ADC_FLAG_EOC);
    
    // 读取ADC值
    unsigned int adc_value = adc_regular_data_read(ADC0);
    
    // 计算NTC电阻
    float voltage = (float)adc_value * 3.3 / 4096;
    float ntc_resistance = NTC_R1 * voltage / (3.3 - voltage);
    
    // 计算温度
    float temperature = 1.0 / (1.0/298.15 + log(ntc_resistance/NTC_R25)/NTC_B) - 273.15;
    
    return temperature;
}

int main(void) {
    float temperature;
    ADC_Init();
    
    while(1) {
        temperature = ADC_ReadTemperature();
        // 可以在这里处理温度值
    }
}
```

### 多通道ADC采集

```c
#include "gd32f10x.h"

#define CHANNEL_NUM 3

void ADC_Init(void) {
    // 使能ADC0时钟
    rcu_periph_clock_enable(RCU_ADC0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA0、PA1、PA2为模拟输入
    gpio_init(GPIOA, GPIO_MODE_AIN, GPIO_OSPEED_50MHZ, GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2);
    
    // 配置ADC0
    adc_deinit(ADC0);
    adc_mode_config(ADC_MODE_FREE);
    adc_special_function_config(ADC0, ADC_SCAN_MODE, ENABLE);
    adc_data_alignment_config(ADC0, ADC_DATAALIGN_RIGHT);
    adc_channel_length_config(ADC0, ADC_REGULAR_CHANNEL, CHANNEL_NUM);
    
    // 配置ADC0的通道0、1、2，采样时间为13.5个周期
    adc_regular_channel_config(ADC0, 0, ADC_CHANNEL_0, ADC_SAMPLETIME_13POINT5);
    adc_regular_channel_config(ADC0, 1, ADC_CHANNEL_1, ADC_SAMPLETIME_13POINT5);
    adc_regular_channel_config(ADC0, 2, ADC_CHANNEL_2, ADC_SAMPLETIME_13POINT5);
    
    // 使能ADC0
    adc_enable(ADC0);
    
    // 校准ADC0
    adc_calibration_enable(ADC0);
}

void ADC_ReadMultiChannel(unsigned int *values) {
    // 启动ADC转换
    adc_software_trigger_enable(ADC0, ADC_REGULAR_CHANNEL);
    
    // 等待转换完成
    while(!adc_flag_get(ADC0, ADC_FLAG_EOC));
    
    // 清除转换完成标志
    adc_flag_clear(ADC0, ADC_FLAG_EOC);
    
    // 读取ADC值
    for(uint8_t i = 0; i < CHANNEL_NUM; i++) {
        values[i] = adc_regular_data_read(ADC0);
    }
}

int main(void) {
    unsigned int adc_values[CHANNEL_NUM];
    ADC_Init();
    
    while(1) {
        ADC_ReadMultiChannel(adc_values);
        // 可以在这里处理多通道ADC值
    }
}
```

## 常见问题与解决方案

### 问题1：ADC采集值不稳定
- **原因**：可能是电源噪声、信号干扰或采样时间不足
- **解决方案**：增加电源滤波，使用屏蔽线缆，增加采样时间，多次采样取平均值

### 问题2：ADC采集值与实际值不符
- **原因**：参考电压设置错误，或者ADC校准不正确
- **解决方案**：检查参考电压配置，重新校准ADC

### 问题3：ADC转换速度慢
- **原因**：采样时间设置过长，或者ADC时钟频率过低
- **解决方案**：适当减少采样时间，提高ADC时钟频率

### 问题4：多通道采集时通道间干扰
- **原因**：通道间存在串扰，或者切换通道后采样时间不足
- **解决方案**：增加通道切换后的采样时间，使用屏蔽措施

## 最佳实践

1. **采样时间选择**：根据信号的噪声水平选择合适的采样时间，噪声大的信号需要更长的采样时间
2. **参考电压选择**：根据输入信号的范围选择合适的参考电压，以获得最佳分辨率
3. **电源管理**：确保ADC的电源稳定，使用稳压电路和滤波电容
4. **信号调理**：对于小信号，使用运放进行放大，以提高测量精度
5. **校准**：定期校准ADC，以确保测量的准确性
6. **多通道管理**：在多通道采集中，合理安排通道切换顺序和采样时间
7. **中断使用**：对于需要实时性的应用，使用ADC中断来处理转换完成事件
8. **数据处理**：对采集的数据进行滤波处理，如移动平均、中值滤波等

## 示例项目

### 项目：电池电压监测

#### 功能描述
- 使用ADC监测电池电压
- 当电压低于阈值时，触发报警
- 通过串口发送电压数据

#### 代码实现

```c
#include "gd32f10x.h"
#include <stdio.h>

#define VREF 3.3 // 参考电压3.3V
#define ADC_RESOLUTION 4096 // 12位ADC
#define BATTERY_THRESHOLD 3.0 // 电池电压阈值

void ADC_Init(void) {
    // 使能ADC0时钟
    rcu_periph_clock_enable(RCU_ADC0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA0为模拟输入
    gpio_init(GPIOA, GPIO_MODE_AIN, GPIO_OSPEED_50MHZ, GPIO_PIN_0);
    
    // 配置ADC0
    adc_deinit(ADC0);
    adc_mode_config(ADC_MODE_FREE);
    adc_special_function_config(ADC0, ADC_SCAN_MODE, DISABLE);
    adc_data_alignment_config(ADC0, ADC_DATAALIGN_RIGHT);
    adc_channel_length_config(ADC0, ADC_REGULAR_CHANNEL, 1);
    
    // 配置ADC0的通道0，采样时间为13.5个周期
    adc_regular_channel_config(ADC0, 0, ADC_CHANNEL_0, ADC_SAMPLETIME_13POINT5);
    
    // 使能ADC0
    adc_enable(ADC0);
    
    // 校准ADC0
    adc_calibration_enable(ADC0);
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

float ADC_ReadVoltage(void) {
    // 启动ADC转换
    adc_software_trigger_enable(ADC0, ADC_REGULAR_CHANNEL);
    
    // 等待转换完成
    while(!adc_flag_get(ADC0, ADC_FLAG_EOC));
    
    // 清除转换完成标志
    adc_flag_clear(ADC0, ADC_FLAG_EOC);
    
    // 读取ADC值
    unsigned int adc_value = adc_regular_data_read(ADC0);
    
    // 计算电压
    float voltage = (float)adc_value * VREF / ADC_RESOLUTION;
    
    return voltage;
}

int main(void) {
    float voltage;
    char buffer[64];
    
    ADC_Init();
    UART_Init();
    
    while(1) {
        voltage = ADC_ReadVoltage();
        
        // 发送电压数据
        sprintf(buffer, "Battery voltage: %.2fV\r\n", voltage);
        UART_SendString((uint8_t *)buffer);
        
        // 检查电池电压
        if(voltage < BATTERY_THRESHOLD) {
            UART_SendString((uint8_t *)"Battery low! Please charge.\r\n");
        }
        
        delay_ms(1000);
    }
}
```

### 项目：环境监测系统

#### 功能描述
- 使用ADC采集温度、湿度和光照强度
- 通过串口发送监测数据
- 实现数据滤波处理

#### 代码实现

```c
#include "gd32f10x.h"
#include <stdio.h>

#define VREF 3.3 // 参考电压3.3V
#define ADC_RESOLUTION 4096 // 12位ADC

// 滤波参数
#define FILTER_SIZE 10

void ADC_Init(void) {
    // 使能ADC0时钟
    rcu_periph_clock_enable(RCU_ADC0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA0、PA1、PA2为模拟输入
    gpio_init(GPIOA, GPIO_MODE_AIN, GPIO_OSPEED_50MHZ, GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2);
    
    // 配置ADC0
    adc_deinit(ADC0);
    adc_mode_config(ADC_MODE_FREE);
    adc_special_function_config(ADC0, ADC_SCAN_MODE, ENABLE);
    adc_data_alignment_config(ADC0, ADC_DATAALIGN_RIGHT);
    adc_channel_length_config(ADC0, ADC_REGULAR_CHANNEL, 3);
    
    // 配置ADC0的通道0、1、2，采样时间为13.5个周期
    adc_regular_channel_config(ADC0, 0, ADC_CHANNEL_0, ADC_SAMPLETIME_13POINT5);
    adc_regular_channel_config(ADC0, 1, ADC_CHANNEL_1, ADC_SAMPLETIME_13POINT5);
    adc_regular_channel_config(ADC0, 2, ADC_CHANNEL_2, ADC_SAMPLETIME_13POINT5);
    
    // 使能ADC0
    adc_enable(ADC0);
    
    // 校准ADC0
    adc_calibration_enable(ADC0);
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

// 移动平均滤波
unsigned int moving_average(unsigned int new_value, unsigned int *buffer, uint8_t *index) {
    buffer[*index] = new_value;
    *index = (*index + 1) % FILTER_SIZE;
    
    unsigned int sum = 0;
    for(uint8_t i = 0; i < FILTER_SIZE; i++) {
        sum += buffer[i];
    }
    
    return sum / FILTER_SIZE;
}

void ADC_ReadSensors(float *temperature, float *humidity, float *light) {
    unsigned int adc_values[3];
    static unsigned int temp_buffer[FILTER_SIZE] = {0};
    static unsigned int humi_buffer[FILTER_SIZE] = {0};
    static unsigned int light_buffer[FILTER_SIZE] = {0};
    static uint8_t temp_index = 0;
    static uint8_t humi_index = 0;
    static uint8_t light_index = 0;
    
    // 启动ADC转换
    adc_software_trigger_enable(ADC0, ADC_REGULAR_CHANNEL);
    
    // 等待转换完成
    while(!adc_flag_get(ADC0, ADC_FLAG_EOC));
    
    // 清除转换完成标志
    adc_flag_clear(ADC0, ADC_FLAG_EOC);
    
    // 读取ADC值
    for(uint8_t i = 0; i < 3; i++) {
        adc_values[i] = adc_regular_data_read(ADC0);
    }
    
    // 滤波处理
    unsigned int filtered_temp = moving_average(adc_values[0], temp_buffer, &temp_index);
    unsigned int filtered_humi = moving_average(adc_values[1], humi_buffer, &humi_index);
    unsigned int filtered_light = moving_average(adc_values[2], light_buffer, &light_index);
    
    // 转换为实际值
    *temperature = (float)filtered_temp * VREF / ADC_RESOLUTION * 100;
    *humidity = (float)filtered_humi * VREF / ADC_RESOLUTION * 100;
    *light = (float)filtered_light * VREF / ADC_RESOLUTION * 1000;
}

int main(void) {
    float temperature, humidity, light;
    char buffer[128];
    
    ADC_Init();
    UART_Init();
    
    while(1) {
        ADC_ReadSensors(&temperature, &humidity, &light);
        
        // 发送监测数据
        sprintf(buffer, "Temperature: %.1f°C, Humidity: %.1f%%, Light: %.0flx\r\n", 
                temperature, humidity, light);
        UART_SendString((uint8_t *)buffer);
        
        delay_ms(1000);
    }
}
```

## 总结

ADC是单片机中非常重要的外设，用于将模拟信号转换为数字信号。本文档提供了STC、GD32、HC32、MM32等国产单片机的ADC实现方法，包括单通道和多通道采集、电压测量、温度传感器采集等应用示例。

在实际开发中，应根据具体的应用场景选择合适的ADC配置：
- **采样时间**：根据信号噪声水平选择
- **参考电压**：根据输入信号范围选择
- **采样率**：根据信号变化速度选择
- **滤波方法**：根据信号特性选择

同时，应注意电源稳定、信号调理、校准等方面，以确保ADC采集的准确性和稳定性。通过本文档的学习，开发者可以掌握国产单片机的ADC采集技术，为嵌入式系统开发打下坚实的基础。