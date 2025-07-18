#include "esp_sntp.h"
#include <driver/i2c.h>
#include <esp_log.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <lwip/sockets.h>
#include <stdio.h>
#include <DS1307.h>
#include "sdkconfig.h"

#define SDA_PIN 19
#define SCL_PIN 18
#define DS1307_ADDRESS 0x68

static const char *TAG = "MAIN";

extern "C" void app_main(void) {
    ESP_LOGI(TAG, "Start MAIN.");

    DS1307 rtc(DS1307_ADDRESS, SDA_PIN, SCL_PIN);
    rtc.readValue();

    // (sec, min, hour, day, wday, mon, year)
    rtc.setTime(45, 30, 14, 4, 16, 8, 2023);
    rtc.readValue();
    
    // rtc.setSpecific(12, 0x00);
    rtc.setSpecific(19, 0x01);
    // rtc.setSpecific(22, 0x02);
    // rtc.setSpecific(5, 0x03);
    rtc.setSpecific(4, 0x04);
    // rtc.setSpecific(9, 0x05);
    rtc.setSpecific(2004, 0x06);

    rtc.readRegister(0);
    rtc.readRegister(1);
    rtc.readRegister(2);
    rtc.readRegister(3);
    rtc.readRegister(4);
    rtc.readRegister(5);
    rtc.readRegister(6);

    while(true) {
        rtc.readValue();
        vTaskDelay(1000/portTICK_PERIOD_MS);
    }
}