#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "driver/adc.h"
#include "esp_log.h"
#include "CButton.h"
#include "esp_err.h"
#include <string.h>
#include <rom/ets_sys.h>
#include "../../../../esp/v5.4/esp-idf/components/esp_adc/deprecated/include/esp_adc_cal_types_legacy.h"
#include "../../../../esp/v5.4/esp-idf/components/esp_adc/deprecated/include/esp_adc_cal.h"


#define BUTTON_GPIO 13
#define Vin 5.0
#define TAG "MAIN"

static esp_adc_cal_characteristics_t *adc_chars;

esp_err_t dht_read_data(gpio_num_t pin, float *humidity, float *temperature) {
    // pripremi za citanje dht
    int data[40] = {0};     // dht senzor salje 40 bitova informacija
    uint8_t byte_index = 0, bit_index = 0;  // trenutni bajt, bit u bajtu
    uint8_t bits[5] = {0};  // niz od 5 bajtova

    // inicijalizacija komunikacije s dht, start signal
    gpio_set_direction(pin, GPIO_MODE_OUTPUT);
    gpio_set_level(pin, 0);     // zapocni komunikaciju, pin na low
    vTaskDelay(pdMS_TO_TICKS(20));  // low 20ms
    gpio_set_level(pin, 1);     // postavi pin na high, dht treba odgovoriti
    ets_delay_us(40);   // cekaj 40 μs
    gpio_set_direction(pin, GPIO_MODE_INPUT);   // prati odgovor senzora

    // cekanje odgovora, sinkronizacija
    uint32_t t = 0;
    while (gpio_get_level(pin) == 1) {  // cekaj pocetak odgovora od senzora
        ets_delay_us(1);
        if (++t > 80) return ESP_ERR_TIMEOUT;
    }

    t = 0;
    while (gpio_get_level(pin) == 0){   // potvrda senzora
        ets_delay_us(1);
        if (++t > 80) return ESP_ERR_TIMEOUT;
    }

    t = 0;
    while (gpio_get_level(pin) == 1) {  // cekaj zavrsetak potvrde
        ets_delay_us(1);
        if (++t > 80) return ESP_ERR_TIMEOUT;
    }

    // citanje podataka sa dht
    for (int i=0; i<40; i++) {  // citaj 40 bita od senzora
        while (gpio_get_level(pin) == 0);   // cekaj dok pin ne postane high
        ets_delay_us(30);   // standard kako bi se odlucilo 1 ili 0
        if (gpio_get_level(pin) == 1) {
            data[i] = 1;
        } else {
            data[i] = 0;
        }
        while (gpio_get_level(pin) == 1);   // cekaj dok pin ne postane low
    }

    // bitovi u bajtove
    for (int i=0; i<5; i++) {
        for (int j=0; j<8; j++) {
            bits[i] <<= 1;
            bits[i] |= data[i*8+j];
        }
    }

    // checksum
    if (((bits[0] + bits[1] + bits[2] + bits[3]) & 0xFF) != bits[4]) {
        ESP_LOGE("DHT", "Checksum error");
        return ESP_FAIL;
    }

    // zapis podataka
    *humidity = ((bits[0] << 8) + bits[1]) / 10.0;
    *temperature = (((bits[2] & 0x7F) << 8) + bits[3]) / 10.0;
    if (bits[2] & 0x80) {
        *temperature = -*temperature;
    }

    return ESP_OK;
}

void singleClickHandler() {
    // Vout = Vin * (Rntc / (Rntc + Rfix)) - djelitelj napona
    double Vout = adc1_get_raw(ADC1_CHANNEL_6) / 1000.0;
    double voltageRatio = Vout / Vin;   
    double resistance = (voltageRatio * 10000) / (1 - voltageRatio);    // otpor NTC

    ESP_LOGI(TAG, "Vout: %.3f V", Vout);
    ESP_LOGI(TAG, "Resistance: %.2f Ω", resistance);

    // Steinhart-Hart koeficijenti (najmanja, najveca i srednja vrijednost)
    double A = 0.002542128997;
    double B = -0.00003850219075;
    double C = 0.000001674298236;

    // 1/T = A + B*ln(R) + C*(ln(R))^3
    double temperatureNTC = 1.0 / (A + B * log(resistance) + C * pow(log(resistance), 3)) - 273.15;
    ESP_LOGI(TAG, "Temperature (NTC): %.2f °C", temperatureNTC);

    // ocitanje DHT22
    float humidity;
    float temperatureDHT;
    if (dht_read_data(GPIO_NUM_15, &humidity, &temperatureDHT) == ESP_OK) {
        ESP_LOGI("DHT", "Temperature (DHT22): %.2f °C, Humidity: %.1f %%\n", temperatureDHT, humidity);
    } else {
        ESP_LOGW(TAG, "Failed to read from DHT22");
    }
}


extern "C" void app_main(void) {
    // ADC konfiguracija
    adc1_config_width(ADC_WIDTH_BIT_12);    // postavi rezoluciju (12-bitna razlucivost)
    adc1_config_channel_atten(ADC1_CHANNEL_6, ADC_ATTEN_DB_12);    // omoguci ocitanje signala na odabranom kanalu

    // omoguci pretvaranje sirovih adc u stvarni napon
    adc_chars = (esp_adc_cal_characteristics_t *)calloc(1, sizeof(esp_adc_cal_characteristics_t));
    esp_adc_cal_characterize(ADC_UNIT_1, ADC_ATTEN_DB_12, ADC_WIDTH_BIT_12, 1100, adc_chars);   // kako pretvoriti sirovu vrijednost u napon

    ESP_LOGI(TAG, "System start");

    // Inicijalizacija gumba
    CButton button(BUTTON_GPIO);
    button.attachSingleClick(singleClickHandler);

    while (1) {
        button.tick();
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}