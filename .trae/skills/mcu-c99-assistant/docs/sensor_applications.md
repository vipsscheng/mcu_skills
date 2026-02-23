# 传感器应用

## 概述

传感器是嵌入式系统中获取外部环境信息的重要组件，它们能够将物理量转换为电信号，为系统提供决策依据。本文档将介绍常见传感器的工作原理、接口方式以及在不同系列微控制器上的应用实现。

## 温度传感器

### 1. DS18B20 数字温度传感器
- **特点**：单总线接口、精度高、抗干扰能力强
- **测量范围**：-55℃ 至 +125℃
- **精度**：±0.5℃（-10℃ 至 +85℃）

### STC系列微控制器实现

```c
#include "stc8.h"

#define DQ P3_7

// 延时函数
void Delay10us(void)
{
    uint8_t i = 2;
    while(i--);
}

// 初始化DS18B20
bit DS18B20_Init(void)
{
    bit ack;
    DQ = 1;
    Delay10us();
    DQ = 0;
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    DQ = 1;
    Delay10us();
    Delay10us();
    ack = DQ;
    Delay10us();
    Delay10us();
    return ack;
}

// 写入一个字节
void DS18B20_WriteByte(uint8_t byte)
{
    uint8_t i;
    for(i = 0; i < 8; i++) {
        DQ = 0;
        Delay10us();
        DQ = byte & 0x01;
        Delay10us();
        DQ = 1;
        Delay10us();
        byte >>= 1;
    }
}

// 读取一个字节
uint8_t DS18B20_ReadByte(void)
{
    uint8_t i, byte = 0;
    for(i = 0; i < 8; i++) {
        DQ = 0;
        Delay10us();
        DQ = 1;
        Delay10us();
        byte >>= 1;
        if(DQ) {
            byte |= 0x80;
        }
        Delay10us();
    }
    return byte;
}

// 读取温度
float DS18B20_ReadTemperature(void)
{
    uint8_t low, high;
    int16_t temp;
    float temperature;
    
    DS18B20_Init();
    DS18B20_WriteByte(0xCC);  // 跳过ROM
    DS18B20_WriteByte(0x44);  // 开始转换
    
    // 等待转换完成
    while(!DS18B20_Init());
    
    DS18B20_Init();
    DS18B20_WriteByte(0xCC);  // 跳过ROM
    DS18B20_WriteByte(0xBE);  // 读取温度
    
    low = DS18B20_ReadByte();  // 低字节
    high = DS18B20_ReadByte();  // 高字节
    
    temp = (high << 8) | low;
    temperature = temp * 0.0625;
    
    return temperature;
}

// 主函数
void main(void)
{
    float temp;
    while(1) {
        temp = DS18B20_ReadTemperature();
        // 处理温度数据
        Delay10ms();
    }
}
```

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

#define DQ_GPIO_PORT GPIOA
#define DQ_GPIO_PIN GPIO_PIN_0

// 延时函数
void Delay1us(void)
{
    uint8_t i = 1;
    while(i--);
}

// 初始化DS18B20
uint8_t DS18B20_Init(void)
{
    uint8_t ack;
    
    // 配置为输出
    gpio_mode_set(DQ_GPIO_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, DQ_GPIO_PIN);
    
    // 发送复位脉冲
    gpio_bit_reset(DQ_GPIO_PORT, DQ_GPIO_PIN);
    for(uint16_t i = 0; i < 500; i++) Delay1us();  // 480us
    
    // 释放总线
    gpio_bit_set(DQ_GPIO_PORT, DQ_GPIO_PIN);
    for(uint16_t i = 0; i < 60; i++) Delay1us();  // 60us
    
    // 配置为输入
    gpio_mode_set(DQ_GPIO_PORT, GPIO_MODE_INPUT, GPIO_PUPD_PULLUP, DQ_GPIO_PIN);
    
    // 读取应答
    ack = gpio_input_bit_get(DQ_GPIO_PORT, DQ_GPIO_PIN);
    
    // 等待总线恢复
    for(uint16_t i = 0; i < 500; i++) Delay1us();  // 480us
    
    return ack;
}

