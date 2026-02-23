# 显示设备驱动

## 概述

显示设备是嵌入式系统中向用户展示信息的重要组件，常见的显示设备包括LCD、OLED、LED等。本文档将介绍常见显示设备的工作原理、接口方式以及在不同系列微控制器上的驱动实现。

## LED 显示

### 1. 单个LED控制
- **特点**：结构简单、成本低、易于控制
- **接口**：GPIO输出

### STC系列微控制器实现

```c
#include "stc8.h"

#define LED P1_0

// 初始化LED
void LED_Init(void)
{
    LED = 0;  // 初始状态关闭
}

// 点亮LED
void LED_On(void)
{
    LED = 1;
}

// 关闭LED
void LED_Off(void)
{
    LED = 0;
}

// 翻转LED状态
void LED_Toggle(void)
{
    LED = !LED;
}

// 主函数
void main(void)
{
    LED_Init();
    
    while(1) {
        LED_Toggle();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
    }
}
```

### 2. LED 点阵显示
- **特点**：可以显示简单图形和文字
- **接口**：GPIO输出，通常使用行扫描方式

### STC系列微控制器实现

```c
#include "stc8.h"

// 定义LED点阵引脚
#define ROW_PORT P0
#define COL_PORT P2

// 数字0-9的点阵数据
uint8_t digit[10] = {
    0x3F,  // 0
    0x06,  // 1
    0x5B,  // 2
    0x4F,  // 3
    0x66,  // 4
    0x6D,  // 5
    0x7D,  // 6
    0x07,  // 7
    0x7F,  // 8
    0x6F   // 9
};

// 初始化LED点阵
void LEDMatrix_Init(void)
{
    ROW_PORT = 0xFF;
    COL_PORT = 0x00;
}

// 显示一个数字
void LEDMatrix_DisplayDigit(uint8_t num)
{
    if(num < 10) {
        ROW_PORT = ~digit[num];
    }
}

// 主函数
void main(void)
{
    LEDMatrix_Init();
    
    uint8_t num = 0;
    while(1) {
        LEDMatrix_DisplayDigit(num);
        num = (num + 1) % 10;
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
    }
}
```

## LCD 显示

### 1. 1602 字符型LCD
- **特点**：可以显示字母、数字和简单符号
- **接口**：并行接口（8位或4位）
- **分辨率**：16x2或20x4

### STC系列微控制器实现

```c
#include "stc8.h"

// 定义LCD引脚
#define LCD_RS P2_0
#define LCD_RW P2_1
#define LCD_EN P2_2
#define LCD_DATA P0

// 延时函数
void Delay1ms(uint16_t ms)
{
    uint16_t i, j;
    for(i = 0; i < ms; i++) {
        for(j = 0; j < 110; j++);
    }
}

// 写命令
void LCD_WriteCmd(uint8_t cmd)
{
    LCD_RS = 0;
    LCD_RW = 0;
    LCD_DATA = cmd;
    LCD_EN = 1;
    Delay1ms(1);
    LCD_EN = 0;
    Delay1ms(1);
}

// 写数据
void LCD_WriteData(uint8_t data)
{
    LCD_RS = 1;
    LCD_RW = 0;
    LCD_DATA = data;
    LCD_EN = 1;
    Delay1ms(1);
    LCD_EN = 0;
    Delay1ms(1);
}

// 初始化LCD
void LCD_Init(void)
{
    LCD_WriteCmd(0x38);  // 8位数据，2行显示，5x7点阵
    LCD_WriteCmd(0x0C);  // 显示开，光标关，闪烁关
    LCD_WriteCmd(0x06);  // 光标右移，不滚动
    LCD_WriteCmd(0x01);  // 清屏
    Delay1ms(2);
}

// 清屏
void LCD_Clear(void)
{
    LCD_WriteCmd(0x01);
    Delay1ms(2);
}

// 设置光标位置
void LCD_SetCursor(uint8_t row, uint8_t col)
{
    uint8_t address;
    if(row == 0) {
        address = 0x00 + col;
    } else {
        address = 0x40 + col;
    }
    LCD_WriteCmd(0x80 | address);
}

// 显示字符串
void LCD_DisplayString(uint8_t row, uint8_t col, char *str)
{
    LCD_SetCursor(row, col);
    while(*str) {
        LCD_WriteData(*str++);
    }
}

// 主函数
void main(void)
{
    LCD_Init();
    LCD_DisplayString(0, 0, "Hello, World!");
    LCD_DisplayString(1, 0, "STM8 Controller");
    
    while(1);
}
```

