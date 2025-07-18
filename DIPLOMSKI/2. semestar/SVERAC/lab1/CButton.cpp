#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "sdkconfig.h"
#include "esp_timer.h"
#include "CButton.h"

#define DOUBLE_CLICK_TIME 300000    // 300 ms standardno vrijeme za dvostruki klik
#define LONG_PRESS_TIME 1000000     // 1 s standarsno vrijeme za prepoznati dugi pritisak

CButton::CButton(int port){     // configure port on constructor

    //ToDo::
    //BOOT is GPIO0 (HIGH when released, LOW when pressed)
    // tipka radi kao pull-up tipkalo (normalno = high, pritisak = low)
    pinNum = (gpio_num_t)port;  // gpio_num_t koji je GPIO pin u pitanju
    ESP_LOGI(LogName, "Configure port %d to input.", port); // ispisi poruku
    gpio_reset_pin(pinNum); // osiguraj da pin nema prethodno postavljene funkcije
    gpio_set_direction(pinNum, GPIO_MODE_INPUT);    // postavi pin kao ulaz (koristimo ga za tipkalo), citamo vrijednosti s tog pina
}

void CButton::tick(){
    //ToDo
    bool btnStatus;     // gpio_get_level citanje trenutnog stanja (naponske razine) pina
    if (gpio_get_level(pinNum) == 0) {  // low when pressed, tipka pritisunuta
        btnStatus = true;
    } else {    // high when released (visoka razina napona), tipka nije stisnuta
        btnStatus = false;
    }

    if (!btnStatus) {   // tipka nije pritisnuta (otpustena)
        if (handleEvent) {  // dogadaj je vec detektiran
            handleEvent = false;
            return;
        }
        if (prevTick) { // doslo je do promjene (otpustena je tipka)
            prevTick = false;
            pressBeforeBtn = true;
        }
        if (lastPressTime == 0) {   // tipka jos nije bila pritisnuta, nemamo sto obraditi
            return;
        }
        if(pressBeforeBtn && (esp_timer_get_time() - lastPressTime) >= DOUBLE_CLICK_TIME) { // prethodni klik registriraj ali ne kao dvoklik
            singleClick();
            lastPressTime = 0;
            pressBeforeBtn = false;
        }
    } else {    // tipka pritisnuta
        if (handleEvent) {  // dogadaj vec registriran i detektiran je trenutni press
            return;
        }
        if (lastPressTime == 0) {   // prati vrijeme prvog pritiska tipke
            lastPressTime = esp_timer_get_time();
            pressBeforeBtn = false;
        }
        if (pressBeforeBtn && (esp_timer_get_time() - lastPressTime) < DOUBLE_CLICK_TIME) { // detekcija dvostrukog klika
            doubleClick();
            lastPressTime = 0;
            handleEvent = true;
            pressBeforeBtn = false;
            return;
        }
        if ((esp_timer_get_time() - lastPressTime) >= LONG_PRESS_TIME) {    // detekcija long pressa
            handleEvent = true;
            longPress();
            lastPressTime = 0;
        }
        prevTick = true;    // prati tipku u sljedecem ciklusu
    }
}