// 写入一个字节
void DS18B20_WriteByte(uint8_t byte)
{
    uint8_t i;
    
    for(i = 0; i < 8; i++) {
        // 拉低总线
        gpio_mode_set(DQ_GPIO_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, DQ_GPIO_PIN);
        gpio_bit_reset(DQ_GPIO_PORT, DQ_GPIO_PIN);
        Delay1us();
        
        // 写入位
        if(byte & 0x01) {
            gpio_bit_set(DQ_GPIO_PORT, DQ_GPIO_PIN);
        } else {
            gpio_bit_reset(DQ_GPIO_PORT, DQ_GPIO_PIN);
        }
        
        // 保持45us
        for(uint8_t j = 0; j < 45; j++) Delay1us();
        
        // 释放总线
        gpio_bit_set(DQ_GPIO_PORT, DQ_GPIO_PIN);
        Delay1us();
        
        byte >>= 1;
    }
}

// 读取一个字节
uint8_t DS18B20_ReadByte(void)
{
    uint8_t i, byte = 0;
    
    for(i = 0; i < 8; i++) {
        // 拉低总线
        gpio_mode_set(DQ_GPIO_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, DQ_GPIO_PIN);
        gpio_bit_reset(DQ_GPIO_PORT, DQ_GPIO_PIN);
        Delay1us();
        
        // 释放总线
        gpio_bit_set(DQ_GPIO_PORT, DQ_GPIO_PIN);
        Delay1us();
        
        // 配置为输入
        gpio_mode_set(DQ_GPIO_PORT, GPIO_MODE_INPUT, GPIO_PUPD_PULLUP, DQ_GPIO_PIN);
        
        // 读取位
        byte >>= 1;
        if(gpio_input_bit_get(DQ_GPIO_PORT, DQ_GPIO_PIN)) {
            byte |= 0x80;
        }
        
        // 保持45us
        for(uint8_t j = 0; j < 45; j++) Delay1us();
    }
    
    return byte;
}

// 读取温度
float DS18B20_ReadTemperature(void)
{
    uint8_t low, high;
    int16_t temp;
    float temperature;
    
    DS18B20_Init();
    DS18B20_WriteByte(0xCC);  // 跳过ROM
    DS18B20_WriteByte(0x44);  // 开始转换
    
    // 等待转换完成
    while(!DS18B20_Init());
    
    DS18B20_Init();
    DS18B20_WriteByte(0xCC);  // 跳过ROM
    DS18B20_WriteByte(0xBE);  // 读取温度
    
    low = DS18B20_ReadByte();  // 低字节
    high = DS18B20_ReadByte();  // 高字节
    
    temp = (high << 8) | low;
    temperature = temp * 0.0625;
    
    return temperature;
}
```

## 温湿度传感器

### 1. DHT11 温湿度传感器
- **特点**：单总线接口、低成本、响应快
- **测量范围**：温度 0℃-50℃，湿度 20%-90%RH
- **精度**：温度 ±2℃，湿度 ±5%RH

### STC系列微控制器实现

```c
#include "stc8.h"

#define DHT11_PIN P3_7

// 延时函数
void Delay10us(void)
{
    uint8_t i = 2;
    while(i--);
}

// 初始化DHT11
bit DHT11_Init(void)
{
    bit ack;
    
    // 发送开始信号
    DHT11_PIN = 0;
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    
    DHT11_PIN = 1;
    Delay10us();
    Delay10us();
    
    // 读取应答
    ack = DHT11_PIN;
    while(!DHT11_PIN);
    while(DHT11_PIN);
    
    return !ack;
}

// 读取一个字节
uint8_t DHT11_ReadByte(void)
{
    uint8_t i, byte = 0;
    for(i = 0; i < 8; i++) {
        while(!DHT11_PIN);
        Delay10us();
        Delay10us();
        byte <<= 1;
        if(DHT11_PIN) {
            byte |= 0x01;
        }
        while(DHT11_PIN);
    }
    return byte;
}