### 2. I2C 接口字符型LCD
- **特点**：使用I2C接口，连线少
- **接口**：I2C

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

#define LCD_ADDR 0x27

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

// 向LCD发送数据
void LCD_Send(uint8_t data, uint8_t mode)
{
    uint8_t high_nibble = data & 0xF0;
    uint8_t low_nibble = (data << 4) & 0xF0;
    
    // 发送高四位
    uint8_t byte = high_nibble | mode | 0x04;
    i2c_start_on_bus(I2C0);
    i2c_master_addressing(I2C0, LCD_ADDR << 1, I2C_TRANSMITTER);
    i2c_data_transmit(I2C0, byte);
    i2c_data_transmit(I2C0, byte & 0xFB);
    
    // 发送低四位
    byte = low_nibble | mode | 0x04;
    i2c_data_transmit(I2C0, byte);
    i2c_data_transmit(I2C0, byte & 0xFB);
    
    i2c_stop_on_bus(I2C0);
    delay_ms(1);
}

// 写命令
void LCD_WriteCmd(uint8_t cmd)
{
    LCD_Send(cmd, 0x00);
}

// 写数据
void LCD_WriteData(uint8_t data)
{
    LCD_Send(data, 0x01);
}

// 初始化LCD
void LCD_Init(void)
{
    // 初始化I2C
    I2C_Init();
    
    // 初始化LCD
    delay_ms(50);
    LCD_Send(0x30, 0x00);
    delay_ms(5);
    LCD_Send(0x30, 0x00);
    delay_ms(1);
    LCD_Send(0x30, 0x00);
    delay_ms(1);
    LCD_Send(0x20, 0x00);  // 4位模式
    delay_ms(1);
    
    LCD_WriteCmd(0x28);  // 4位数据，2行显示，5x7点阵
    LCD_WriteCmd(0x0C);  // 显示开，光标关，闪烁关
    LCD_WriteCmd(0x06);  // 光标右移，不滚动
    LCD_WriteCmd(0x01);  // 清屏
    delay_ms(2);
}

// 清屏
void LCD_Clear(void)
{
    LCD_WriteCmd(0x01);
    delay_ms(2);
}

// 设置光标位置
void LCD_SetCursor(uint8_t row, uint8_t col)
{
    uint8_t address;
    if(row == 0) {
        address = 0x00 + col;
    } else {
        address = 0x40 + col;
    }
    LCD_WriteCmd(0x80 | address);
}

