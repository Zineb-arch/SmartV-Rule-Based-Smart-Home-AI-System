# 🏠 SmartV: Rule-Based Smart Home AI System

A rule-based intelligent system that automates home devices using forward chaining reasoning.  
The system monitors environmental conditions (temperature, light, air quality, occupancy) and applies logical rules to control devices such as lights, heaters, fans, and windows.

---

##  Overview

SmartV simulates an intelligent home environment where decisions are made automatically based on predefined rules.  
It demonstrates how Artificial Intelligence can be applied using **symbolic reasoning** rather than machine learning.

The system continuously evaluates conditions and applies rules until a stable state (fixpoint) is reached.

---

##  Key AI Concepts

- Rule-Based Systems
- Knowledge Representation
- Forward Chaining Inference
- Conflict Resolution (Priority-based)
- State Transition Systems
- Fixpoint Computation

---

##  Features

- Multi-room smart home simulation
- Rule-based decision making
- Priority-based conflict resolution
- Automatic device control:
  - Lights
  - Heater
  - Fan
  - Windows
- Environmental awareness:
  - Temperature
  - Light level
  - Air quality
  - Occupancy
  - Sleep state
- Fixpoint reasoning (runs until no more rules apply)
- Step-by-step simulation over time

---

##  System Architecture

### 1. Knowledge Base
Stores:
- Room states (temperature, light, air quality, etc.)
- Device states (on/off, open/closed)

### 2. Rule System
Rules are defined using:
- Conditions (IF)
- Actions (THEN)
- Priority levels

Example:
```python
("room", "temperature", "<", 20)
→ turn heater ON
