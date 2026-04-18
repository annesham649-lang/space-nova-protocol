# Space Nova | Autonomous Collision Avoidance

### 🛡️ Executive Summary
Space Nova is an autonomous 'Executive' safety layer designed for high-latency orbital environments. 

### 🔍 Technical Core: Deterministic Maneuver Logic
The core mathematical logic for the autonomous decision-making loops is located in: [space_nova_mobile.py] (https://github.com/annesham649-lang/space-nova-protocol/blob/main/space_nova_mobile.py)

**Key Logic Overview:**
* **State Estimation:** Real-time processing of orbital TLE (Two-Line Element) data.
* **Collision Probability ($P_c$):** Calculated based on covariance scaling for high-risk conjunctions.
* **Deterministic Threshold:** If $P_c > 10^{-4}$, the autonomous safety loop executes a delta-V maneuver.
* **Hardware Target:** Optimized for NVIDIA Jetson Orin (Edge-AI inference).
---
## 🛰️ Operational Constraint Logic 

To ensure operational trust, Space Nova utilizes a **Tripartite Confidence Model**. This removes the "Black Box" element of AI decision-making by breaking trust into three verifiable layers:

1. **State Confidence:** Real-time trust in sensor telemetry and GPS positioning.
2. **Propagation Confidence:** Trust in the forward-physics model and orbital drift predictions.
3. **Decision Confidence:** The clarity of the safety margin for the proposed maneuver.

### Decision Matrix
| Mode | Confidence Threshold | System Action |
| :--- | :--- | :--- |
| **AUTONOMOUS** | > 90% | Real-time maneuver execution without delay. |
| **AUGMENTED** | 75% - 90% | Suggests maneuver; awaits Operator "GO" command. |
| **MANUAL** | < 75% | System inhabitation; full telemetry handover to Human-in-the-Loop. |