// 显示字符串
void LCD_DisplayString(uint8_t row, uint8_t col, char *str)
{
    LCD_SetCursor(row, col);
    while(*str) {
        LCD_WriteData(*str++);
    }
}
```

### 3. TFT LCD 彩色显示
- **特点**：可以显示彩色图像和文字
- **接口**：SPI或并行接口
- **分辨率**：常见128x128、128x160、240x320等

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

// 定义TFT LCD引脚
#define TFT_CS_PORT GPIOA
#define TFT_CS_PIN GPIO_PIN_4
#define TFT_DC_PORT GPIOA
#define TFT_DC_PIN GPIO_PIN_5
#define TFT_RST_PORT GPIOA
#define TFT_RST_PIN GPIO_PIN_6

// 颜色定义
#define BLACK       0x0000
#define WHITE       0xFFFF
#define RED         0xF800
#define GREEN       0x07E0
#define BLUE        0x001F
#define YELLOW      0xFFE0
#define CYAN        0x07FF
#define MAGENTA     0xF81F

// 初始化SPI
void SPI_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    // 使能SPI0时钟
    rcu_periph_clock_enable(RCU_SPI0);
    
    // 配置PA5为SPI0_SCK
    gpio_af_set(GPIOA, GPIO_AF_5, GPIO_PIN_5);
    // 配置PA7为SPI0_MOSI
    gpio_af_set(GPIOA, GPIO_AF_5, GPIO_PIN_7);
    
    // 配置控制引脚
    gpio_mode_set(TFT_CS_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, TFT_CS_PIN);
    gpio_mode_set(TFT_DC_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, TFT_DC_PIN);
    gpio_mode_set(TFT_RST_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, TFT_RST_PIN);
    
    // 配置GPIO
    gpio_mode_set(GPIOA, GPIO_MODE_AF, GPIO_PUPD_PULLUP, GPIO_PIN_5 | GPIO_PIN_7);
    gpio_output_options_set(GPIOA, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_4 | GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7);
    
    // 配置SPI0
    spi_deinit(SPI0);
    spi_init(SPI0, SPI_MODE_MASTER, SPI_TRANSMODE_FULLDUPLEX, SPI_FRAMESIZE_8BIT, SPI_NSS_SOFT, 4);
    spi_enable(SPI0);
    
    // 初始化解选
    gpio_bit_set(TFT_CS_PORT, TFT_CS_PIN);
}

// 发送SPI数据
void SPI_SendByte(uint8_t data)
{
    // 等待发送缓冲区为空
    while(RESET == spi_flag_get(SPI0, SPI_FLAG_TBE));
    // 发送数据
    spi_data_transmit(SPI0, data);
    // 等待接收缓冲区非空
    while(RESET == spi_flag_get(SPI0, SPI_FLAG_RBNE));
    // 读取接收数据
    spi_data_receive(SPI0);
}

// 写命令
void TFT_WriteCmd(uint8_t cmd)
{
    gpio_bit_reset(TFT_CS_PORT, TFT_CS_PIN);
    gpio_bit_reset(TFT_DC_PORT, TFT_DC_PIN);
    SPI_SendByte(cmd);
    gpio_bit_set(TFT_CS_PORT, TFT_CS_PIN);
}

// 写数据
void TFT_WriteData(uint8_t data)
{
    gpio_bit_reset(TFT_CS_PORT, TFT_CS_PIN);
    gpio_bit_set(TFT_DC_PORT, TFT_DC_PIN);
    SPI_SendByte(data);
    gpio_bit_set(TFT_CS_PORT, TFT_CS_PIN);
}

// 写16位数据
void TFT_WriteData16(uint16_t data)
{
    TFT_WriteData(data >> 8);
    TFT_WriteData(data & 0xFF);
}

// 设置显示区域
void TFT_SetWindow(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1)
{
    // 设置列地址
    TFT_WriteCmd(0x2A);
    TFT_WriteData16(x0);
    TFT_WriteData16(x1);
    
    // 设置行地址
    TFT_WriteCmd(0x2B);
    TFT_WriteData16(y0);
    TFT_WriteData16(y1);
    
    // 写入GRAM
    TFT_WriteCmd(0x2C);
}

// 填充颜色
void TFT_Fill(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1, uint16_t color)
{
    uint32_t i, count = (x1 - x0 + 1) * (y1 - y0 + 1);
    TFT_SetWindow(x0, y0, x1, y1);
    
    gpio_bit_reset(TFT_CS_PORT, TFT_CS_PIN);
    gpio_bit_set(TFT_DC_PORT, TFT_DC_PIN);
    
    for(i = 0; i < count; i++) {
        SPI_SendByte(color >> 8);
        SPI_SendByte(color & 0xFF);
    }
    
    gpio_bit_set(TFT_CS_PORT, TFT_CS_PIN);
}

// 绘制点
void TFT_DrawPoint(uint16_t x, uint16_t y, uint16_t color)
{
    TFT_SetWindow(x, y, x, y);
    TFT_WriteData16(color);
}

// 初始化TFT LCD
void TFT_Init(void)
{
    // 初始化SPI
    SPI_Init();
    
    // 复位
    gpio_bit_reset(TFT_RST_PORT, TFT_RST_PIN);
    delay_ms(100);
    gpio_bit_set(TFT_RST_PORT, TFT_RST_PIN);
    delay_ms(100);
    
    // 初始化序列
    TFT_WriteCmd(0x11);  // 睡眠退出
    delay_ms(120);
    
    // 像素格式设置
    TFT_WriteCmd(0x3A);
    TFT_WriteData(0x05);  // 16位模式
    
    // 显示开
    TFT_WriteCmd(0x29);
    
    // 清屏
    TFT_Fill(0, 0, 127, 127, BLACK);
}
```

