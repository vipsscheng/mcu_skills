# I2C/SPI接口

## 概述

I2C（Inter-Integrated Circuit）和SPI（Serial Peripheral Interface）是两种常用的串行通信协议，广泛应用于单片机与外设之间的数据交换。本文档将详细介绍国产单片机的I2C和SPI接口实现方法，包括初始化配置、数据传输、中断处理等。

## I2C接口

### 基本概念

- **I2C总线**：由SCL（时钟线）和SDA（数据线）组成的两线串行总线
- **主从架构**：支持多主多从，通过地址区分不同设备
- **通信速率**：标准模式（100kHz）、快速模式（400kHz）、高速模式（3.4MHz）
- **数据传输**：起始条件、数据传输、停止条件

### STC系列I2C实现

#### STC89C51软件I2C实现

```c
#include <reg51.h>

// 定义I2C引脚
#define SCL P2_0
#define SDA P2_1

// 延时函数
void I2C_Delay(void) {
    unsigned char i;
    for(i = 0; i < 10; i++);
}

// 起始条件
void I2C_Start(void) {
    SDA = 1;
    SCL = 1;
    I2C_Delay();
    SDA = 0;
    I2C_Delay();
    SCL = 0;
}

// 停止条件
void I2C_Stop(void) {
    SDA = 0;
    SCL = 1;
    I2C_Delay();
    SDA = 1;
    I2C_Delay();
}

// 发送应答
void I2C_SendAck(unsigned char ack) {
    SDA = ack;
    SCL = 1;
    I2C_Delay();
    SCL = 0;
    I2C_Delay();
}

// 接收应答
unsigned char I2C_ReceiveAck(void) {
    unsigned char ack;
    SCL = 1;
    I2C_Delay();
    ack = SDA;
    SCL = 0;
    I2C_Delay();
    return ack;
}

// 发送一个字节
void I2C_SendByte(unsigned char byte) {
    unsigned char i;
    for(i = 0; i < 8; i++) {
        SDA = (byte & 0x80) >> 7;
        SCL = 1;
        I2C_Delay();
        SCL = 0;
        I2C_Delay();
        byte <<= 1;
    }
}

// 接收一个字节
unsigned char I2C_ReceiveByte(void) {
    unsigned char i, byte = 0;
    SDA = 1;
    for(i = 0; i < 8; i++) {
        SCL = 1;
        I2C_Delay();
        byte = (byte << 1) | SDA;
        SCL = 0;
        I2C_Delay();
    }
    return byte;
}

// 写数据到I2C设备
void I2C_Write(unsigned char dev_addr, unsigned char reg_addr, unsigned char data) {
    I2C_Start();
    I2C_SendByte(dev_addr << 1); // 写地址
    I2C_ReceiveAck();
    I2C_SendByte(reg_addr);
    I2C_ReceiveAck();
    I2C_SendByte(data);
    I2C_ReceiveAck();
    I2C_Stop();
}

// 从I2C设备读取数据
unsigned char I2C_Read(unsigned char dev_addr, unsigned char reg_addr) {
    unsigned char data;
    I2C_Start();
    I2C_SendByte(dev_addr << 1); // 写地址
    I2C_ReceiveAck();
    I2C_SendByte(reg_addr);
    I2C_ReceiveAck();
    I2C_Start();
    I2C_SendByte((dev_addr << 1) | 1); // 读地址
    I2C_ReceiveAck();
    data = I2C_ReceiveByte();
    I2C_SendAck(1); // 发送非应答
    I2C_Stop();
    return data;
}
```

#### STC12C5A60S2硬件I2C实现

