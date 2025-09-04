# Sampling Period Calculation for an RC Circuit with the Raspberry Pi Pico

## 1. Capacitor Charging Model
The voltage across a capacitor when charging through a resistor from a voltage source is:

$V_C(t) = V_{in}(1 - e^{-t/RC})$

where:  
- **R** – resistance in ohms  
- **C** – capacitance in farads  
- **τ = RC** – time constant of the circuit in seconds  

After a time of **5τ**, the capacitor is charged to about **99.3%** of $V_{in}$.

Therefore, the interesting interval to sample is up to about **5τ**.

---

## 2. Sampling Requirement
To properly reconstruct an exponential signal, we typically aim for **10–20 samples per time constant** τ.

- Recommended number of samples:  
  $N \approx 10 \; \text{to} \; 20 \; \text{samples per} \; τ$

- Sampling period:  
  $T_s = \frac{τ}{N}$

- Sampling frequency:  
  $f_s = \frac{1}{T_s} = \frac{N}{τ}$

---

## 3. Raspberry Pi Pico ADC
- Maximum theoretical sampling frequency:  
  $f_s = 500{,}000 \;\text{samples/s}$

- Minimum theoretical sampling period:  
  $T_s = \frac{1}{f_s} = \frac{1}{500{,}000} = 2 \; \mu s$

In practice (due to latency, buffers, etc.), even if the hardware supports 500 ksps, a more stable working rate is usually lower (e.g., 100–400 ksps).

If we want about **20 samples per τ**:
$T_s = \frac{τ}{20} \;\Rightarrow\; τ = 20 T_s$

With $T_s = 2 \; \mu s$, the ideal time constant to sample would be:
$τ \approx 20 \times 2 \; \mu s = 40 \; \mu s$

---

## 4. Notes about the Raspberry Pi Pico
- The Pico’s ADC works up to **500 ksps (500,000 samples/s)** theoretically.  
- In **MicroPython** or **C**, your practical limit will be much lower (a few kHz).  
- Using **DMA** you can approach the theoretical maximum.

---

## 5. Exercise
Capture, at the highest sampling rate available, the interval of **5τ** with **20 samples per τ**. Compare the collected data against a digital oscilloscope trace.
