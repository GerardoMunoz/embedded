
# Embedded Systems Class — Energy System Design Case Study
## Differential Robot Battery & Power Architecture

---

# 1. Class Objective

Design the complete energy system of a differential mobile robot considering:

- Component current consumption
- Required autonomy
- Battery selection
- Voltage regulation
- Charging methods
- Safety and protection
- Power distribution architecture

---

# 2. Case Study Description

System:

- Raspberry Pi Pico 2W (Wi‑Fi, MicroPython)
- 3 × SG90 Servos
- 2 × TT Gear Motors
- 0.96” OLED Display
- OV7670 Camera
- HC‑SR04 Ultrasonic Sensor

Goal:

- Precision movement (not high speed)
- Educational mobile robot
- Portable energy system

---



# 3. Step 1 — Current Consumption Calculation

| Device | Typical Current | Peak Current |
|--------|-----------------|--------------|
| Pico 2W (Wi‑Fi) | 120 mA | 300 mA |
| 3 × SG90 Servos | 750 mA | 2.4 A |
| 2 × Gear Motors | 600 mA | 2.0 A |
| OLED | 25 mA | 40 mA |
| OV7670 | 80 mA | 100 mA |
| Ultrasonic | 15 mA | 30 mA |

**Average total ≈ 1.6 A**  
**Peak total ≈ 4.5–5 A**

Design must consider peaks.

---

# 4. Step 2 — Desired Autonomy

Example target:

- 3 hours operation

Battery capacity formula:

Wh = V × Ah

Runtime:

t = Capacity (mAh) / Current (mA)

Example:

5000 mAh / 1600 mA ≈ 3.1 h

---

# 5. Step 3 — Battery Options Comparison

| Battery | Pros | Cons |
|--------|------|------|
| Li‑ion 18650 | High capacity | Needs BMS |
| LiPo | Light, compact | Fire risk |
| NiMH | Safe | Heavy |
| Lead‑acid | Cheap | Very heavy |
| Power Bank | Protected, USB | Limited current |

Conclusion for this robot:

**Power Bank is practical**:

- Integrated protection
- Regulated 5 V
- Easy recharge
- Safe for classroom use

---

# 6. Step 4 — Voltage Regulation

Different blocks need different voltages:

| Block | Voltage |
|-------|----------|
| Pico + Sensors | 5 V / 3.3 V |
| Servos | 5–6 V |
| Motors | 6–9 V |

Solution:

- DC‑DC Buck Converters
- Separate rails for motors and logic

---

# 7. Step 5 — Charging & Battery Management

Topics:

- CC/CV charging (Li‑ion)
- TP4056 modules
- Protection circuits
- Cell balancing (series packs)

Optional charging sources:

- Solar panels
- Dock charging
- USB charging

---

# 8. Power Distribution Architecture (Power Tree)

Example:

Battery / Power Bank
        │
        ├── 5V → Pico + OLED + Camera
        │
        ├── Buck 6V → Servos
        │
        └── Buck 7–9V → Motors

Key rules:

- Common GND
- Separate noisy loads
- Add bulk capacitors

---

# 9. Peak vs Average Current

Why peaks matter:

- Motor startup
- Servo stall
- Wi‑Fi transmission

Design margin:

Regulator current ≥ 1.5× peak expected load

---

# 10. Design Trade‑Off Discussion

Questions for students:

- Precision vs speed → energy impact?
- Weight vs autonomy?
- Safety vs energy density?
- Cost vs performance?

---

# 11. Key Engineering Takeaways

- Energy is a system‑level design problem
- Average current is not enough
- Regulation architecture matters
- Protection & safety are mandatory
- Practical solutions (power banks) are often optimal

---

# 12. Suggested Lab Extensions

- Measure servo current
- Compare buck vs linear regulators
- Estimate robot autonomy
- Test resets under peak load

---

End of Class Content


```
PowerBank 5V
     │
     ├── Pico 2W + Sensors
     └── Motor Driver → Motors
```