// 读取温湿度
bit DHT11_ReadData(uint8_t *temperature, uint8_t *humidity)
{
    uint8_t buf[5];
    uint8_t i;
    
    if(!DHT11_Init()) {
        return 0;
    }
    
    for(i = 0; i < 5; i++) {
        buf[i] = DHT11_ReadByte();
    }
    
    // 校验
    if(buf[0] + buf[1] + buf[2] + buf[3] == buf[4]) {
        *humidity = buf[0];
        *temperature = buf[2];
        return 1;
    } else {
        return 0;
    }
}
```

### 2. SHT30 数字温湿度传感器
- **特点**：I2C接口、高精度、低功耗
- **测量范围**：温度 -40℃-125℃，湿度 0%-100%RH
- **精度**：温度 ±0.3℃，湿度 ±2%RH

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

#define SHT30_ADDR 0x44

// 初始化I2C
void I2C_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOB);
    // 使能I2C0时钟
    rcu_periph_clock_enable(RCU_I2C0);
    
    // 配置PB6为I2C0_SCL
    gpio_af_set(GPIOB, GPIO_AF_4, GPIO_PIN_6);
    // 配置PB7为I2C0_SDA
    gpio_af_set(GPIOB, GPIO_AF_4, GPIO_PIN_7);
    
    // 配置GPIO
    gpio_mode_set(GPIOB, GPIO_MODE_AF, GPIO_PUPD_PULLUP, GPIO_PIN_6 | GPIO_PIN_7);
    gpio_output_options_set(GPIOB, GPIO_OTYPE_OD, GPIO_OSPEED_50MHZ, GPIO_PIN_6 | GPIO_PIN_7);
    
    // 配置I2C0
    i2c_deinit(I2C0);
    i2c_clock_config(I2C0, 100000, I2C_DTCY_2);
    i2c_mode_addr_config(I2C0, I2C_I2CMODE_ENABLE, I2C_ADDFORMAT_7BITS, 0x00);
    i2c_enable(I2C0);
}

// 向SHT30写入命令
void SHT30_WriteCommand(uint16_t command)
{
    // 等待总线空闲
    while(i2c_flag_get(I2C0, I2C_FLAG_I2CBSY));
    
    // 发送起始信号
    i2c_start_on_bus(I2C0);
    while(!i2c_flag_get(I2C0, I2C_FLAG_SBSEND));
    
    // 发送设备地址
    i2c_master_addressing(I2C0, SHT30_ADDR << 1, I2C_TRANSMITTER);
    while(!i2c_flag_get(I2C0, I2C_FLAG_ADDSEND));
    i2c_flag_clear(I2C0, I2C_FLAG_ADDSEND);
    
    // 发送命令高字节
    i2c_data_transmit(I2C0, (command >> 8) & 0xFF);
    while(!i2c_flag_get(I2C0, I2C_FLAG_TBE));
    
    // 发送命令低字节
    i2c_data_transmit(I2C0, command & 0xFF);
    while(!i2c_flag_get(I2C0, I2C_FLAG_TBE));
    
    // 发送停止信号
    i2c_stop_on_bus(I2C0);
    while(i2c_flag_get(I2C0, I2C_FLAG_STPDET));
}

// 从SHT30读取数据
void SHT30_ReadData(float *temperature, float *humidity)
{
    uint8_t data[6];
    
    // 发送测量命令
    SHT30_WriteCommand(0x2400);  // 单次测量，高重复性
    
    // 等待测量完成
    delay_ms(10);
    
    // 等待总线空闲
    while(i2c_flag_get(I2C0, I2C_FLAG_I2CBSY));
    
    // 发送起始信号
    i2c_start_on_bus(I2C0);
    while(!i2c_flag_get(I2C0, I2C_FLAG_SBSEND));
    
    // 发送设备地址（读取模式）
    i2c_master_addressing(I2C0, SHT30_ADDR << 1, I2C_RECEIVER);
    while(!i2c_flag_get(I2C0, I2C_FLAG_ADDSEND));
    i2c_flag_clear(I2C0, I2C_FLAG_ADDSEND);
    
    // 接收数据
    for(uint8_t i = 0; i < 5; i++) {
        while(!i2c_flag_get(I2C0, I2C_FLAG_RBNE));
        data[i] = i2c_data_receive(I2C0);
        i2c_ack_config(I2C0, I2C_ACK_ENABLE);
    }
    
    // 接收最后一个字节
    while(!i2c_flag_get(I2C0, I2C_FLAG_RBNE));
    data[5] = i2c_data_receive(I2C0);
    i2c_ack_config(I2C0, I2C_ACK_DISABLE);
    
    // 发送停止信号
    i2c_stop_on_bus(I2C0);
    while(i2c_flag_get(I2C0, I2C_FLAG_STPDET));
    
    // 计算温度和湿度
    uint16_t temp_raw = (data[0] << 8) | data[1];
    uint16_t hum_raw = (data[3] << 8) | data[4];
    
    *temperature = -45 + 175 * (float)temp_raw / 65535;
    *humidity = 100 * (float)hum_raw / 65535;
}
```

