#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/rtc.h"
#define LED_PIN 21
#define BTN_PIN 20
const uint PERIOD = 40;

void say_one(void){
    datetime_t t_1; 
    bool b=rtc_get_datetime(&t_1);
    printf("one %d %b \n",t_1.sec,b);
    printf("Date and Time: %04d-%02d-%02d %02d:%02d:%02d\n", 
           t_1.year, t_1.month, t_1.day, t_1.hour, t_1.min, t_1.sec);
}
void say_two(void){
    datetime_t t_2;
    bool b=rtc_get_datetime(&t_2);
    printf("two %d %b \n",t_2.sec,b);
   // printf("Date and Time: %04d-%02d-%02d %02d:%02d:%02d\n", 
   //        t_1.year, t_1.month, t_1.day, t_1.hour, t_1.min, t_1.sec);
}


int main() {
    stdio_init_all();
    printf("Step 0\n");
    sleep_ms(1000);   
    printf("Step 1\n");

    datetime_t t = {
        .year  = 2024,
        .month = 04,
        .day   = 18,
        .dotw  = 4,
        .hour  = 11,
        .min   = 30,
        .sec   = 24
    };
        datetime_t t_alarm = {
        .year  = 2024,
        .month = 04,
        .day   = 18,
        .dotw  = 4,
        .hour  = 11,
        .min   = 30,
        .sec   = 35
    };
    rtc_init();
    rtc_set_datetime(&t);
    rtc_set_alarm(&t_alarm, say_two);

    printf("Step 2\n");

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_init(BTN_PIN);
    gpio_set_dir(BTN_PIN, GPIO_IN);
    int i=0;
    int j=0;

    while (true) {
        gpio_put(LED_PIN, i/(PERIOD/2) ^ gpio_get(BTN_PIN));
        i++;
        if (i == PERIOD){
            i=0;
            printf("Loop %d\n",j);
            j++;
            say_one();
        }
        sleep_ms(100);   
        
    }
}