```c
#include <STC12C5A60S2.h>

void I2C_Init(void) {
    // 配置I2C引脚
    P1M0 &= ~0x03; // P1.0和P1.1设为准双向口
    P1M1 &= ~0x03;
    
    // 设置I2C时钟频率
    // I2C频率 = FOSC / (2 * (I2C_SCLH + I2C_SCLL))
    I2C_SCLH = 0x1E; // 高电平时间
    I2C_SCLL = 0x1E; // 低电平时间
    
    // 使能I2C
    I2C_CONTR = 0x80; // 使能I2C
}

void I2C_Start(void) {
    I2C_CONTR |= 0x02; // 发送起始条件
    while((I2C_CONTR & 0x02)); // 等待起始条件发送完成
}

void I2C_Stop(void) {
    I2C_CONTR |= 0x04; // 发送停止条件
    while((I2C_CONTR & 0x04)); // 等待停止条件发送完成
}

void I2C_SendByte(unsigned char byte) {
    I2C_DATA = byte;
    I2C_CONTR &= ~0x01; // 清除中断标志
    I2C_CONTR |= 0x08; // 发送数据
    while(!(I2C_CONTR & 0x01)); // 等待发送完成
}

unsigned char I2C_ReceiveByte(void) {
    I2C_CONTR &= ~0x01; // 清除中断标志
    I2C_CONTR |= 0x10; // 接收数据
    while(!(I2C_CONTR & 0x01)); // 等待接收完成
    return I2C_DATA;
}

void I2C_SendAck(unsigned char ack) {
    I2C_CONTR &= ~0x20; // 清除应答标志
    if(!ack) {
        I2C_CONTR |= 0x20; // 发送应答
    }
    I2C_CONTR &= ~0x01; // 清除中断标志
    I2C_CONTR |= 0x08; // 发送应答
    while(!(I2C_CONTR & 0x01)); // 等待发送完成
}

unsigned char I2C_CheckAck(void) {
    return !(I2C_STAT & 0x01); // 0表示收到应答
}

void I2C_Write(unsigned char dev_addr, unsigned char reg_addr, unsigned char data) {
    I2C_Start();
    I2C_SendByte(dev_addr << 1); // 写地址
    if(!I2C_CheckAck()) {
        I2C_Stop();
        return;
    }
    I2C_SendByte(reg_addr);
    if(!I2C_CheckAck()) {
        I2C_Stop();
        return;
    }
    I2C_SendByte(data);
    if(!I2C_CheckAck()) {
        I2C_Stop();
        return;
    }
    I2C_Stop();
}

unsigned char I2C_Read(unsigned char dev_addr, unsigned char reg_addr) {
    unsigned char data;
    I2C_Start();
    I2C_SendByte(dev_addr << 1); // 写地址
    if(!I2C_CheckAck()) {
        I2C_Stop();
        return 0;
    }
    I2C_SendByte(reg_addr);
    if(!I2C_CheckAck()) {
        I2C_Stop();
        return 0;
    }
    I2C_Start();
    I2C_SendByte((dev_addr << 1) | 1); // 读地址
    if(!I2C_CheckAck()) {
        I2C_Stop();
        return 0;
    }
    data = I2C_ReceiveByte();
    I2C_SendAck(1); // 发送非应答
    I2C_Stop();
    return data;
}
```

### GD32系列I2C实现

