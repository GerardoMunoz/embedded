#  Final Project Evaluation Guide

## Final Grade Distribution

| Category                             | Weight |
| ------------------------------------ | ------ |
|  RPi Pico Coding (OOP + PubSub)    | 49%    |
|  Frontend + Functional Performance | 51%    |

---

# 1. RPi Pico Coding (49%)

Each subsystem is evaluated using the same criteria:

* Encapsulation (OOP design)
* PubSub communication (topics) ⭐
* Code quality
* Documentation
* Testing

## 📊 Evaluation Matrix

| Block ↓ / Criteria → | Encapsulation (2) | PubSub (2) | Quality (1) | Docs (1) | Testing (1) | Total |
| -------------------- | ----------------- | ---------- | ----------- | -------- | ----------- | ----- |
|  Car               |                   |            |             |          |             | /7    |
|  Arm               |                   |            |             |          |             | /7    |
|  Display battery level          |                   |            |             |          |             | /7    |
|  Distance          |                   |            |             |          |             | /7    |
|  Communication     |                   |            |             |          |             | /7    |
|  Scheduling        |                   |            |             |          |             | /7    |
|  PubSub Core       |                   |            |             |          |             | /7    |

 Total: **49%**

---

# 2. Frontend (36%)

The interface must use a **class-based structure + PubSub architecture** and reflect the robot state.

## 📊 Evaluation

| Component       | Weight | Description                      |
| --------------- | ------ | -------------------------------- |
|  Camera View  | 6%     | Displays camera stream correctly |
|  Virtual Arm  | 6%     | Reflects real arm movement       |
|  Virtual Car  | 6%     | Reflects robot position          |
|  Controls     | 6%     | Sends commands via topics        |
|  Robot Info   | 6%     | Displays sensor data             |
|  Log Messages | 6%     | Shows system messages via PubSub |

---

#  3. Functional Performance (15%)

##📊 Tasks

| Task               | Weight | Description                     |
| ------------------ | ------ | ------------------------------- |
|  Go to Cardboard | 5%     | Robot approaches using camera   |
|  Hold Cardboard  | 5%     | Robot successfully grips object |
|  Move Cardboard  | 5%     | Robot moves object to target    |

---

#  SYSTEM REQUIREMENTS

Your system must demonstrate:

##  OOP Design

* Each hardware element is a class

##  PubSub Architecture

* Internal (robot)
* External (broker)
* Frontend (UI)

##  Topic Consistency

Same topic structure across:

* Robot
* Broker
* Frontend

---

#  IMPORTANT RULES

* The running code must match the submitted code
* Systems must be understandable and modular
* All team members must understand their system

---

#  What We Are Evaluating

This project is not only about making a robot work.

We are evaluating your ability to design:

* A modular embedded system
* A distributed communication architecture
* A digital twin with real-time synchronization

---

#  Summary

To succeed:

* Think in **systems**, not scripts
* Use **PubSub for everything**
* Keep your design **clean and modular**
* Ensure your frontend and robot speak the same language (topics)

---
