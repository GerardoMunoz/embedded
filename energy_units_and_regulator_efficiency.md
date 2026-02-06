# Units of Energy, Battery Capacity, and Regulator Efficiency

## 1. Units of Energy

Energy represents the capacity to perform work. In electrical and electronic systems, the most common unit of energy is the **Watt-hour (Wh)**.

### Watt (W)
A Watt is a unit of power:

Power (W) = Voltage (V) × Current (A)

### Watt-hour (Wh)
A Watt-hour is a unit of energy:

Energy (Wh) = Power (W) × Time (h)

Example:

If a system consumes 10 W for 2 hours:

Energy = 10 W × 2 h = 20 Wh

This unit is very useful when comparing batteries because it includes both voltage and current.

---

## 2. Ampere-hour (Ah) as Energy Measure

Another common way to express battery capacity is **Ampere-hour (Ah)**.

Capacity (Ah) = Current (A) × Time (h)

Example:

A 2 Ah battery can theoretically deliver:

- 2 A for 1 hour, or  
- 1 A for 2 hours

However, **Ah alone does not represent energy** unless voltage is considered.

To convert Ah to Wh:

Energy (Wh) = Voltage (V) × Capacity (Ah)

Example:

3.7 V × 2 Ah = 7.4 Wh

---

## 3. Important: Ah Assumes Constant Voltage

The Ah rating assumes the battery voltage remains constant.

But in real batteries:

- Voltage changes during discharge
- Lithium batteries drop from ~4.2 V to ~3.0 V
- Alkaline batteries also decrease gradually

Therefore:

- Ah is an approximation
- Wh is more accurate for energy comparisons

---

## 4. Energy Conversion and Heat Loss

Not all stored energy reaches the load.

Part of the energy converts into **heat**, reducing system efficiency.

This happens mainly in **voltage regulators**.

---

## 5. Linear Regulators (7805, LM317)

Linear regulators reduce voltage by dissipating excess energy as heat.

Example:

Input: 12 V  
Output: 5 V  
Load current: 1 A

Power in:

P_in = 12 V × 1 A = 12 W

Power out:

P_out = 5 V × 1 A = 5 W

Power lost as heat:

P_loss = 12 W − 5 W = 7 W

Efficiency:

η = P_out / P_in ≈ 42%

So more than half the energy becomes heat.

### Consequences

- Heat sinks required
- Reduced battery life
- Lower autonomy

---

## 6. Switching Regulators (DC‑DC Converters)

Switching regulators (Buck, Boost, Buck‑Boost) are much more efficient.

Typical efficiencies:

- 80% – 95%

Instead of burning excess voltage as heat, they convert energy using inductors and switching circuits.

### Example (90% efficiency)

If the load needs 5 W:

P_in = 5 W / 0.9 ≈ 5.56 W

Energy loss is only 0.56 W, far less than linear regulators.

---

## 7. Current Differences in DC‑DC Conversion

In DC‑DC converters, **power is approximately conserved**:

P_in ≈ P_out

So if voltage changes, current also changes.

### Buck Converter Example

Input: 12 V  
Output: 5 V  
Load current: 1 A

Output power:

P_out = 5 V × 1 A = 5 W

Input current:

I_in = P_out / V_in ≈ 0.42 A

So:

- Output current ≠ Input current
- Higher voltage → Lower current
- Lower voltage → Higher current

This is critical when sizing batteries and wires.

---

## 8. Why Correct Current Calculation Matters

Battery capacity (Ah) relates to **input current**, not output current.

If you ignore converter efficiency and voltage differences:

- Autonomy calculations will be wrong
- Battery may be undersized
- Regulators may overheat

Always calculate from **power**, not just current.

---

## 9. Summary

- Energy is best measured in **Watt-hours (Wh)**
- Ampere-hours (Ah) require voltage to represent energy
- Battery voltage changes during discharge
- Linear regulators waste energy as heat
- Switching regulators are far more efficient
- DC‑DC converters change current when changing voltage
- Correct power calculations are essential for battery design

---

This knowledge is fundamental when designing robotic, embedded, and battery‑powered systems.
