#include "esp_sntp.h"
#include <driver/i2c.h>
#include <esp_log.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <lwip/sockets.h>
#include <stdio.h>
#include <DS1307.h>
#include "sdkconfig.h"

#define YEAR_DS 2000
static const char *TAG = "DS1307";

// inicijalizacija i2c sabirnice
DS1307::DS1307(unsigned char ds1307_address, int SDA_pin, int SCL_pin) {
    address = ds1307_address;
    i2c_config_t config;    // kreiraj strukturu koja ce se napuniti podacima za konfiguraciju i2c sabirnice
    config.mode = I2C_MODE_MASTER;  // postavi esp32 da bude master na i2c sabirnici
    config.sda_io_num = SDA_pin;
    config.scl_io_num = SCL_pin;
    config.sda_pullup_en = GPIO_PULLUP_ENABLE;  // omoguci pull up otpornike
    config.scl_pullup_en = GPIO_PULLUP_ENABLE;
    config.master.clk_speed = 100000;   // postavi brzinu i2c na 100 kHz
    config.clk_flags = 0;
    i2c_param_config(I2C_NUM_0, &config);   // primjeni konfiguraciju na i2c port 0
    i2c_driver_install(I2C_NUM_0, I2C_MODE_MASTER, 0, 0, 0);    // instalira i2c driver za port 0 u master modu
}

// pretvori decimalni broj u binary-coded decimal
uint8_t DS1307::intToBCD(uint8_t num) {
    return ((num / 10) << 4) | (num % 10);
}

// pretvori iz BCD u decimalni broj
uint8_t DS1307::BCDToInt(uint8_t num) {
    return ((num >> 4) * 10) + (num & 0x0f);
}

// postavi vrijeme
void DS1307::setTime(uint8_t sec, uint8_t min, uint8_t hour, uint8_t wday, uint8_t day, uint8_t mon, int year) {
    char y = year - YEAR_DS;   // ds1307 sadrzava godinu od 0 do 99
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();   // prazna lista komandi
    i2c_master_start(cmd);  // pocetak komunikacije
    i2c_master_write_byte(cmd, (address << 1) | I2C_MASTER_WRITE, true);    // salji adresu slave uredaja na i2c, pisanje, ocekuj potvrdu ACK
    i2c_master_write_byte(cmd, 0x0, true);  // pocetna adresa gdje pisemo
    i2c_master_write_byte(cmd, intToBCD(sec), true);
    i2c_master_write_byte(cmd, intToBCD(min), true);    // za svaki bajt se automatski inkrementira interna adresa
    i2c_master_write_byte(cmd, intToBCD(hour), true);
    i2c_master_write_byte(cmd, intToBCD(wday+1), true); // 1 - 7
    i2c_master_write_byte(cmd, intToBCD(day), true);
    i2c_master_write_byte(cmd, intToBCD(mon), true);
    i2c_master_write_byte(cmd, intToBCD(y), true);
    i2c_master_stop(cmd);   // zavrsi prijenos
    i2c_master_cmd_begin(I2C_NUM_0, cmd, 1000/portTICK_PERIOD_MS);  // pokreni komande
    i2c_cmd_link_delete(cmd);   // oslobodi memoriju
}

// citaj vrijeme
void DS1307::readValue() {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();   // prazna lista komandi
    uint8_t data[7];    // 7 bajtova vremena
    i2c_master_start(cmd);  // pocetak komunikacije
    i2c_master_write_byte(cmd, (address << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, 0x0, true);
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (address << 1) | I2C_MASTER_READ, true); // zelim citati
    i2c_master_read(cmd, data, 7, I2C_MASTER_NACK); // citaj 7 bajtova i spremi u data
    i2c_master_stop(cmd);
    i2c_master_cmd_begin(I2C_NUM_0, cmd, 1000/portTICK_PERIOD_MS);  // izvrsi
    i2c_cmd_link_delete(cmd);   // oslobodi memoriju

    int sec, min, hour, wday, day, month, year;
    sec = BCDToInt(data[0]);
    min = BCDToInt(data[1]);
    hour = BCDToInt(data[2]);
    wday = BCDToInt(data[3]);
    day = BCDToInt(data[4]);
    month = BCDToInt(data[5]);  // 0 - 11
    year = BCDToInt(data[6]);

    // const char* day_str = wday == 1 ? "Sunday" : wday == 2 ? "Monday" : wday == 3 ? "Tuesday" : wday == 4 ? "Wednesday" : wday == 5 ? "Thursday" : wday == 6 ? "Friday" : wday == 7 ? "Saturday" : "none";
    ESP_LOGI(TAG, "%d:%d:%d %d.%d.%d", hour, min, sec, day, month, year + YEAR_DS);
}

