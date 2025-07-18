#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "sdkconfig.h"
#include "CButton.h"

CButton::CButton(int port){
    m_pinNumber = (gpio_num_t)port;
    ESP_LOGI(LogName, "Configure port[%d] to input.", port);
    gpio_reset_pin(m_pinNumber);
    gpio_set_direction(m_pinNumber, GPIO_MODE_INPUT);
}

void CButton::tick(){
    bool buttonState = !gpio_get_level(m_pinNumber);
    if (buttonState) {
        buttonPressed = true;
    } else {
        if (buttonPressed) {
            singleClick();
            buttonPressed = false;
        }
    }
}
