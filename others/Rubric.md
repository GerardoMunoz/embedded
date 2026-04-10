#  Final Project Evaluation Guide

## Final Grade Distribution



---

# 1. RPi Pico Coding (30%)

Each subsystem is evaluated using the same criteria:

* Encapsulation (OOP design)
* PubSub communication (topics) ⭐
* Code quality
* Documentation
* Testing

## 📊 Evaluation Matrix

| Block ↓ / Criteria → | Encapsulation (10%) | PubSub (10%) | Quality (4%) | Docs (3%) | Testing (3%) | Total |
| -------------------- | ----------------- | ---------- | ----------- | -------- | ----------- | ----- |
|  Car               |                   |            |             |          |             |    |
|  Arm               |                   |            |             |          |             |    |
|  Display battery level          |                   |            |             |          |             |    |
|  Camera          |                   |            |             |          |             |    |
|  Distance          |                   |            |             |          |             |   |
|  Communication     |                   |            |             |          |             |    |
|  Scheduling        |                   |            |             |          |             |    |
|  PubSub Core       |                   |            |             |          |             |     |



---

# 2. Frontend (30%)

The interface must use a **class-based structure + PubSub architecture** and reflect the robot state.

## 📊 Evaluation

| Component       | Weight | Description                      |
| --------------- | ------ | -------------------------------- |
|  Camera View  | 5%     | Displays camera and RoI  |
|  Virtual Arm  | 5%     | Reflects real arm movement       |
|  Virtual Car  | 5%     | Reflects robot position          |
|  Controls     | 5%     | Sends commands via topics        |
|  Robot Info   | 5%     | Displays sensor data             |
|  Log Messages | 5%     | Shows system messages via PubSub |

---

#  3. Functional Performance (40%)

##📊 Tasks

| Task               | Weight | Description                     |
| ------------------ | ------ | ------------------------------- |
|  Go to Cardboard | 10%     | Robot approaches using camera   |
|  Hold Cardboard  | 10%     | Robot successfully grips object |
|  Move Cardboard  | 20%     | Robot moves object to target    |

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