```c
#include "gd32f10x.h"

void I2C_Init(void) {
    // 使能I2C0时钟
    rcu_periph_clock_enable(RCU_I2C0);
    // 使能GPIOB时钟
    rcu_periph_clock_enable(RCU_GPIOB);
    
    // 配置PB6为I2C0_SCL
    gpio_init(GPIOB, GPIO_MODE_AF_OD, GPIO_OSPEED_50MHZ, GPIO_PIN_6);
    // 配置PB7为I2C0_SDA
    gpio_init(GPIOB, GPIO_MODE_AF_OD, GPIO_OSPEED_50MHZ, GPIO_PIN_7);
    
    // 配置I2C0
    i2c_deinit(I2C0);
    i2c_clock_config(I2C0, 400000, I2C_DTCY_2); // 400kHz
    i2c_mode_addr_config(I2C0, I2C_I2CMODE_ENABLE, I2C_ADDFORMAT_7BITS, 0x00);
    i2c_enable(I2C0);
    i2c_ack_config(I2C0, I2C_ACK_ENABLE);
}

void I2C_WriteByte(uint8_t dev_addr, uint8_t reg_addr, uint8_t data) {
    // 等待总线空闲
    while(i2c_flag_get(I2C0, I2C_FLAG_I2CBSY));
    
    // 发送起始条件
    i2c_start_on_bus(I2C0);
    while(!i2c_flag_get(I2C0, I2C_FLAG_SBSEND));
    
    // 发送设备地址（写）
    i2c_master_addressing(I2C0, dev_addr << 1, I2C_TRANSMITTER);
    while(!i2c_flag_get(I2C0, I2C_FLAG_ADDSEND));
    i2c_flag_clear(I2C0, I2C_FLAG_ADDSEND);
    
    // 发送寄存器地址
    i2c_data_transmit(I2C0, reg_addr);
    while(!i2c_flag_get(I2C0, I2C_FLAG_TBE));
    
    // 发送数据
    i2c_data_transmit(I2C0, data);
    while(!i2c_flag_get(I2C0, I2C_FLAG_TBE));
    
    // 发送停止条件
    i2c_stop_on_bus(I2C0);
    while(i2c_flag_get(I2C0, I2C_FLAG_STPDET));
}

uint8_t I2C_ReadByte(uint8_t dev_addr, uint8_t reg_addr) {
    uint8_t data;
    
    // 等待总线空闲
    while(i2c_flag_get(I2C0, I2C_FLAG_I2CBSY));
    
    // 发送起始条件
    i2c_start_on_bus(I2C0);
    while(!i2c_flag_get(I2C0, I2C_FLAG_SBSEND));
    
    // 发送设备地址（写）
    i2c_master_addressing(I2C0, dev_addr << 1, I2C_TRANSMITTER);
    while(!i2c_flag_get(I2C0, I2C_FLAG_ADDSEND));
    i2c_flag_clear(I2C0, I2C_FLAG_ADDSEND);
    
    // 发送寄存器地址
    i2c_data_transmit(I2C0, reg_addr);
    while(!i2c_flag_get(I2C0, I2C_FLAG_TBE));
    
    // 重新发送起始条件
    i2c_start_on_bus(I2C0);
    while(!i2c_flag_get(I2C0, I2C_FLAG_SBSEND));
    
    // 发送设备地址（读）
    i2c_master_addressing(I2C0, dev_addr << 1, I2C_RECEIVER);
    while(!i2c_flag_get(I2C0, I2C_FLAG_ADDSEND));
    i2c_flag_clear(I2C0, I2C_FLAG_ADDSEND);
    
    // 禁用应答
    i2c_ack_config(I2C0, I2C_ACK_DISABLE);
    
    // 发送停止条件
    i2c_stop_on_bus(I2C0);
    while(!i2c_flag_get(I2C0, I2C_FLAG_RBNE));
    
    // 读取数据
    data = i2c_data_receive(I2C0);
    while(i2c_flag_get(I2C0, I2C_FLAG_STPDET));
    
    // 重新启用应答
    i2c_ack_config(I2C0, I2C_ACK_ENABLE);
    
    return data;
}
```

## SPI接口

### 基本概念

- **SPI总线**：由SCK（时钟线）、MOSI（主出从入）、MISO（主入从出）和CS（片选）组成
- **主从架构**：通常是一主多从，通过片选信号选择从设备
- **通信速率**：可根据时钟频率调整，通常可达几MHz
- **数据传输**：全双工，同时发送和接收数据

### STC系列SPI实现

#### STC89C51软件SPI实现

