# Phase 2: 3D Waypoint Navigation

Quadcopter navigates through full 3D waypoints using a PD controller — extended from Phase 1.

## What This Does

The quadcopter tracks waypoints in **full 3D space (X, Y, Z axes)** using independent PD
controllers per axis with gravity compensation on Z.

**Implementation:** Direct force application via PhysX Force API. Each axis is controlled
independently using F = ma, with a feedforward gravity compensation term on Z to counteract
the constant 9.81 m/s² downward pull.

**Physics Model:** Simplified point-mass model — forces are applied directly to the centre
of mass without modelling quadcopter attitude (roll/pitch/yaw) or rotor dynamics. This is
an intentional simplification suitable for waypoint logic and RL reward design.

**Status:** ✅ Working — Quadcopter navigates all 5 waypoints in 3D, cycling continuously

## How to Run

### Ubuntu / Linux

```bash
conda activate env_isaaclab
cd 02_waypoint_pd
python waypoint_simple.py
```

### Windows

```powershell
cd 02_waypoint_pd
& "C:\isaac-sim\isaac-sim-standalone-5.1.0-windows-x86_64\python.bat" waypoint_simple.py
```

## Waypoint Path (Full 3D Navigation)

```
1. [0.0, 0.0, 1.5]m  -> Start position
2. [2.0, 0.0, 1.5]m  -> Move right (+X)
3. [2.0, 2.0, 2.0]m  -> Move forward + up (+Y +Z)
4. [0.0, 2.0, 2.0]m  -> Move left (-X)
5. [0.0, 0.0, 1.5]m  -> Return to start (-Y -Z)
```

The quadcopter cycles through all 5 waypoints continuously.

## Key Differences from Phase 1

| Feature | Phase 1 | Phase 2 |
|---------|---------|---------|
| Target | Fixed height (1.5m) | 3D waypoints |
| Axes controlled | Z only | X, Y, Z |
| Task | Hover in place | Navigate 3D path |
| Gravity compensation | Z feedforward | Z feedforward |
| Force output | Scalar thrust | 3D force vector |
| Controller | PD (Kp=10, Kd=5) | Same PD gains, per axis |

## Controller Parameters

- **Kp:** 10.0 (Position gain — same for all axes)
- **Kd:** 5.0 (Velocity gain — same for all axes)
- **Mass:** 1.0 kg
- **Max Force:** 60.0 N per axis (symmetric ±)
- **Waypoint Radius:** 0.3m (considered "reached" within this distance)

## How It Works

### PD Controller Logic (3D)

```
For each axis (X, Y, Z):
    error = target_position - current_position
    F     = mass * (Kp * error - Kd * velocity)

Gravity compensation (Z only):
    Fz   += mass * 9.81

Clamp all axes:
    F     = clip(F, -max_force, +max_force)
```

**Why the same PD formula works on all axes:**
Newton's second law (F = ma) is identical per axis — X, Y, Z dynamics are fully
decoupled. The same Kp/Kd values work because the plant (mass) is the same on every axis.

**Why gravity compensation on Z only:**
Gravity vector = [0, 0, -9.81] m/s². It has zero X and Y components — only Z needs
a feedforward term to cancel the constant downward pull.

### Force Application (PhysX)

```python
# 3D force vector applied directly to centre of mass
force_api.GetForceAttr().Set(Gf.Vec3f(float(force[0]),
                                       float(force[1]),
                                       float(force[2])))
force_api.GetWorldFrameEnabledAttr().Set(True)
```

### Code Structure

```
waypoint_simple.py
├── WaypointQuadcopter
│   ├── __init__()               <- Setup waypoints & controller
│   ├── _create_quadcopter()     <- Create rigid body (same as Phase 1)
│   ├── get_current_target()     <- Get current waypoint position
│   ├── check_waypoint_reached() <- Distance check & sequencing
│   ├── compute_control()        <- 3D PD controller -> force vector
│   └── apply_control()          <- Apply 3D force via PhysX API
└── main()                       <- Simulation loop
```

## Physics Model: Simplifications

This implementation uses a **direct force model** — a deliberate simplification of real
quadcopter physics:

| | Real Quadcopter | This Model |
|---|---|---|
| X/Y force | Via body tilt (attitude change) | Applied directly |
| Attitude dynamics | Roll, pitch, yaw | Not modelled |
| Controller structure | Cascaded (position -> attitude -> rotors) | Single PD loop |
| Rotor dynamics | 4 independent motors | Not modelled |

**Why this simplification is acceptable:** The goal of Phase 2 is to verify waypoint
sequencing logic and PD stability before introducing RL. Real attitude dynamics will be
relevant in Phase 3 when the RL agent learns its own control policy.

## Expected Terminal Output

```
[  100] Position: [ 0.05,  0.01,  1.48]m | Target: [ 0.00,  0.00,  1.50]m | Distance:  0.05m
Waypoint 1 reached!
Next waypoint: [2.0, 0.0, 1.5]m
[ 1100] Position: [ 0.96, -0.00,  1.50]m | Target: [ 2.00,  0.00,  1.50]m | Distance:  1.04m
Waypoint 2 reached!
Next waypoint: [2.0, 2.0, 2.0]m
[ 1200] Position: [ 1.12,  1.99,  2.00]m | Target: [ 0.00,  2.00,  2.00]m | Distance:  1.12m
Waypoint 3 reached!
Next waypoint: [0.0, 2.0, 2.0]m
```

## Current Results

**As of April 2026 (Ubuntu 24.04, Isaac Sim 5.1.0):**
- ✅ Quadcopter navigates all 5 waypoints in full 3D
- ✅ X, Y, Z axes independently controlled
- ✅ Gravity compensation stable
- ✅ Waypoint sequencing and cycling working
- ✅ Force application confirmed via PhysX Force API

## Customization

### Change Waypoints

Edit the `waypoints` list in `main()`:

```python
waypoints = [
    [0.0, 0.0, 2.0],
    [3.0, 0.0, 2.0],
    [3.0, 3.0, 3.0],
]
```

### Tune PD Controller

```python
self.kp = 12.0  # Faster response (may overshoot)
self.kd = 6.0   # More damping (reduces oscillation)
```

### Adjust Waypoint Detection Radius

```python
self.waypoint_radius = 0.5  # Larger = easier to reach
```

## Troubleshooting

### Quadcopter oscillates at waypoint
- Decrease Kp (try 8.0) or increase Kd (try 7.0)

### Quadcopter overshoots badly
- Increase Kd or decrease Kp

### Quadcopter drifts without reaching waypoint
- Decrease waypoint_radius or increase Kp

## Dependencies

- Isaac Sim 5.1.0
- Python 3.11 (conda env_isaaclab)
- NumPy (included in env_isaaclab)

---

**Status:** ✅ Working  
**Framework:** Isaac Sim standalone (no Isaac Lab)  
**Tested:** April 2026 — Ubuntu 24.04, Isaac Sim 5.1.0, RTX 5070  
**Next Phase:** → [Phase 3: RL Hover Training](../03_rl_hover/)