## 光照传感器

### 1. BH1750 数字光照传感器
- **特点**：I2C接口、高精度、宽量程
- **测量范围**：1-65535 lx
- **精度**：±20%

### STC系列微控制器实现

```c
#include "stc8.h"

#define SCL P3_2
#define SDA P3_3
#define BH1750_ADDR 0x23

// 延时函数
void I2C_Delay(void)
{
    uint8_t i = 10;
    while(i--);
}

// 初始化I2C
void I2C_Init(void)
{
    SCL = 1;
    SDA = 1;
}

// 启动I2C
void I2C_Start(void)
{
    SDA = 1;
    SCL = 1;
    I2C_Delay();
    SDA = 0;
    I2C_Delay();
    SCL = 0;
}

// 停止I2C
void I2C_Stop(void)
{
    SDA = 0;
    SCL = 1;
    I2C_Delay();
    SDA = 1;
    I2C_Delay();
}

// 发送应答
void I2C_SendAck(uint8_t ack)
{
    SDA = ack;
    SCL = 1;
    I2C_Delay();
    SCL = 0;
    I2C_Delay();
}

// 接收应答
uint8_t I2C_ReceiveAck(void)
{
    uint8_t ack;
    SDA = 1;
    SCL = 1;
    I2C_Delay();
    ack = SDA;
    SCL = 0;
    I2C_Delay();
    return ack;
}

// 发送字节
void I2C_SendByte(uint8_t byte)
{
    uint8_t i;
    for(i = 0; i < 8; i++) {
        SDA = (byte & 0x80) >> 7;
        SCL = 1;
        I2C_Delay();
        SCL = 0;
        I2C_Delay();
        byte <<= 1;
    }
}

// 接收字节
uint8_t I2C_ReceiveByte(void)
{
    uint8_t i, byte = 0;
    for(i = 0; i < 8; i++) {
        SCL = 1;
        I2C_Delay();
        byte <<= 1;
        byte |= SDA;
        SCL = 0;
        I2C_Delay();
    }
    return byte;
}

// 向BH1750写入命令
void BH1750_WriteCommand(uint8_t command)
{
    I2C_Start();
    I2C_SendByte(BH1750_ADDR << 1);  // 写入模式
    I2C_ReceiveAck();
    I2C_SendByte(command);
    I2C_ReceiveAck();
    I2C_Stop();
}

// 从BH1750读取数据
uint16_t BH1750_ReadLight(void)
{
    uint8_t high, low;
    uint16_t light;
    
    // 发送测量命令
    BH1750_WriteCommand(0x10);  // 连续高分辨率模式
    
    // 等待测量完成
    Delay10ms();
    
    // 读取数据
    I2C_Start();
    I2C_SendByte((BH1750_ADDR << 1) | 0x01);  // 读取模式
    I2C_ReceiveAck();
    high = I2C_ReceiveByte();
    I2C_SendAck(0);
    low = I2C_ReceiveByte();
    I2C_SendAck(1);
    I2C_Stop();
    
    // 计算光照强度
    light = (high << 8) | low;
    light = light / 1.2;
    
    return light;
}
```

## 加速度传感器

### 1. ADXL345 数字加速度传感器
- **特点**：SPI/I2C接口、低功耗、三轴测量
- **测量范围**：±2g/±4g/±8g/±16g
- **精度**：13位分辨率

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

#define ADXL345_CS_PORT GPIOA
#define ADXL345_CS_PIN GPIO_PIN_4
#define ADXL345_SPI SPI0