```c
#include <reg51.h>

// 定义SPI引脚
#define SCK P1_0
#define MOSI P1_1
#define MISO P1_2
#define CS P1_3

// 延时函数
void SPI_Delay(void) {
    unsigned char i;
    for(i = 0; i < 5; i++);
}

// SPI初始化
void SPI_Init(void) {
    // 配置引脚
    SCK = 0;
    MOSI = 0;
    CS = 1; // 片选高电平无效
}

// SPI发送一个字节
unsigned char SPI_SendByte(unsigned char byte) {
    unsigned char i, recv = 0;
    for(i = 0; i < 8; i++) {
        // 发送一位
        MOSI = (byte & 0x80) >> 7;
        SCK = 1;
        SPI_Delay();
        // 接收一位
        recv = (recv << 1) | MISO;
        SCK = 0;
        SPI_Delay();
        byte <<= 1;
    }
    return recv;
}

// SPI读写操作
unsigned char SPI_Transfer(unsigned char dev_cs, unsigned char data) {
    unsigned char recv;
    CS = 0; // 片选有效
    recv = SPI_SendByte(data);
    CS = 1; // 片选无效
    return recv;
}
```

#### STC12C5A60S2硬件SPI实现

```c
#include <STC12C5A60S2.h>

void SPI_Init(void) {
    // 配置SPI引脚
    P1M0 |= 0x0E; // P1.1-P1.3设为推挽输出
    P1M1 &= ~0x0E;
    P1M0 &= ~0x08; // P1.3设为准双向口（CS）
    
    // 配置SPI
    SPCTL = 0x50; // 主机模式，时钟极性0，相位0，1/16分频
    SPSTAT = 0xC0; // 清除中断标志
}

unsigned char SPI_SendByte(unsigned char byte) {
    SPSTAT = 0xC0; // 清除中断标志
    SPDR = byte;
    while(!(SPSTAT & 0x80)); // 等待发送完成
    return SPDR;
}

unsigned char SPI_Transfer(unsigned char dev_cs, unsigned char data) {
    unsigned char recv;
    P1_3 = 0; // 片选有效
    recv = SPI_SendByte(data);
    P1_3 = 1; // 片选无效
    return recv;
}
```

### GD32系列SPI实现

```c
#include "gd32f10x.h"

void SPI_Init(void) {
    // 使能SPI0时钟
    rcu_periph_clock_enable(RCU_SPI0);
    // 使能GPIOA时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    
    // 配置PA5为SPI0_SCK
    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_5);
    // 配置PA6为SPI0_MISO
    gpio_init(GPIOA, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_50MHZ, GPIO_PIN_6);
    // 配置PA7为SPI0_MOSI
    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_7);
    // 配置PA4为CS
    gpio_init(GPIOA, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_4);
    
    // 配置SPI0
    spi_deinit(SPI0);
    spi_init(SPI0, SPI_MASTER, SPI_MODE_0, SPI_FRAME_8BIT, SPI_SPEED_2MHZ);
    spi_enable(SPI0);
    
    // 初始化CS
    gpio_bit_set(GPIOA, GPIO_PIN_4);
}

unsigned char SPI_Transfer(unsigned char data) {
    // 等待发送缓冲区为空
    while(RESET == spi_flag_get(SPI0, SPI_FLAG_TBE));
    // 发送数据
    spi_data_transmit(SPI0, data);
    // 等待接收缓冲区非空
    while(RESET == spi_flag_get(SPI0, SPI_FLAG_RBNE));
    // 返回接收的数据
    return spi_data_receive(SPI0);
}

void SPI_WriteByte(unsigned char dev_cs, unsigned char data) {
    gpio_bit_reset(GPIOA, GPIO_PIN_4); // 片选有效
    SPI_Transfer(data);
    gpio_bit_set(GPIOA, GPIO_PIN_4); // 片选无效
}

unsigned char SPI_ReadByte(unsigned char dev_cs) {
    gpio_bit_reset(GPIOA, GPIO_PIN_4); // 片选有效
    unsigned char data = SPI_Transfer(0xFF);
    gpio_bit_set(GPIOA, GPIO_PIN_4); // 片选无效
    return data;
}

void SPI_WriteBuffer(unsigned char dev_cs, uint8_t *buffer, uint16_t length) {
    gpio_bit_reset(GPIOA, GPIO_PIN_4); // 片选有效
    for(uint16_t i = 0; i < length; i++) {
        SPI_Transfer(buffer[i]);
    }
    gpio_bit_set(GPIOA, GPIO_PIN_4); // 片选无效
}

void SPI_ReadBuffer(unsigned char dev_cs, uint8_t *buffer, uint16_t length) {
    gpio_bit_reset(GPIOA, GPIO_PIN_4); // 片选有效
    for(uint16_t i = 0; i < length; i++) {
        buffer[i] = SPI_Transfer(0xFF);
    }
    gpio_bit_set(GPIOA, GPIO_PIN_4); // 片选无效
}
```

