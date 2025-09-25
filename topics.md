# MQTT Topics Specification for Differential Drive Robot with Arm

This document defines the MQTT topics and the expected JSON payloads to control the robot.

## 1. Immediate State

### Topic:

`UDFJC/emb1/robot0/RPi/state`


### Description:
Applies an immediate state to the robot, setting linear/angular velocities and arm joint angles for a given duration.

### Expected JSON payload:

```json
{
  "v": 0.2,        // linear velocity [dm/s]
  "w": 0.0,        // angular velocity [°/s]
  "alfa0": 0,      // joint 0 angle [°]
  "alfa1": 45,     // joint 1 angle [°]
  "alfa2": 30,     // joint 2 angle [°]
  "duration": 2.0  // time in seconds to maintain this state
}
```

### Notes:

All fields are required except duration (default = 1.0 s).

The robot executes this state immediately when received.

## 2. Sequence Management

### Topic base:

`UDFJC/emb1/robot0/RPi/sequence`

### Description:

Manage the sequences

### Expected JSON payload:

```json
// Create a sequence
{
  "action": "create",
  "sequence": {
    "name": "saludo",
    "states": [
        { "v": 10, "w": 0, "alfa0": 0, "alfa1": 0, "alfa2": 0, "duration": 1.0 },
        { "v": 15.7, "w": 90, "alfa0": 0, "alfa1": 0, "alfa2": 0, "duration": 1.0 },
        { "v": 0, "w": 0, "alfa0": -90, "alfa1": 0, "alfa2": 0, "duration": 1.0 },
        { "v": 0, "w": 0, "alfa0": 90, "alfa1": 0, "alfa2": 0, "duration": 2.0 },
        { "v": 0, "w": 0, "alfa0": 0, "alfa1": 90, "alfa2": 0, "duration": 1.0 },
        { "v": 0, "w": 0, "alfa0": 0, "alfa1": 0, "alfa2": 90, "duration": 1.0 }
     ]
  }
}

// Delete a sequence
{
  "action": "delete",
  "name": "saludo"
}

// Add an state in a sequence
{
  "action": "add_state",
  "name": "saludo",
  "state": { "v": 0, "w": 0, "alfa0": 0, "alfa1": 45, "alfa2": 0, "duration": 1.5 }
}

// Execute a sequience immediately
{
  "action": "execute_now",
  "name": "saludo"
}

// Program the excution
{
  "action": "schedule",
  "name": "saludo",
  "time": "2025-09-25T20:00:00Z"
}
```
## 3. Bezier curve

### Topic base:

`UDFJC/emb1/robot0/RPi/bezier`

To be defined