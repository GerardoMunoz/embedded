

# MicroPython Haks

## Types of Data

### Type Hints & Pydantic
Type hints improve readability and enable static analysis. Pydantic (if available) helps validate data.


```python
def add(a: int, b: int) -> int:
    return a + b
````

---

### bytearray

Mutable sequence of bytes (useful for buffers).

```python
buf = bytearray(10)
buf[0] = 255
```

---

### array.array

Efficient numeric arrays.

```python
import array

arr = array.array('I', [1, 2, 3])  # unsigned int
```

---

### Micropython con while

```python
from machine import Pin
import time

led_pin = Pin(0, Pin.OUT)   
button_pin = Pin(15, Pin.IN,Pin.PULL_UP)  

while True:
    button_state = button_pin.value()
    if button_state == 0:
        led_pin.toggle()  

```

---

## RP2 (Raspberry Pi Pico)

### SIO

Allows writing/reading GPIO by touching registers directly:

```python
import machine

# SIO base address (see RP2040 datasheet)
SIO_BASE = 0xD0000000
GPIO_OUT_SET = SIO_BASE + 0x014
GPIO_OUT_CLR = SIO_BASE + 0x018


i = 0
while True:
    machine.mem32[GPIO_OUT_SET] = i
    machine.mem32[GPIO_OUT_CLR] = ~i
    i = (i + 1) % 256
```

### PIO (rp2.StateMachine)

Programmable I/O for fast parallel or timed signals.
```python
import time
import rp2
from machine import Pin


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    jmp(pin, "one")    
    set(pins, 1)   [31]
    label("one")
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    set(pins, 0)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    wrap()

sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(0),jmp_pin=Pin(15))
sm.active(1)
```

```python
from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

@asm_pio(out_init=(PIO.OUT_LOW,) * 8, autopull=True, pull_thresh=8)
def prog():
    pull()
    out(pins, 8)

sm = StateMachine(0, prog, freq=1_000_000, out_base=Pin(0))
sm.active(1)

sm.put(0b10101010)
```

---

### DMA (concept)

DMA allows memory transfer without CPU (limited direct support in MicroPython).

* Typically configured via registers (advanced use)
* Not commonly used directly in MicroPython

---

## Program Flow

### Super Loop

Classic embedded structure.

```python
def setup():
    print("Init")

def loop():
    print("Running")

setup()
while True:
    loop()
```

---

### Multithreading (_thread)

Run tasks on second core.

```python
import _thread
import time

def task():
    while True:
        print("Core1")
        time.sleep(0.1)

_thread.start_new_thread(task, ())

while True:
    print("Core0")
    time.sleep(0.5)
```

###  Locks

```python
import _thread

lock = _thread.allocate_lock()
counter = 0

def safe_increment():
    global counter
    with lock:
        counter += 1
```


---

### Decorators for Speed

Compile functions to native code.

```python
import micropython

@micropython.native
def fast_add(a, b):
    return a + b


@micropython.viper
def toggle(pin: int):
    import machine
    machine.mem32[0xD0000014] = 1 << pin
```

---

### Interrupts


React to timer events.

```python
from machine import Pin,Timer

pin_led = Pin(0, mode=Pin.OUT)
pin_button = Pin(15, mode=Pin.IN, pull=Pin.PULL_UP)

def toggle_led(t:Timer):
    pin_led(not pin_led() and pin_button())

Timer().init(mode=Timer.PERIODIC, period= 500, callback=toggle_led
```

---

React to hardware events.

```python
from machine import Pin

def handler(pin):
    print("See the following example!") # Printing during an interrupt is not recommended.

btn = Pin(15, Pin.IN, Pin.PULL_DOWN)
btn.irq(trigger=Pin.IRQ_RISING, handler=handler)
```

#### micropython.schedule()

Safe way to defer work from interrupts.

```python
import micropython

def work(arg):
    print("Scheduled:", arg)

def irq_handler(pin):
    micropython.schedule(work, 123)
```

---

## Multithreading: Memory Problems & Solutions

### Problem

Race conditions when sharing variables.

---
### Pre-allocated ring buffer

Create a fixed-size buffer in advance, then write into it by index:

```python
BUFFER_SIZE = 32
ring = [None] * BUFFER_SIZE
head = 0

def irq_handler(pin):
    global head, ring
    ring[head] = pin.value()  # or some small integer/event code
    head = (head + 1) % BUFFER_SIZE
```

This uses no dynamic allocation, so it’s ISR-safe.

---

### Solution: Locks

```python
import _thread

lock = _thread.allocate_lock()
counter = 0

def safe_increment():
    global counter
    with lock:
        counter += 1
```

---

### Alternative: Avoid Sharing

Use message passing or queues instead of shared variables.

---

## Notes

* Use PIO for precise timing (MHz range)
* Use native/viper for speed-critical code
* Avoid heavy work inside interrupts
* Be careful with shared memory in threads


