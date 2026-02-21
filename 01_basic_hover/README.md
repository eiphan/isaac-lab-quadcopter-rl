\# Phase 1: Basic Hover Control



Simple PD controller for quadcopter hovering at a target height.



\## What This Does



\- Quadcopter hovers at 1.5m using PD controller

\- Gravity compensation

\- Velocity damping for stability



\## How to Run

```powershell

conda deactivate

cd 01\_basic\_hover

\& "C:\\isaac-sim\\isaac-sim-standalone-5.1.0-windows-x86\_64\\python.bat" simple\_hover.py

```



\## Controller Parameters



\- \*\*Kp (Position):\*\* 10.0

\- \*\*Kd (Velocity):\*\* 5.0

\- \*\*Mass:\*\* 1.0 kg

\- \*\*Target Height:\*\* 1.5m



\## Results



\- Hovering accuracy: ±0.1m

\- Stable hovering achieved

\- No RL training required



\## Next Phase



→ \[Phase 2: Waypoint Navigation](../02\_waypoint\_pd/)