## 通用设备驱动示例

### I2C设备驱动：AT24C02 EEPROM

```c
#include "i2c.h" // 包含上面的I2C实现

#define AT24C02_ADDR 0x50

void AT24C02_WriteByte(uint8_t addr, uint8_t data) {
    I2C_Write(AT24C02_ADDR, addr, data);
    // AT24C02需要一些时间来写入
    delay_ms(5);
}

uint8_t AT24C02_ReadByte(uint8_t addr) {
    return I2C_Read(AT24C02_ADDR, addr);
}

void AT24C02_WritePage(uint8_t addr, uint8_t *data, uint8_t length) {
    // AT24C02每页8字节
    for(uint8_t i = 0; i < length; i++) {
        AT24C02_WriteByte(addr + i, data[i]);
    }
}

void AT24C02_ReadPage(uint8_t addr, uint8_t *data, uint8_t length) {
    for(uint8_t i = 0; i < length; i++) {
        data[i] = AT24C02_ReadByte(addr + i);
    }
}
```

### SPI设备驱动：W25Q64 Flash

```c
#include "spi.h" // 包含上面的SPI实现

#define W25Q64_CS PA4

// 命令定义
#define W25Q_WRITE_ENABLE     0x06
#define W25Q_WRITE_DISABLE    0x04
#define W25Q_READ_STATUS_REG1 0x05
#define W25Q_READ_STATUS_REG2 0x35
#define W25Q_READ_DATA        0x03
#define W25Q_PAGE_PROGRAM     0x02
#define W25Q_SECTOR_ERASE     0x20
#define W25Q_BLOCK_ERASE_32K  0x52
#define W25Q_BLOCK_ERASE_64K  0xD8
#define W25Q_CHIP_ERASE       0xC7
#define W25Q_POWER_DOWN       0xB9
#define W25Q_RELEASE_POWER_DOWN 0xAB
#define W25Q_READ_ID          0x90

void W25Q64_WriteEnable(void) {
    GPIO_ResetBits(GPIOC, W25Q64_CS);
    SPI_SendByte(W25Q_WRITE_ENABLE);
    GPIO_SetBits(GPIOC, W25Q64_CS);
}

uint8_t W25Q64_ReadStatusReg1(void) {
    uint8_t status;
    GPIO_ResetBits(GPIOC, W25Q64_CS);
    SPI_SendByte(W25Q_READ_STATUS_REG1);
    status = SPI_SendByte(0xFF);
    GPIO_SetBits(GPIOC, W25Q64_CS);
    return status;
}

void W25Q64_WaitBusy(void) {
    while((W25Q64_ReadStatusReg1() & 0x01) == 0x01);
}

void W25Q64_ReadData(uint32_t addr, uint8_t *data, uint32_t length) {
    GPIO_ResetBits(GPIOC, W25Q64_CS);
    SPI_SendByte(W25Q_READ_DATA);
    SPI_SendByte((addr >> 16) & 0xFF);
    SPI_SendByte((addr >> 8) & 0xFF);
    SPI_SendByte(addr & 0xFF);
    for(uint32_t i = 0; i < length; i++) {
        data[i] = SPI_SendByte(0xFF);
    }
    GPIO_SetBits(GPIOC, W25Q64_CS);
}

void W25Q64_PageProgram(uint32_t addr, uint8_t *data, uint16_t length) {
    W25Q64_WriteEnable();
    W25Q64_WaitBusy();
    
    GPIO_ResetBits(GPIOC, W25Q64_CS);
    SPI_SendByte(W25Q_PAGE_PROGRAM);
    SPI_SendByte((addr >> 16) & 0xFF);
    SPI_SendByte((addr >> 8) & 0xFF);
    SPI_SendByte(addr & 0xFF);
    for(uint16_t i = 0; i < length; i++) {
        SPI_SendByte(data[i]);
    }
    GPIO_SetBits(GPIOC, W25Q64_CS);
    
    W25Q64_WaitBusy();
}

void W25Q64_SectorErase(uint32_t addr) {
    W25Q64_WriteEnable();
    W25Q64_WaitBusy();
    
    GPIO_ResetBits(GPIOC, W25Q64_CS);
    SPI_SendByte(W25Q_SECTOR_ERASE);
    SPI_SendByte((addr >> 16) & 0xFF);
    SPI_SendByte((addr >> 8) & 0xFF);
    SPI_SendByte(addr & 0xFF);
    GPIO_SetBits(GPIOC, W25Q64_CS);
    
    W25Q64_WaitBusy();
}
```