// 初始化SPI
void SPI_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    // 使能SPI0时钟
    rcu_periph_clock_enable(RCU_SPI0);
    
    // 配置PA5为SPI0_SCK
    gpio_af_set(GPIOA, GPIO_AF_5, GPIO_PIN_5);
    // 配置PA6为SPI0_MISO
    gpio_af_set(GPIOA, GPIO_AF_5, GPIO_PIN_6);
    // 配置PA7为SPI0_MOSI
    gpio_af_set(GPIOA, GPIO_AF_5, GPIO_PIN_7);
    // 配置PA4为CS
    gpio_mode_set(GPIOA, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, GPIO_PIN_4);
    
    // 配置GPIO
    gpio_mode_set(GPIOA, GPIO_MODE_AF, GPIO_PUPD_PULLUP, GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7);
    gpio_output_options_set(GPIOA, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_4 | GPIO_PIN_5 | GPIO_PIN_7);
    
    // 配置SPI0
    spi_deinit(SPI0);
    spi_init(SPI0, SPI_MODE_MASTER, SPI_TRANSMODE_FULLDUPLEX, SPI_FRAMESIZE_8BIT, SPI_NSS_SOFT, 128);
    spi_enable(SPI0);
    
    // 初始化解选
    GPIO_BOP(GPIOA) = GPIO_PIN_4;
}

// SPI发送接收字节
uint8_t SPI_Transfer(uint8_t data)
{
    // 等待发送缓冲区为空
    while(RESET == spi_flag_get(SPI0, SPI_FLAG_TBE));
    // 发送数据
    spi_data_transmit(SPI0, data);
    // 等待接收缓冲区非空
    while(RESET == spi_flag_get(SPI0, SPI_FLAG_RBNE));
    // 接收数据
    return spi_data_receive(SPI0);
}

// 向ADXL345写入寄存器
void ADXL345_WriteRegister(uint8_t reg, uint8_t value)
{
    // 使能片选
    GPIO_BC(GPIOA) = GPIO_PIN_4;
    // 发送寄存器地址（写模式）
    SPI_Transfer(reg);
    // 发送数据
    SPI_Transfer(value);
    // 禁用片选
    GPIO_BOP(GPIOA) = GPIO_PIN_4;
}

// 从ADXL345读取寄存器
uint8_t ADXL345_ReadRegister(uint8_t reg)
{
    uint8_t value;
    // 使能片选
    GPIO_BC(GPIOA) = GPIO_PIN_4;
    // 发送寄存器地址（读模式）
    SPI_Transfer(reg | 0x80);
    // 读取数据
    value = SPI_Transfer(0xFF);
    // 禁用片选
    GPIO_BOP(GPIOA) = GPIO_PIN_4;
    return value;
}

// 从ADXL345读取多个寄存器
void ADXL345_ReadRegisters(uint8_t reg, uint8_t *data, uint8_t length)
{
    // 使能片选
    GPIO_BC(GPIOA) = GPIO_PIN_4;
    // 发送寄存器地址（读模式，多字节）
    SPI_Transfer(reg | 0x80 | 0x40);
    // 读取数据
    for(uint8_t i = 0; i < length; i++) {
        data[i] = SPI_Transfer(0xFF);
    }
    // 禁用片选
    GPIO_BOP(GPIOA) = GPIO_PIN_4;
}

// 初始化ADXL345
void ADXL345_Init(void)
{
    // 进入测量模式
    ADXL345_WriteRegister(0x2D, 0x08);
    // 设置量程为±16g
    ADXL345_WriteRegister(0x31, 0x03);
}

// 读取加速度数据
void ADXL345_ReadAccel(int16_t *x, int16_t *y, int16_t *z)
{
    uint8_t data[6];
    ADXL345_ReadRegisters(0x32, data, 6);
    *x = (int16_t)((data[1] << 8) | data[0]);
    *y = (int16_t)((data[3] << 8) | data[2]);
    *z = (int16_t)((data[5] << 8) | data[4]);
}
```

## 气体传感器

### 1. MQ-2 烟雾传感器
- **特点**：模拟输出、灵敏度高、响应快
- **检测范围**：烟雾、液化气、丙烷、丁烷等
- **接口**：模拟输入

### STC系列微控制器实现

```c
#include "stc8.h"

#define MQ2_PIN P1_0

