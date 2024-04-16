#include <stdio.h>
#include "pico/stdlib.h"
#define LED_PIN 21
#define BTN_PIN 20
const uint PERIOD = 40;

int main() {
    stdio_init_all();
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_init(BTN_PIN);
    gpio_set_dir(BTN_PIN, GPIO_IN);
    int i=0;
    int j=0;
    printf("Hello\n");
    printf("Hello\n");
    while (true) {
        gpio_put(LED_PIN, i/(PERIOD/2) ^ gpio_get(BTN_PIN));
        i++;
        if (i == PERIOD){
            i=0;
            printf("Hello. %d\n",j);
            j++;
        }
        sleep_ms(100);        
    }
}