## OLED 显示

### 1. I2C 接口 OLED
- **特点**：低功耗、高对比度、视角广
- **接口**：I2C
- **分辨率**：常见128x64

### STC系列微控制器实现

```c
#include "stc8.h"

#define SCL P3_2
#define SDA P3_3
#define OLED_ADDR 0x78

// 延时函数
void I2C_Delay(void)
{
    uint8_t i = 10;
    while(i--);
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
    I2C_ReceiveAck();
}

// 向OLED发送命令
void OLED_WriteCmd(uint8_t cmd)
{
    I2C_Start();
    I2C_SendByte(OLED_ADDR);
    I2C_SendByte(0x00);  // 命令
    I2C_SendByte(cmd);
    I2C_Stop();
}

// 向OLED发送数据
void OLED_WriteData(uint8_t data)
{
    I2C_Start();
    I2C_SendByte(OLED_ADDR);
    I2C_SendByte(0x40);  // 数据
    I2C_SendByte(data);
    I2C_Stop();
}

// 初始化OLED
void OLED_Init(void)
{
    OLED_WriteCmd(0xAE);  // 关闭显示
    OLED_WriteCmd(0x00);  // 设置列低地址
    OLED_WriteCmd(0x10);  // 设置列高地址
    OLED_WriteCmd(0x40);  // 设置起始行
    OLED_WriteCmd(0xB0);  // 设置页地址
    OLED_WriteCmd(0x81);  // 设置对比度
    OLED_WriteCmd(0xFF);  // 对比度最大值
    OLED_WriteCmd(0xA1);  // 设置段重映射
    OLED_WriteCmd(0xA6);  // 正常显示
    OLED_WriteCmd(0xA8);  // 设置多路复用率
    OLED_WriteCmd(0x3F);  // 1/64 duty
    OLED_WriteCmd(0xC8);  // 设置COM扫描方向
    OLED_WriteCmd(0xD3);  // 设置显示偏移
    OLED_WriteCmd(0x00);  // 无偏移
    OLED_WriteCmd(0xD5);  // 设置时钟分频因子
    OLED_WriteCmd(0x80);  // 默认值
    OLED_WriteCmd(0xD9);  // 设置预充电周期
    OLED_WriteCmd(0xF1);  // 预充电周期
    OLED_WriteCmd(0xDA);  // 设置COM硬件引脚配置
    OLED_WriteCmd(0x12);  // 交替 COM pin config
    OLED_WriteCmd(0xDB);  // 设置VCOMH
    OLED_WriteCmd(0x40);  // VCOMH
    OLED_WriteCmd(0xAF);  // 开启显示
}

// 清屏
void OLED_Clear(void)
{
    uint8_t page, column;
    for(page = 0; page < 8; page++) {
        OLED_WriteCmd(0xB0 + page);  // 设置页地址
        OLED_WriteCmd(0x00);  // 设置列低地址
        OLED_WriteCmd(0x10);  // 设置列高地址
        for(column = 0; column < 128; column++) {
            OLED_WriteData(0x00);  // 写入0，清屏
        }
    }
}

// 设置位置
void OLED_SetPos(uint8_t x, uint8_t y)
{
    OLED_WriteCmd(0xB0 + y);  // 设置页地址
    OLED_WriteCmd((x & 0x0F));  // 设置列低地址
    OLED_WriteCmd(0x10 + ((x >> 4) & 0x0F));  // 设置列高地址
}

// 显示字符
void OLED_DisplayChar(uint8_t x, uint8_t y, uint8_t chr)
{
    uint8_t c = 0, i = 0;
    c = chr - ' ';
    if(x > 127) {
        x = 0;
        y++;
    }
    OLED_SetPos(x, y);
    for(i = 0; i < 6; i++) {
        OLED_WriteData(Font6x8[c][i]);
    }
}

// 显示字符串
void OLED_DisplayString(uint8_t x, uint8_t y, char *str)
{
    uint8_t len = 0;
    while(*str != '\0') {
        OLED_DisplayChar(x + len * 6, y, *str++);
        len++;
    }
}

// 6x8字体
uint8_t Font6x8[][6] = {
    {0x00, 0x00, 0x00, 0x00, 0x00, 0x00},  // 空格
    {0x00, 0x00, 0x00, 0x2f, 0x00, 0x00},  // !
    // 其他字符省略...
};
```