## 常见问题与解决方案

### I2C常见问题

#### 问题1：I2C通信失败
- **原因**：可能是地址错误、时序问题、硬件连接问题
- **解决方案**：检查设备地址是否正确，使用示波器检查时序，检查硬件连接

#### 问题2：I2C总线上拉电阻
- **原因**：I2C总线需要上拉电阻，否则通信会失败
- **解决方案**：在SCL和SDA线上添加4.7kΩ左右的上拉电阻

#### 问题3：I2C总线冲突
- **原因**：多个主设备同时访问总线
- **解决方案**：实现总线仲裁，或使用单一主设备

### SPI常见问题

#### 问题1：SPI通信乱码
- **原因**：时钟极性和相位设置错误，或时钟频率过高
- **解决方案**：根据从设备要求设置正确的时钟模式，降低时钟频率

#### 问题2：SPI片选信号
- **原因**：片选信号没有正确控制
- **解决方案**：确保在通信开始前拉低片选，结束后拉高

#### 问题3：SPI数据传输错误
- **原因**：数据线连接错误，或从设备未就绪
- **解决方案**：检查硬件连接，确保从设备已正确初始化

## 最佳实践

### I2C最佳实践

1. **上拉电阻**：在SCL和SDA线上添加适当的上拉电阻（通常4.7kΩ）
2. **地址确认**：使用I2C扫描工具确认设备地址
3. **错误处理**：添加通信错误检测和重试机制
4. **时钟速度**：根据设备要求选择合适的通信速率
5. **总线长度**：I2C总线长度不宜过长，一般不超过1米
6. **电源隔离**：如果总线上有不同电压的设备，需要使用电平转换器

### SPI最佳实践

1. **片选控制**：确保片选信号的正确控制，避免多个设备同时被选中
2. **时钟设置**：根据从设备的最大时钟频率设置SPI时钟
3. **数据格式**：确保主从设备的数据格式（位序、长度）一致
4. **信号完整性**：对于高速SPI，考虑使用屏蔽线缆和端接电阻
5. **电源稳定**：确保SPI设备的电源稳定，避免电压波动
6. **中断处理**：对于大批量数据传输，考虑使用DMA或中断方式

## 示例项目

### 项目：I2C温湿度传感器（DHT12）

#### 功能描述
- 通过I2C接口读取DHT12温湿度传感器数据
- 显示温度和湿度值
- 实现错误检测和处理

#### 代码实现

