/* Blink Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "led_strip.h"
#include "sdkconfig.h"
#include "CLed.h"
#include "CButton.h"

static const char *TAG = "MAIN";    // string za identifikaciju modula

/* Use project configuration menu (idf.py menuconfig) to choose the GPIO to blink,
   or you can edit the following line and set a number here.
*/
#define BLINK_GPIO 2 //CONFIG_BLINK_GPIO
#define BUTTON_GPIO 15  // GPIO za button


CLed cled(BLINK_GPIO);  // stvori objekt klase s vrijednoscu BLINK_GPIO
//
//Task Loop
//
void task_loop (void *parameters)
{
    ESP_LOGI(TAG, "Start TASK Loop.");
    
    CLed *led;
    //Cast parameter
    led = (CLed*)parameters;
    ESP_LOGI(TAG, "Get Led pointer.");
    
    while(1) {
        //Do tick
        led->tick();  
        vTaskDelay(100 / portTICK_PERIOD_MS);      
    }
}

void button_task_loop(void *parameters) {   // funkcija koja se koristi kao task
    ESP_LOGI(TAG, "Start button TASK loop.");

    CButton *button;

    button = (CButton*)parameters;
    ESP_LOGI(TAG, "Get Button pointer.");

    while(1) {  // funkcija za obradu tipke
        //Do tick
        button->tick();     // ocitavanje statusa tipke
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}

void singleClickHandler() {
    ESP_LOGI(TAG, "Single click detected");
    if (cled.getLedStatus() == OFF) {
        cled.setLedState(ON);
    } 
    else {
        cled.setLedState(OFF);
    }
}

void doubleClickHandler() {
    ESP_LOGI(TAG, "Double click detected");
    
    cled.setLedState(FAST_BLINK);
}

void longPressHandler() {
    ESP_LOGI(TAG, "Long press detected");
    
    cled.setLedState(SLOW_BLINK);
}

TaskHandle_t xHandle = NULL;
TaskHandle_t buttonHandle = NULL;

//ESP32 mian function
extern "C" void app_main(void)
{
    ESP_LOGI(TAG, "Start MAIN.");
    
    //Create CLed object
    CLed led1(BLINK_GPIO);
    //Create CButton object
    CButton button(BUTTON_GPIO);

    // callback funkcije
    button.attachSingleClick(singleClickHandler);   // spaja funkciju sa dogadajem
    button.attachDoubleClick(doubleClickHandler);
    button.attachLongPress(longPressHandler);

    led1.setLedState(LedStatus::OFF);

    //Create Task
    
    ESP_LOGI(TAG, "Start Task Create.");
    xTaskCreate(task_loop,      //Task function
                "ledLoop",      //Name of task in task scheduler
                1024*5,         //Stack size
                (void*)&led1,   //Parameter send to function
                1,              //Priority
                &xHandle);      //task handler 
    ESP_LOGI(TAG, "Task Created.");

    ESP_LOGI(TAG, "Start Button Task Create.");
    xTaskCreate(button_task_loop,      //kreiraj i pokreni novi zadatak u FreeRTOS -funkcija koja ce biti izvrsena kao zadatak
                "buttonLoop",       //Name of task in task scheduler
                1024*2,             //Stack size
                (void*)&button,     //Parameter send to function
                1,                  //Priority
                &buttonHandle);     //task handler 
    ESP_LOGI(TAG, "Button Task Created.");
    
    //Main loop
    while(1) {
        // led1.setLedState(LedStatus::BLINK);
        // vTaskDelay(10000 / portTICK_PERIOD_MS);

        // led1.setLedState(LedStatus::FAST_BLINK);
        // vTaskDelay(10000 / portTICK_PERIOD_MS);

        // led1.setLedState(LedStatus::SLOW_BLINK);
        // vTaskDelay(10000 / portTICK_PERIOD_MS);

        cled.tick();
        button.tick();
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }

}
