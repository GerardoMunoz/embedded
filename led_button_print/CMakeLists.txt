cmake_minimum_required(VERSION 3.13)
set(PICO_BOARD pico_w)
include(pico_sdk_import.cmake)
project(led_button C CXX ASM)
pico_sdk_init()
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
add_executable(led_button led_button.c)
pico_add_extra_outputs(led_button)
target_link_libraries(
    led_button 
    pico_stdlib
    )
pico_enable_stdio_usb(led_button 1)
pico_enable_stdio_uart(led_button 0)