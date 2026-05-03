#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "bsec_interface.h"
#include "bme68x.h"
#include "bsec_datatypes.h"

/*
 NOTE:
 You must link:
 - bsec library
 - bme68x driver
 - I2C implementation for Raspberry Pi
*/

int main(void)
{
    struct bsec_output outputs[BSEC_NUMBER_OUTPUTS];
    uint8_t n_outputs = 0;

    // Initialize BSEC
    if (bsec_init() != BSEC_OK)
    {
        printf("BSEC init failed\n");
        return -1;
    }

    // Configure virtual sensors
    bsec_sensor_configuration_t virtual_sensors[6];

    virtual_sensors[0].sensor_id = BSEC_OUTPUT_IAQ;
    virtual_sensors[1].sensor_id = BSEC_OUTPUT_CO2_EQUIVALENT;
    virtual_sensors[2].sensor_id = BSEC_OUTPUT_BREATH_VOC_EQUIVALENT;
    virtual_sensors[3].sensor_id = BSEC_OUTPUT_RAW_TEMPERATURE;
    virtual_sensors[4].sensor_id = BSEC_OUTPUT_RAW_PRESSURE;
    virtual_sensors[5].sensor_id = BSEC_OUTPUT_RAW_HUMIDITY;
    virtual_sensors[6].sensor_id = BSEC_OUTPUT_RAW_GAS;

    bsec_update_subscription(virtual_sensors, 6, virtual_sensors, &n_outputs);

    while (1)
    {
        bsec_do_steps(NULL, 0, outputs, &n_outputs);

        float temp = 0, hum = 0, press = 0;
        float iaq = 0, co2 = 0, voc = 0;
        float gas = 0;

        for (int i = 0; i < n_outputs; i++)
        {
            switch (outputs[i].sensor_id)
            {
                case BSEC_OUTPUT_IAQ:
                    iaq = outputs[i].signal;
                    break;

                case BSEC_OUTPUT_CO2_EQUIVALENT:
                    co2 = outputs[i].signal;
                    break;

                case BSEC_OUTPUT_BREATH_VOC_EQUIVALENT:
                    voc = outputs[i].signal;
                    break;

                case BSEC_OUTPUT_RAW_TEMPERATURE:
                    temp = outputs[i].signal;
                    break;

                case BSEC_OUTPUT_RAW_HUMIDITY:
                    hum = outputs[i].signal;
                    break;

                case BSEC_OUTPUT_RAW_PRESSURE:
                    press = outputs[i].signal;
                    break;

                case BSEC_OUTPUT_RAW_GAS:
                     gas = outputs[i].signal;
                     break;
            }
        }

        // OUTPUT FOR PYTHON
        printf("temp:%.2f,hum:%.2f,press:%.2f,gas:%.2f,iaq:%.2f,co2:%.2f,voc:%.2f\n",
               temp, hum, press, gas ,iaq, co2, voc);

        fflush(stdout);

        sleep(1);
    }

    return 0;
}