### 2. SPI 接口 OLED
- **特点**：高速传输、适合显示动态内容
- **接口**：SPI

### GD32系列微控制器实现

```c
#include "gd32f4xx.h"

// 定义OLED引脚
#define OLED_CS_PORT GPIOA
#define OLED_CS_PIN GPIO_PIN_4
#define OLED_DC_PORT GPIOA
#define OLED_DC_PIN GPIO_PIN_5
#define OLED_RST_PORT GPIOA
#define OLED_RST_PIN GPIO_PIN_6

// 初始化SPI
void SPI_Init(void)
{
    // 使能GPIO时钟
    rcu_periph_clock_enable(RCU_GPIOA);
    // 使能SPI0时钟
    rcu_periph_clock_enable(RCU_SPI0);
    
    // 配置PA5为SPI0_SCK
    gpio_af_set(GPIOA, GPIO_AF_5, GPIO_PIN_5);
    // 配置PA7为SPI0_MOSI
    gpio_af_set(GPIOA, GPIO_AF_5, GPIO_PIN_7);
    
    // 配置控制引脚
    gpio_mode_set(OLED_CS_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, OLED_CS_PIN);
    gpio_mode_set(OLED_DC_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, OLED_DC_PIN);
    gpio_mode_set(OLED_RST_PORT, GPIO_MODE_OUTPUT, GPIO_PUPD_PULLUP, OLED_RST_PIN);
    
    // 配置GPIO
    gpio_mode_set(GPIOA, GPIO_MODE_AF, GPIO_PUPD_PULLUP, GPIO_PIN_5 | GPIO_PIN_7);
    gpio_output_options_set(GPIOA, GPIO_OTYPE_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_4 | GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7);
    
    // 配置SPI0
    spi_deinit(SPI0);
    spi_init(SPI0, SPI_MODE_MASTER, SPI_TRANSMODE_FULLDUPLEX, SPI_FRAMESIZE_8BIT, SPI_NSS_SOFT, 4);
    spi_enable(SPI0);
    
    // 初始化解选
    gpio_bit_set(OLED_CS_PORT, OLED_CS_PIN);
}

// 发送SPI数据
void SPI_SendByte(uint8_t data)
{
    // 等待发送缓冲区为空
    while(RESET == spi_flag_get(SPI0, SPI_FLAG_TBE));
    // 发送数据
    spi_data_transmit(SPI0, data);
    // 等待接收缓冲区非空
    while(RESET == spi_flag_get(SPI0, SPI_FLAG_RBNE));
    // 读取接收数据
    spi_data_receive(SPI0);
}

// 写命令
void OLED_WriteCmd(uint8_t cmd)
{
    gpio_bit_reset(OLED_CS_PORT, OLED_CS_PIN);
    gpio_bit_reset(OLED_DC_PORT, OLED_DC_PIN);
    SPI_SendByte(cmd);
    gpio_bit_set(OLED_CS_PORT, OLED_CS_PIN);
}

// 写数据
void OLED_WriteData(uint8_t data)
{
    gpio_bit_reset(OLED_CS_PORT, OLED_CS_PIN);
    gpio_bit_set(OLED_DC_PORT, OLED_DC_PIN);
    SPI_SendByte(data);
    gpio_bit_set(OLED_CS_PORT, OLED_CS_PIN);
}

// 初始化OLED
void OLED_Init(void)
{
    // 初始化SPI
    SPI_Init();
    
    // 复位
    gpio_bit_reset(OLED_RST_PORT, OLED_RST_PIN);
    delay_ms(100);
    gpio_bit_set(OLED_RST_PORT, OLED_RST_PIN);
    delay_ms(100);
    
    // 初始化序列
    OLED_WriteCmd(0xAE);  // 关闭显示
    OLED_WriteCmd(0x00);  // 设置列低地址
    OLED_WriteCmd(0x10);  // 设置列高地址
    OLED_WriteCmd(0x40);  // 设置起始行
    OLED_WriteCmd(0xB0);  // 设置页地址
    OLED_WriteCmd(0x81);  // 设置对比度
    OLED_WriteCmd(0xFF);  // 对比度最大值
    OLED_WriteCmd(0xA1);  // 设置段重映射
    OLED_WriteCmd(0xA6);  // 正常显示
    OLED_WriteCmd(0xA8);  // 设置多路复用率
    OLED_WriteCmd(0x3F);  // 1/64 duty
    OLED_WriteCmd(0xC8);  // 设置COM扫描方向
    OLED_WriteCmd(0xD3);  // 设置显示偏移
    OLED_WriteCmd(0x00);  // 无偏移
    OLED_WriteCmd(0xD5);  // 设置时钟分频因子
    OLED_WriteCmd(0x80);  // 默认值
    OLED_WriteCmd(0xD9);  // 设置预充电周期
    OLED_WriteCmd(0xF1);  // 预充电周期
    OLED_WriteCmd(0xDA);  // 设置COM硬件引脚配置
    OLED_WriteCmd(0x12);  // 交替 COM pin config
    OLED_WriteCmd(0xDB);  // 设置VCOMH
    OLED_WriteCmd(0x40);  // VCOMH
    OLED_WriteCmd(0xAF);  // 开启显示
    
    // 清屏
    OLED_Clear();
}

// 清屏
void OLED_Clear(void)
{
    uint8_t page, column;
    for(page = 0; page < 8; page++) {
        OLED_WriteCmd(0xB0 + page);  // 设置页地址
        OLED_WriteCmd(0x00);  // 设置列低地址
        OLED_WriteCmd(0x10);  // 设置列高地址
        for(column = 0; column < 128; column++) {
            OLED_WriteData(0x00);  // 写入0，清屏
        }
    }
}

// 设置位置
void OLED_SetPos(uint8_t x, uint8_t y)
{
    OLED_WriteCmd(0xB0 + y);  // 设置页地址
    OLED_WriteCmd((x & 0x0F));  // 设置列低地址
    OLED_WriteCmd(0x10 + ((x >> 4) & 0x0F));  // 设置列高地址
}

// 显示字符
void OLED_DisplayChar(uint8_t x, uint8_t y, uint8_t chr)
{
    uint8_t c = 0, i = 0;
    c = chr - ' ';
    if(x > 127) {
        x = 0;
        y++;
    }
    OLED_SetPos(x, y);
    for(i = 0; i < 6; i++) {
        OLED_WriteData(Font6x8[c][i]);
    }
}

// 显示字符串
void OLED_DisplayString(uint8_t x, uint8_t y, char *str)
{
    uint8_t len = 0;
    while(*str != '\0') {
        OLED_DisplayChar(x + len * 6, y, *str++);
        len++;
    }
}
```