// postavi registar
void DS1307::setSpecific(int input, uint8_t position) {
    // if ((position == 0x00 && input > 59) || (position == 0x01 && input > 59) || (position == 0x02 && input > 23) || (position == 0x03 && input > 7) || (position == 0x04 && input > 31) || (position == 0x05 && input > 11)) {
    //     ESP_LOGI(TAG, "Could not set.");
    //     return;
    // }

    uint8_t value; 
    if(position == 0x06) {
        value = input - YEAR_DS;
    } else {
        value = input;
    }

	i2c_cmd_handle_t cmd = i2c_cmd_link_create();   // prazna lista komandi
    i2c_master_start(cmd);
	i2c_master_write_byte(cmd, (address << 1) | I2C_MASTER_WRITE, true);
	i2c_master_write_byte(cmd, position, true);
	i2c_master_write_byte(cmd, intToBCD(value), true);
	i2c_master_stop(cmd);
    i2c_master_cmd_begin(I2C_NUM_0, cmd, 1000/portTICK_PERIOD_MS);
	i2c_cmd_link_delete(cmd);
}

// citaj registar
void DS1307::readRegister(int reg) {
    // if (reg > 6 || reg < 0) {
    //     ESP_LOGI(TAG, "Wrong register");
    //     return;
    // }

    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
	i2c_master_start(cmd);
	i2c_master_write_byte(cmd, (address << 1) | I2C_MASTER_WRITE, 1);
	i2c_master_write_byte(cmd, 0x0 + reg, 1);
	i2c_master_start(cmd);
	i2c_master_write_byte(cmd, (address << 1) | I2C_MASTER_READ, 1);
	uint8_t data;
	i2c_master_read_byte(cmd, &data, I2C_MASTER_LAST_NACK);
	i2c_master_stop(cmd);
	i2c_master_cmd_begin(I2C_NUM_0, cmd, 1000/portTICK_PERIOD_MS);
	i2c_cmd_link_delete(cmd);

    int time_val = BCDToInt(data);

    if (reg == 0) {
        ESP_LOGI(TAG, "Seconds: %d", time_val);
    } else if (reg == 1) {
        ESP_LOGI(TAG, "Minutes: %d", time_val);
    } else if (reg == 2) {
        ESP_LOGI(TAG, "Hours: %d", time_val);
    } else if (reg == 3) {
        if (time_val == 1) {
            ESP_LOGI(TAG, "Sunday");
        } else if (time_val == 2) {
            ESP_LOGI(TAG, "Monday");
        } else if (time_val == 3) {
            ESP_LOGI(TAG, "Tuesday");
        } else if (time_val == 4) {
            ESP_LOGI(TAG, "Wednesday");
        } else if (time_val == 5) {
            ESP_LOGI(TAG, "Thursday");
        } else if (time_val == 6) {
            ESP_LOGI(TAG, "Friday");
        } else if (time_val == 7) {
            ESP_LOGI(TAG, "Saturday");
        }
    } else if (reg == 4) {
        ESP_LOGI(TAG, "Date: %d", time_val);
    } else if (reg == 5) {
        ESP_LOGI(TAG, "Month: %d", time_val);
    } else if (reg == 6) {
        ESP_LOGI(TAG, "Year: %d", (time_val + YEAR_DS));
    }

    return;
}