# Accessing GPIO on Nanopi

- Install [WiringNP](https://github.com/friendlyarm/WiringNP)
- Find your GPIO "linux pin" on the official docs - Nano pi neo 2 for example:
----
### GPIO Pin Description Example
| Pin# | Name | Linux gpio | Pin# | Name | Linux gpio |
| ---| ---| ---| ---| ---| ---|
| 1 | SYS_3.3V | | 2 | VDD_5V	|
| 3	| I2C0_SDA/GPIOA12 | 12 | 4 | VDD_5V |
| 5	| I2C0_SCL/GPIOA11 | 11	| 6 | GND |
| 7	| GPIOG11 | 203 | 8 | UART1_TX/GPIOG6 | 198 |
| 9	| GND | | 10 | UART1_RX/GPIOG7 | 199 |
| 11 | UART2_TX/GPIOA0 | 0 | 12 | GPIOA6 | 6 |
| 13 | UART2_RTS/GPIOA2	| 2 | 14 | GND |
| 15 | UART2_CTS/GPIOA3	| 3 | 16 | UART1_RTS/GPIOG8 | 200 |
| 17 | SYS_3.3V	 | 18 | | UART1_CTS/GPIOG9 | 201 |
| 19 | SPI0_MOSI/GPIOC0	| 64 | 20 | GND	|
| 21 | SPI0_MISO/GPIOC1	| 65 | 22 | UART2_RX/GPIOA1	| 1 |
| 23 | SPI0_CLK/GPIOC2 | 66 | 24 | SPI0_CS/GPIOC3 |67 |

---
## Enable the pin
- Enable it in /sys/class/gpio/

## Example
```sh
    echo "203" >/sys/class/gpio/export # Set the pin
    echo "out" >/sys/class/gpio/gpio203/direction # Set pin as "in" or "out"
```

## Use the pin
```sh
    echo "1" >/sys/class/gpio/gpio203/value # on
    echo "0" >/sys/class/gpio/gpio203/value # off