// 初始化ADC
void ADC_Init(void)
{
    P1ASF = 0x01;  // P1.0作为ADC输入
    ADC_CONTR = 0x80;  // 开启ADC电源
    Delay10ms();
}

// 读取ADC值
uint16_t ADC_Read(void)
{
    uint16_t value;
    ADC_CONTR = 0x88;  // 启动ADC转换
    while(!(ADC_CONTR & 0x10));  // 等待转换完成
    value = ADC_RES << 8 | ADC_RESL;
    ADC_CONTR &= ~0x10;  // 清除转换完成标志
    return value;
}

// 读取MQ-2传感器值
uint16_t MQ2_Read(void)
{
    return ADC_Read();
}

// 判断是否有烟雾
bit MQ2_DetectSmoke(void)
{
    uint16_t value = MQ2_Read();
    // 根据实际情况调整阈值
    return value > 500;
}
```

### 2. MQ-135 空气质量传感器
- **特点**：模拟输出、检测多种气体
- **检测范围**：NH3、NOx、酒精、苯、CO2等
- **接口**：模拟输入

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

// 初始化ADC
void ADC_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    // 使能ADC0时钟
    rcu_periph_clock_enable(RCU_ADC0);
    
    // 配置PA0为ADC输入
    gpio_mode_set(GPIOA, GPIO_MODE_ANALOG, GPIO_PUPD_NONE, GPIO_PIN_0);
    
    // 配置ADC
    adc_deinit(ADC0);
    adc_sync_mode_config(ADC_SYNC_MODE_INDEPENDENT);
    adc_data_alignment_config(ADC0, ADC_DATAALIGN_RIGHT);
    adc_channel_length_config(ADC0, ADC_REGULAR_CHANNEL, 1);
    adc_special_function_config(ADC0, ADC_SCAN_MODE, ENABLE);
    adc_external_trigger_source_config(ADC0, ADC_REGULAR_CHANNEL, ADC0_1_2_EXTTRIG_REGULAR_NONE);
    adc_external_trigger_config(ADC0, ADC_REGULAR_CHANNEL, ENABLE);
    adc_enable(ADC0);
    
    // 校准ADC
    adc_calibration_enable(ADC0);
}

// 读取ADC值
uint16_t ADC_Read(uint8_t channel)
{
    // 配置通道
    adc_regular_channel_config(ADC0, 0, channel, ADC_SAMPLETIME_55POINT5);
    
    // 启动转换
    adc_software_trigger_enable(ADC0, ADC_REGULAR_CHANNEL);
    
    // 等待转换完成
    while(!adc_flag_get(ADC0, ADC_FLAG_EOC));
    
    // 清除标志
    adc_flag_clear(ADC0, ADC_FLAG_EOC);
    
    // 返回结果
    return adc_regular_data_read(ADC0);
}

// 读取MQ-135传感器值
uint16_t MQ135_Read(void)
{
    return ADC_Read(ADC_CHANNEL_0);
}

// 计算空气质量指数
uint8_t MQ135_GetAQI(void)
{
    uint16_t value = MQ135_Read();
    // 根据实际情况调整计算方法
    if(value < 1000) return 0;  // 良好
    else if(value < 2000) return 1;  // 一般
    else if(value < 3000) return 2;  // 较差
    else return 3;  // 差
}
```

## 超声波传感器

### 1. HC-SR04 超声波测距模块
- **特点**：非接触测量、精度高、测距范围广
- **测量范围**：2cm-400cm
- **精度**：±0.3cm

### STC系列微控制器实现

```c
#include "stc8.h"

#define TRIG P1_0
#define ECHO P1_1

// 延时函数
void Delay10us(void)
{
    uint8_t i = 2;
    while(i--);
}

// 初始化超声波传感器
void Ultrasonic_Init(void)
{
    TRIG = 0;
    ECHO = 1;
}

// 测量距离
float Ultrasonic_Measure(void)
{
    uint16_t time;
    float distance;
    
    // 发送触发信号
    TRIG = 1;
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    Delay10us();
    TRIG = 0;
    
    // 等待回声
    while(!ECHO);
    
    // 计时
    time = 0;
    while(ECHO) {
        time++;
        Delay10us();
    }
    
    // 计算距离（声速340m/s）
    distance = time * 0.034 / 2;
    
    return distance;
}
```

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

