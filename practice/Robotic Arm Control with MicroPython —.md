# Robotic Arm Control with MicroPython — Student Questionnaire

## Instructions

Answer the following questions based on the robotic arm project developed in class. Provide explanations, diagrams, pseudocode, or calculations where required. Do **not** include full program listings unless explicitly requested.

---

# Section 1 — Servo Fundamentals


1. What PWM frequency is typically used for standard servos? Why?
3. Explain the relationship between:

   * Pulse width
   * Duty cycle
   * Servo angle
4. If a servo operates between 500 µs and 2500 µs, what pulse width would correspond to 90°?
5. Why is calibration necessary for different servos?
6. Describe at least two factors that can cause servo jitter.
7. What is the purpose of defining minimum and maximum angle limits in software?

---

# Section 2 — MicroPython Servo Class Design

7. What attributes should a Servo class store internally? List at least four.
9. Why is it useful to separate:

   * Angle commands
   * Duty cycle output
10. Propose method names for:

    * Writing an angle
    * Writing a duty cycle directly
    * Setting angle limits
11. What is the purpose of an offset parameter?
12. How would you prevent commanding an angle outside safe limits?
13. Explain the benefit of encapsulation in the Servo class.

---

# Section 3 — Smooth Motion

13. Why is instantaneous motion undesirable in robotic arms?
15. Define motion interpolation.
16. What parameters are required to move a servo smoothly?
17. How does increasing the number of interpolation steps affect motion?
18. What is the trade‑off between smoothness and CPU usage?
19. Describe the difference between:

    * Time‑based motion
    * Speed‑based motion
20. What types of easing or motion profiles could improve smoothness beyond linear interpolation?

---

# Section 4 — Arm Class Architecture

20. What is the responsibility of the Arm class compared to the Servo class?
22. Why is it useful to group servos into a single Arm object?
23. Propose attributes the Arm class should contain.
24. Suggest method names for:

    * Setting joint angles
    * Moving to a Cartesian position
    * Homing the arm
25. What is joint space control?
26. What is task space control?
27. When would you use each?

---

# Section 5 — Angle Limits and Constraints

27. Explain the difference between:

    * Independent joint limits
    * Coupled joint limits
29. Why can the elbow limit depend on the shoulder angle?
30. Describe a real mechanical situation where link collision occurs.
31. How could you experimentally determine coupled limits?
32. What should happen if an invalid tuple of angles is commanded?
33. Compare:

    * Rejecting invalid commands
    * Clamping them automatically

---

# Section 6 — Kinematics

33. Define forward kinematics.
35. What information does forward kinematics compute?
36. Define inverse kinematics.
37. Why can inverse kinematics have multiple solutions?
38. What does it mean for a point to be unreachable?
39. How do link lengths affect the workspace?
40. Provide the law of cosines formula used in planar IK.

---

# Section 7 — Timer Interrupts (RP2350 / MicroPython)

40. What is an interrupt?
42. How does a timer interrupt differ from using `sleep()`?
43. List three advantages of timer‑based motion control.
44. Why should timer callbacks execute quickly?
45. Give examples of operations that should be avoided inside interrupts.
46. What is deterministic timing?
47. How does timer frequency affect motion smoothness?

---

# Section 8 — Real‑Time Motion Architecture

47. Why is it better to use one global timer instead of one timer per servo?
49. What internal variables are needed for timer‑driven smoothing?
50. Explain the concept of incremental position updates.
51. How can multiple servos finish motion simultaneously?
52. What is motion synchronization?

---

