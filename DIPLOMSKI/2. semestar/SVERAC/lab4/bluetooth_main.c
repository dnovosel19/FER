#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include "esp_log.h"
#include "esp_nimble_hci.h"
#include "nimble/nimble_port.h"
#include "nimble/nimble_port_freertos.h"
#include "host/ble_hs.h"
#include "services/gap/ble_svc_gap.h"
#include "services/gatt/ble_svc_gatt.h"
#include "sdkconfig.h"
#include "esp_bt.h"

char *TAG = "BLE-Server";
uint8_t ble_addr_type;
void ble_app_advertise(void);

static uint32_t counterBLE = 0;
static const char* readBLE = "1191249229";
static uint8_t writeBLE = 1;
static uint16_t conn_handle = 0;
uint16_t notify_handle = 0;

static int device_write(uint16_t conn_handle, uint16_t attr_handle, struct ble_gatt_access_ctxt *ctxt, void *arg) {
    if (ble_uuid_u16(ctxt->chr->uuid) == (0x9229 + 3)) {
        int new_value = *((uint8_t *)ctxt->om->om_data);
        if (new_value >= 1 && new_value <= 10) {
            writeBLE = new_value;
        }
    }
    return 0;
}

static int device_read(uint16_t conn_handle, uint16_t attr_handle, struct ble_gatt_access_ctxt *ctxt, void *arg) {
    const char* value;
    size_t value_len;

    if (ble_uuid_u16(ctxt->chr->uuid) == (0x9229 + 2)) {
        value = readBLE;
        value_len = strlen(readBLE);
    } else if (ble_uuid_u16(ctxt->chr->uuid) == (0x9229 + 1)) {
        value = (char *)&counterBLE;
        value_len = sizeof(counterBLE);
    } else {
        return BLE_ATT_ERR_UNLIKELY;
    }

    os_mbuf_append(ctxt->om, value, value_len);
    return 0;
}

static int device_notify(uint16_t conn_handle, uint16_t attr_handle, struct ble_gatt_access_ctxt *ctxt, void *arg) {
    char counter_str[20];
    snprintf(counter_str, sizeof(counter_str), "value: %lu", counterBLE);
    os_mbuf_append(ctxt->om, counter_str, strlen(counter_str));
    return 0;
}

static const struct ble_gatt_svc_def gatt_svcs[] = {
    {   .type = BLE_GATT_SVC_TYPE_PRIMARY,
        .uuid = BLE_UUID16_DECLARE(0x9229),     // Define UUID for device type
        .characteristics = (struct ble_gatt_chr_def[]) {
            {   .uuid = BLE_UUID16_DECLARE(0x9229 + 1),     // Define UUID for notify
                .flags = BLE_GATT_CHR_F_NOTIFY,
                .access_cb = device_notify,
                .val_handle = &notify_handle,
            },
            {   .uuid = BLE_UUID16_DECLARE(0x9229 + 2),     // Define UUID for reading
                .flags = BLE_GATT_CHR_F_READ,
                .access_cb = device_read,
            },
            {   .uuid = BLE_UUID16_DECLARE(0x9229 + 3),     // Define UUID for writing
                .flags = BLE_GATT_CHR_F_WRITE,
                .access_cb = device_write,
            },
            {0}},},
    {0}};

// BLE event handling
static int ble_gap_event(struct ble_gap_event *event, void *arg) {
    switch (event->type) {
        // Advertise if connected
        case BLE_GAP_EVENT_CONNECT:
            ESP_LOGI("GAP", "BLE GAP EVENT CONNECT %s", event->connect.status == 0 ? "OK!" : "FAILED!");
            if (event->connect.status == 0) {
                conn_handle = event->connect.conn_handle;
            } else {
                ble_app_advertise();
            }
            break;
        case BLE_GAP_EVENT_DISCONNECT:
            ESP_LOGI("GAP", "BLE GAP EVENT DISCONNECT");
            ble_app_advertise();
            break;
        // Advertise again after completion of the event
        case BLE_GAP_EVENT_ADV_COMPLETE:
            ESP_LOGI("GAP", "BLE GAP EVENT ADV COMPLETE");
            ble_app_advertise();
            break;
        default:
            break;
    }
    return 0;
}

// Define the BLE connection
void ble_app_advertise(void) {
    struct ble_hs_adv_fields fields;
    const char *device_name = "DominikNovosel";
    memset(&fields, 0, sizeof(fields));
    fields.name = (uint8_t *)device_name;
    fields.name_len = strlen(device_name);
    fields.name_is_complete = 1;
    ble_gap_adv_set_fields(&fields);

    // GAP - device connectivity definition
    struct ble_gap_adv_params adv_params;
    memset(&adv_params, 0, sizeof(adv_params));
    adv_params.conn_mode = BLE_GAP_CONN_MODE_UND;   // connectable or nonconnectable
    adv_params.disc_mode = BLE_GAP_DISC_MODE_GEN;   // discoverable or non-discoverable
    ble_gap_adv_start(ble_addr_type, NULL, BLE_HS_FOREVER, &adv_params, ble_gap_event, NULL);
}

void ble_app_on_sync(void) {
    ble_hs_id_infer_auto(0, &ble_addr_type);    // Determines the best address type automatically
    ble_app_advertise();    // Define the BLE connection
}

void host_task(void *param) {
    nimble_port_run();
}

void counter_task(void *param) {
    while (1) {
        ble_gatts_chr_updated(notify_handle);
        counterBLE += writeBLE;
        vTaskDelay(pdMS_TO_TICKS(1000)); 
    }
}

void app_main() {
    nvs_flash_init();   // 1 - Initialize NVS flash using
    // esp_nimble_hci_and_controller_init();    // 2 - Initialize ESP controller
    nimble_port_init();     // 3 - Initialize the host stack
    ble_svc_gap_device_name_set("DominikNovosel");  // 4 - Initialize NimBLE configuration - server name
    ble_svc_gap_init();     // 4 - Initialize NimBLE configuration - gap service
    ble_svc_gatt_init();    // 4 - Initialize NimBLE configuration - gatt service
    ble_gatts_count_cfg(gatt_svcs);     // 4 - Initialize NimBLE configuration - config gatt services
    ble_gatts_add_svcs(gatt_svcs);      // 4 - Initialize NimBLE configuration - queues gatt services.
    ble_hs_cfg.sync_cb = ble_app_on_sync;   // 5 - Initialize application
    nimble_port_freertos_init(host_task);   // 6 - Run the thread

    xTaskCreate(counter_task, "counter_task", 2048, NULL, 5, NULL);
}