## 显示设备应用示例

### 1. 温湿度监测显示系统

**功能说明**：使用DHT11温湿度传感器采集数据，在LCD上显示温湿度值。

**硬件需求**：
- 微控制器开发板
- DHT11温湿度传感器
- 1602 LCD显示屏

**软件设计**：
- 初始化LCD和DHT11
- 定期采集温湿度数据
- 在LCD上显示数据

**实现代码**：

```c
#include "stc8.h"

// LCD和DHT11初始化
void System_Init(void)
{
    LCD_Init();
    DHT11_Init();
}

// 主函数
void main(void)
{
    System_Init();
    
    uint8_t temperature, humidity;
    char buffer[20];
    
    while(1) {
        // 读取温湿度
        if(DHT11_ReadData(&temperature, &humidity)) {
            // 显示温度
            sprintf(buffer, "Temp: %dC", temperature);
            LCD_DisplayString(0, 0, buffer);
            
            // 显示湿度
            sprintf(buffer, "Humidity: %d%%", humidity);
            LCD_DisplayString(1, 0, buffer);
        } else {
            LCD_DisplayString(0, 0, "Error reading DHT11");
        }
        
        // 延时
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
        Delay10ms();
    }
}
```

### 2. 实时时钟显示系统

**功能说明**：使用RTC模块获取时间，在OLED上显示当前时间。