```c
#include "gd32f10x.h"
#include "i2c.h"

#define DHT12_ADDR 0x5c

typedef struct {
    uint8_t humidity_int;
    uint8_t humidity_dec;
    uint8_t temperature_int;
    uint8_t temperature_dec;
    uint8_t checksum;
} DHT12_Data;

uint8_t DHT12_ReadData(DHT12_Data *data) {
    uint8_t buffer[5];
    
    // 读取5字节数据
    for(uint8_t i = 0; i < 5; i++) {
        buffer[i] = I2C_Read(DHT12_ADDR, i);
    }
    
    // 计算校验和
    uint8_t checksum = buffer[0] + buffer[1] + buffer[2] + buffer[3];
    if(checksum != buffer[4]) {
        return 0; // 校验失败
    }
    
    // 填充数据
    data->humidity_int = buffer[0];
    data->humidity_dec = buffer[1];
    data->temperature_int = buffer[2];
    data->temperature_dec = buffer[3];
    data->checksum = buffer[4];
    
    return 1; // 成功
}

void main(void) {
    I2C_Init();
    UART_Init();
    
    DHT12_Data data;
    
    while(1) {
        if(DHT12_ReadData(&data)) {
            // 计算温度和湿度
            float temperature = data.temperature_int + data.temperature_dec / 10.0;
            float humidity = data.humidity_int + data.humidity_dec / 10.0;
            
            // 发送到串口
            char buffer[64];
            sprintf(buffer, "Temperature: %.1f°C, Humidity: %.1f%%\r\n", temperature, humidity);
            UART_SendString((uint8_t *)buffer);
        } else {
            UART_SendString((uint8_t *)"DHT12 read error\r\n");
        }
        
        delay_ms(2000); // 每2秒读取一次
    }
}
```

### 项目：SPI OLED显示

#### 功能描述
- 通过SPI接口控制SSD1306 OLED显示屏
- 显示文本和简单图形
- 实现屏幕清屏、字符显示等基本功能

#### 代码实现