#define TRIG_PORT GPIOA
#define TRIG_PIN GPIO_PIN_0
#define ECHO_PORT GPIOA
#define ECHO_PIN GPIO_PIN_1

// 初始化超声波传感器
void Ultrasonic_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置TRIG为输出
    gpio_mode_set(TRIG_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, TRIG_PIN);
    gpio_output_options_set(TRIG_PORT, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, TRIG_PIN);
    
    // 配置ECHO为输入
    gpio_mode_set(ECHO_PORT, GPIO_MODE_INPUT, GPIO_PUPD_PULLUP, ECHO_PIN);
    
    // 初始状态
    gpio_bit_reset(TRIG_PORT, TRIG_PIN);
}

// 延时函数
void Delay_us(uint32_t us)
{
    uint32_t i = us * (SystemCoreClock / 1000000);
    while(i--);
}

// 测量距离
float Ultrasonic_Measure(void)
{
    uint32_t start_time, end_time, time;
    float distance;
    
    // 发送触发信号
    gpio_bit_set(TRIG_PORT, TRIG_PIN);
    Delay_us(10);
    gpio_bit_reset(TRIG_PORT, TRIG_PIN);
    
    // 等待回声
    while(!gpio_input_bit_get(ECHO_PORT, ECHO_PIN));
    
    // 计时
    start_time = GET_TICK();
    while(gpio_input_bit_get(ECHO_PORT, ECHO_PIN));
    end_time = GET_TICK();
    
    // 计算时间差
    time = end_time - start_time;
    
    // 计算距离（声速340m/s）
    distance = time * 0.034 / 2;
    
    return distance;
}
```

## 传感器数据处理

### 1. 数据滤波

**移动平均滤波**

```c
#define FILTER_SIZE 10

uint16_t filter_buffer[FILTER_SIZE];
uint8_t filter_index = 0;

// 移动平均滤波
uint16_t MovingAverageFilter(uint16_t new_value)
{
    uint32_t sum = 0;
    uint8_t i;
    
    // 存入新值
    filter_buffer[filter_index] = new_value;
    filter_index = (filter_index + 1) % FILTER_SIZE;
    
    // 计算平均值
    for(i = 0; i < FILTER_SIZE; i++) {
        sum += filter_buffer[i];
    }
    
    return sum / FILTER_SIZE;
}
```

**中值滤波**

```c
#define FILTER_SIZE 5

uint16_t filter_buffer[FILTER_SIZE];
uint8_t filter_index = 0;

