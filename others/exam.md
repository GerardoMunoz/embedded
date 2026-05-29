#  Final Project – Embedded Systems

##  Project Description

In this final project, you will design and implement an **autonomous robotic system** using:

* A differential drive robot
* A robotic arm (MeArm)
* A camera (OV7670)
* Sensors and actuators
* A distributed communication architecture (PubSub + Broker)
* A web-based interface with visualization (Digital Twin)

---

##  Evaluation Distribution

The final grade will be distributed as follows:

1. **25% – Challenge: Autonomous Cardboard Handling**
2. **5% – Presentation**
3. **5% – GitHub Repository**

---

##  1. Challenge: Autonomous Cardboard Handling

Your robot must autonomously complete the following tasks:

* **5%** Position itself in front of the cardboard tray
* **5%** Place the fork underneath the tray
* **5%** Lift the tray
* **5%** Place the tray inside a rectangular area located 10 cm to the right of the original position
* **5%** **Completion Time Performance**

---

###  Completion Time Performance (5%)

The final 5% will be assigned based on how fast each robot completes the full task autonomously.

* The **first team** to successfully complete the challenge receives **5.0**
* Each subsequent position will receive **0.2 less** than the previous one

#### Example:

* 1st place → 5.0
* 2nd place → 4.8
* 3rd place → 4.6
* 4th place → 4.4
* …

---

### ⚠️ Important Rules

* The task must be completed **fully autonomously** (no manual intervention)
* Only **successful completions** are ranked
* If a robot fails the task, it does not receive time-based points
* In case of a tie, teams will receive the same score

---

---

## 2. GitHub Repository

You must submit a repository on GitHub containing:

* All source code (robot + frontend)
* A clear project structure
* A README file including:

  * System description
  * Architecture diagram
  * Topic structure (PubSub)
  * Instructions to run the project

---

## 3. Final Presentation (in English)

There will be **one global presentation for the entire class**.

### Presentation Format:

* The system must be presented as a **single integrated project**
* Each student is responsible for explaining a specific part
  *(Please select one topic from the list and write your choice in the class WhatsApp chat)*

---

### Video Submission

Each student must record a **video of their assigned topic**:

* Minimum duration: **1 minute**
* The video must be uploaded to a **cloud platform** (e.g., Google Drive)
* Submit the **video link** using the provided form


---
# List of Topics

## A. Global Overview

1. **Project Introduction**

   * Problem, objectives, and system overview

2. **System Architecture**

   * High-level diagram (robot + frontend + broker)

---

## B. Robot (Embedded System)

3. **Differential Drive System (Car)**

   * Motors, encoders, movement logic

4. **Motor Control Algorithms**

   * Speed control, direction, basic navigation

5. **Robotic Arm (MeArm)**

   * Servos, basic kinematics, movement sequences

6. **Gripping Mechanism (Fork System)**

   * Strategy to pick up the cardboard

7. **Ultrasonic Distance Sensor**

   * Distance measurement and usage

8. **Camera System (OV7670)**

   * Data acquisition and limitations

9. **Vision Processing Strategy**

   * How the robot detects the egg carton

10. **ROI and Detection Logic**

* Region of Interest and decision-making

---

## C. Software Architecture (CORE PART)

11. **OOP Design in MicroPython**

* Class structure and responsibilities

12. **Internal PubSub System**

* MessageBus design and topic usage

13. **Scheduling and Concurrency**

* Loops, timing, and threads

14. **Communication with Broker**

* TCP/WebSocket implementation

---

## D. Frontend & Digital Twin

15. **Frontend Architecture (JavaScript + PubSub)**

* Class structure and communication

16. **Robot Control Interface**

* Manual control and command system

17. **Camera Visualization**

* Display and debugging features (ROI, overlays)

18. **Digital Twin – Car**

* Visualization of robot movement

19. **Digital Twin – Arm**

* Visualization of arm motion

20. **Logs and System Monitoring**

* Debug messages, topics, and system insight

---

##  Topic Selection

Please write in the WhatsApp chat the number (**1 to 20**) of the topic you choose.

Each student must present a **different topic**.







---

###  Video Submission

Each student must record a **video of their assigned topic**:

* Minimum duration: **1 minute**
* The video must be uploaded to a **cloud platform** (e.g., Google Drive)
* Submit the **video link** using the provided form

📅 **Deadline:** June 3
You must submit:

* Video link
* GitHub repository link

---

###  Robot Challenge Evaluation

The evaluation of the robot challenge will take place on:

📅 **June 5**

---