```c
#include "gd32f10x.h"
#include "spi.h"

#define OLED_CS PA4
#define OLED_DC PA3
#define OLED_RST PA2

// SSD1306命令
#define SSD1306_COMMAND 0
#define SSD1306_DATA 1

#define SSD1306_SET_CONTRAST 0x81
#define SSD1306_DISPLAY_ALL_ON_RESUME 0xA4
#define SSD1306_DISPLAY_ALL_ON 0xA5
#define SSD1306_NORMAL_DISPLAY 0xA6
#define SSD1306_INVERT_DISPLAY 0xA7
#define SSD1306_DISPLAY_OFF 0xAE
#define SSD1306_DISPLAY_ON 0xAF
#define SSD1306_SET_DISPLAY_OFFSET 0xD3
#define SSD1306_SET_COM_PINS 0xDA
#define SSD1306_SET_VCOM_DETECT 0xDB
#define SSD1306_SET_DISPLAY_CLOCK_DIV 0xD5
#define SSD1306_SET_PRECHARGE 0xD9
#define SSD1306_SET_MULTIPLEX 0xA8
#define SSD1306_SET_LOW_COLUMN 0x00
#define SSD1306_SET_HIGH_COLUMN 0x10
#define SSD1306_SET_START_LINE 0x40
#define SSD1306_MEMORY_MODE 0x20
#define SSD1306_COLUMN_ADDR 0x21
#define SSD1306_PAGE_ADDR 0x22
#define SSD1306_COM_SCAN_DIR_INC 0xC0
#define SSD1306_COM_SCAN_DIR_DEC 0xC8
#define SSD1306_SEGMENT_REMAP 0xA0
#define SSD1306_SEGMENT_REMAP_REVERSE 0xA1
#define SSD1306_CHARGE_PUMP 0x8D

void OLED_SendCmd(uint8_t cmd) {
    GPIO_ResetBits(GPIOA, OLED_DC); // 命令模式
    GPIO_ResetBits(GPIOA, OLED_CS); // 片选有效
    SPI_Transfer(cmd);
    GPIO_SetBits(GPIOA, OLED_CS); // 片选无效
}

void OLED_SendData(uint8_t data) {
    GPIO_SetBits(GPIOA, OLED_DC); // 数据模式
    GPIO_ResetBits(GPIOA, OLED_CS); // 片选有效
    SPI_Transfer(data);
    GPIO_SetBits(GPIOA, OLED_CS); // 片选无效
}

void OLED_Init(void) {
    // 复位OLED
    GPIO_ResetBits(GPIOA, OLED_RST);
    delay_ms(10);
    GPIO_SetBits(GPIOA, OLED_RST);
    delay_ms(10);
    
    // 初始化命令
    OLED_SendCmd(SSD1306_DISPLAY_OFF);
    OLED_SendCmd(SSD1306_SET_DISPLAY_CLOCK_DIV);
    OLED_SendCmd(0x80);
    OLED_SendCmd(SSD1306_SET_MULTIPLEX);
    OLED_SendCmd(0x3F);
    OLED_SendCmd(SSD1306_SET_DISPLAY_OFFSET);
    OLED_SendCmd(0x00);
    OLED_SendCmd(SSD1306_SET_START_LINE | 0x00);
    OLED_SendCmd(SSD1306_CHARGE_PUMP);
    OLED_SendCmd(0x14);
    OLED_SendCmd(SSD1306_MEMORY_MODE);
    OLED_SendCmd(0x00);
    OLED_SendCmd(SSD1306_SEGMENT_REMAP_REVERSE);
    OLED_SendCmd(SSD1306_COM_SCAN_DIR_DEC);
    OLED_SendCmd(SSD1306_SET_COM_PINS);
    OLED_SendCmd(0x12);
    OLED_SendCmd(SSD1306_SET_CONTRAST);
    OLED_SendCmd(0xCF);
    OLED_SendCmd(SSD1306_SET_PRECHARGE);
    OLED_SendCmd(0xF1);
    OLED_SendCmd(SSD1306_SET_VCOM_DETECT);
    OLED_SendCmd(0x40);
    OLED_SendCmd(SSD1306_DISPLAY_ALL_ON_RESUME);
    OLED_SendCmd(SSD1306_NORMAL_DISPLAY);
    OLED_SendCmd(SSD1306_DISPLAY_ON);
}

void OLED_Clear(void) {
    for(uint8_t page = 0; page < 8; page++) {
        OLED_SendCmd(SSD1306_PAGE_ADDR);
        OLED_SendCmd(page);
        OLED_SendCmd(SSD1306_COLUMN_ADDR);
        OLED_SendCmd(0);
        OLED_SendCmd(127);
        
        for(uint8_t col = 0; col < 128; col++) {
            OLED_SendData(0x00);
        }
    }
}

// 简单的字符显示函数
void OLED_DrawChar(uint8_t x, uint8_t y, char c) {
    // 假设使用8x8字体
    const uint8_t font[] = {
        // 这里应该包含字体数据
    };
    
    OLED_SendCmd(SSD1306_PAGE_ADDR);
    OLED_SendCmd(y);
    OLED_SendCmd(SSD1306_COLUMN_ADDR);
    OLED_SendCmd(x);
    OLED_SendCmd(x + 7);
    
    for(uint8_t i = 0; i < 8; i++) {
        OLED_SendData(font[(c - ' ') * 8 + i]);
    }
}

void OLED_DrawString(uint8_t x, uint8_t y, char *str) {
    while(*str) {
        OLED_DrawChar(x, y, *str++);
        x += 8;
    }
}

void main(void) {
    SPI_Init();
    OLED_Init();
    OLED_Clear();
    
    while(1) {
        OLED_DrawString(0, 0, "Hello, OLED!");
        OLED_DrawString(0, 2, "Temperature: 25.5°C");
        OLED_DrawString(0, 4, "Humidity: 60%");
        delay_ms(1000);
    }
}
```

## 总结

I2C和SPI是两种重要的串行通信协议，在嵌入式系统中广泛应用。本文档提供了STC、GD32等国产单片机的I2C和SPI接口实现方法，包括软件模拟和硬件实现两种方式。

在实际开发中，应根据具体的应用场景选择合适的通信协议：
- **I2C**：适用于设备数量较多、通信速率要求不高的场景，如传感器网络
- **SPI**：适用于需要高速通信的场景，如显示屏、Flash存储器等

同时，应注意通信协议的正确实现，包括时序控制、错误处理、电源管理等方面，以确保通信的可靠性和稳定性。

通过本文档的学习，开发者可以掌握国产单片机的I2C和SPI接口技术，为嵌入式系统开发打下坚实的基础。