// 排序函数
void SortArray(uint16_t *array, uint8_t size)
{
    uint8_t i, j;
    uint16_t temp;
    
    for(i = 0; i < size - 1; i++) {
        for(j = i + 1; j < size; j++) {
            if(array[i] > array[j]) {
                temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
        }
    }
}

// 中值滤波
uint16_t MedianFilter(uint16_t new_value)
{
    uint8_t i;
    
    // 存入新值
    filter_buffer[filter_index] = new_value;
    filter_index = (filter_index + 1) % FILTER_SIZE;
    
    // 复制到临时数组
    uint16_t temp[FILTER_SIZE];
    for(i = 0; i < FILTER_SIZE; i++) {
        temp[i] = filter_buffer[i];
    }
    
    // 排序
    SortArray(temp, FILTER_SIZE);
    
    // 返回中值
    return temp[FILTER_SIZE / 2];
}
```

### 2. 数据校准

**线性校准**

```c
// 线性校准
float LinearCalibration(uint16_t raw_value, float raw_min, float raw_max, float cal_min, float cal_max)
{
    return (raw_value - raw_min) * (cal_max - cal_min) / (raw_max - raw_min) + cal_min;
}
```

**多项式校准**

```c
// 多项式校准（二次）
float PolynomialCalibration(uint16_t raw_value, float a, float b, float c)
{
    return a * raw_value * raw_value + b * raw_value + c;
}
```

## 传感器应用示例

### 1. 环境监测系统

**功能说明**：使用温湿度传感器、光照传感器和气体传感器，监测环境参数并通过串口发送数据。

**硬件需求**：
- 微控制器开发板
- DHT11温湿度传感器
- BH1750光照传感器
- MQ-135气体传感器
- 串口模块

**软件设计**：
- 初始化各个传感器
- 定期采集传感器数据
- 对数据进行滤波和校准
- 通过串口发送数据

**实现代码**：

```c
#include "gd32f4xx.h"

// 传感器初始化
void Sensors_Init(void)
{
    DHT11_Init();
    BH1750_Init();
    MQ135_Init();
    UART_Init();
}

// 主函数
int main(void)
{
    // 系统初始化
    SystemInit();
    
    // 传感器初始化
    Sensors_Init();
    
    uint8_t temperature, humidity;
    uint16_t light;
    uint16_t gas;
    
    while(1) {
        // 读取温湿度
        DHT11_ReadData(&temperature, &humidity);
        
        // 读取光照
        light = BH1750_ReadLight();
        
        // 读取气体
        gas = MQ135_Read();
        
        // 发送数据
        char buffer[100];
        sprintf(buffer, "Temp: %dC, Humidity: %d%%, Light: %dlx, Gas: %d\r\n", 
                temperature, humidity, light, gas);
        UART_SendString(buffer);
        
        // 延时
        delay_ms(1000);
    }
}
```

### 2. 智能小车避障系统

**功能说明**：使用超声波传感器检测前方障碍物，控制小车避障。

**硬件需求**：
- 微控制器开发板
- HC-SR04超声波传感器
- 电机驱动模块
- 直流电机

**软件设计**：
- 初始化超声波传感器和电机
- 定期测量距离
- 根据距离控制电机运动

**实现代码**：

```c
#include "stc8.h"

// 电机控制
#define MOTOR1_DIR P2_0
#define MOTOR1_PWM P2_1
#define MOTOR2_DIR P2_2
#define MOTOR2_PWM P2_3

// 初始化电机
void Motor_Init(void)
{
    MOTOR1_DIR = 0;
    MOTOR1_PWM = 0;
    MOTOR2_DIR = 0;
    MOTOR2_PWM = 0;
}

// 控制电机
void Motor_Control(int speed1, int speed2)
{
    // 控制方向
    MOTOR1_DIR = speed1 > 0 ? 1 : 0;
    MOTOR2_DIR = speed2 > 0 ? 1 : 0;
    
    // 控制速度
    // 这里需要根据实际情况实现PWM控制
}

// 主函数
void main(void)
{
    // 初始化
    Ultrasonic_Init();
    Motor_Init();
    
    float distance;
    
    while(1) {
        // 测量距离
        distance = Ultrasonic_Measure();
        
        // 根据距离控制小车
        if(distance > 30) {
            // 前进
            Motor_Control(50, 50);
        } else if(distance > 10) {
            // 减速
            Motor_Control(30, 30);
        } else {
            // 后退并转向
            Motor_Control(-30, 30);
            Delay10ms();
            Delay10ms();
            Delay10ms();
            Delay10ms();
            Delay10ms();
        }
        
        // 延时
        Delay10ms();
    }
}
```

## 常见问题与解决方案

### 1. 传感器数据不稳定
- **症状**：传感器读数波动较大
- **解决方案**：使用滤波算法、增加采样时间、检查电源稳定性

### 2. 传感器无响应
- **症状**：传感器返回固定值或无数据
- **解决方案**：检查接线、检查电源、检查传感器是否损坏

### 3. 传感器精度不足
- **症状**：测量值与实际值偏差较大
- **解决方案**：进行校准、选择更高精度的传感器、改善安装环境

### 4. 传感器功耗过高
- **症状**：系统功耗超出预期
- **解决方案**：选择低功耗传感器、使用休眠模式、优化采样频率

## 总结

传感器是嵌入式系统与外部环境交互的重要桥梁，合理选择和使用传感器可以为系统提供准确的环境信息。本文档介绍了常见传感器的工作原理、接口方式以及在不同系列微控制器上的应用实现，包括温度传感器、温湿度传感器、光照传感器、加速度传感器、气体传感器和超声波传感器等。

通过本章节的学习，您应该能够：
1. 了解常见传感器的基本原理和特点
2. 在不同系列微控制器上实现传感器接口
3. 对传感器数据进行滤波和校准
4. 解决传感器使用过程中的常见问题
5. 设计基于传感器的嵌入式系统应用