**硬件需求**：
- 微控制器开发板
- DS3231 RTC模块
- OLED显示屏

**软件设计**：
- 初始化OLED和I2C
- 从RTC模块读取时间
- 在OLED上显示时间

**实现代码**：

```c
#include "gd32f4xx.h"

// 从DS3231读取时间
void DS3231_ReadTime(uint8_t *hour, uint8_t *minute, uint8_t *second)
{
    // 读取秒
    I2C_Start();
    I2C_SendByte(0xD0);  // DS3231地址
    I2C_SendByte(0x00);  // 秒寄存器
    I2C_Start();
    I2C_SendByte(0xD1);  // 读模式
    *second = BCD_to_DEC(I2C_ReceiveByte());
    I2C_SendAck(0);
    
    // 读取分
    *minute = BCD_to_DEC(I2C_ReceiveByte());
    I2C_SendAck(0);
    
    // 读取时
    *hour = BCD_to_DEC(I2C_ReceiveByte());
    I2C_SendAck(1);
    I2C_Stop();
}

// BCD转十进制
uint8_t BCD_to_DEC(uint8_t bcd)
{
    return (bcd >> 4) * 10 + (bcd & 0x0F);
}

// 主函数
int main(void)
{
    // 初始化
    OLED_Init();
    I2C_Init();
    
    uint8_t hour, minute, second;
    char buffer[20];
    
    while(1) {
        // 读取时间
        DS3231_ReadTime(&hour, &minute, &second);
        
        // 显示时间
        sprintf(buffer, "%02d:%02d:%02d", hour, minute, second);
        OLED_Clear();
        OLED_DisplayString(32, 3, buffer);
        
        // 延时
        delay_ms(1000);
    }
}
```

## 常见问题与解决方案

### 1. 显示设备无显示
- **症状**：显示设备没有任何显示
- **解决方案**：检查电源、检查接线、检查初始化代码

### 2. 显示内容乱码
- **症状**：显示内容不正确或乱码
- **解决方案**：检查时序、检查数据传输、检查字体数据

### 3. 显示闪烁
- **症状**：显示内容闪烁
- **解决方案**：检查电源稳定性、优化刷新频率、检查接地

### 4. 显示对比度问题
- **症状**：显示太暗或太亮
- **解决方案**：调整对比度设置、检查电源电压

## 总结

显示设备是嵌入式系统中与用户交互的重要界面，选择合适的显示设备并正确实现驱动对于系统的用户体验至关重要。本文档介绍了常见显示设备的工作原理、接口方式以及在不同系列微控制器上的驱动实现，包括LED、LCD和OLED等。

通过本章节的学习，您应该能够：
1. 了解常见显示设备的基本原理和特点
2. 在不同系列微控制器上实现显示设备驱动
3. 设计基于显示设备的用户界面
4. 解决显示设备使用过程中的常见问题
5. 开发完整的显示系统应用