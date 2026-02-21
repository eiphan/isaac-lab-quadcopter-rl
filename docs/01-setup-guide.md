# Setup Guide - Isaac Lab Quadcopter Project

Complete installation guide for Windows 11.

---

## ✅ Prerequisites Checklist

Before starting, ensure you have:

- [ ] Windows 11 (Home, Pro, or Education)
- [ ] NVIDIA GPU with 8GB+ VRAM
- [ ] 32GB RAM (16GB minimum)
- [ ] 50GB free disk space
- [ ] Git installed
- [ ] GitHub account created

---

## 📥 Installation Steps

### Step 1: Install Isaac Sim 5.1

1. Download from [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac-sim)
2. Install to: `C:\isaac-sim\isaac-sim-standalone-5.1.0-windows-x86_64`
3. Verify installation:
   ```powershell
   Test-Path "C:\isaac-sim\isaac-sim-standalone-5.1.0-windows-x86_64\python.bat"
   # Should return: True
   ```

### Step 2: Enable Long Paths (Windows 11)

Open PowerShell as **Administrator**:

```powershell
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1
```

Restart your computer after this step.

### Step 3: Install Isaac Lab

```powershell
# Clone Isaac Lab
cd C:\Users\YOUR_USERNAME\Documents
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab

# Create symlink (PowerShell as Administrator!)
New-Item -ItemType SymbolicLink -Name "_isaac_sim" -Target "C:\isaac-sim\isaac-sim-standalone-5.1.0-windows-x86_64"

# Install Isaac Lab (normal PowerShell)
& "C:\isaac-sim\isaac-sim-standalone-5.1.0-windows-x86_64\python.bat" -m pip install -e source\isaaclab

# Install RL libraries
& "C:\isaac-sim\isaac-sim-standalone-5.1.0-windows-x86_64\python.bat" -m pip install skrl
& "C:\isaac-sim\isaac-sim-standalone-5.1.0-windows-x86_64\python.bat" -m pip install git+https://github.com/leggedrobotics/rsl_rl.git
& "C:\isaac-sim\isaac-sim-standalone-5.1.0-windows-x86_64\python.bat" -m pip install -e source\isaaclab_tasks
```

### Step 4: Verify Installation

```powershell
& "C:\isaac-sim\isaac-sim-standalone-5.1.0-windows-x86_64\python.bat" -c "import isaaclab; print('Isaac Lab:', isaaclab.__version__)"
& "C:\isaac-sim\isaac-sim-standalone-5.1.0-windows-x86_64\python.bat" -c "import skrl; print('SKRL OK')"
```

Expected output:
```
Isaac Lab: 0.54.3
SKRL OK
```

### Step 5: Clone This Project

```powershell
cd C:\Users\YOUR_USERNAME\Documents\03_NUS\CEG5003\00_REPO
git clone https://github.com/YOUR_USERNAME/isaac-lab-quadcopter-rl.git
cd isaac-lab-quadcopter-rl
```

---

## 🎮 Quick Test

Run the basic hover example:

```powershell
conda deactivate  # Exit conda if active
cd 01_basic_hover
& "C:\isaac-sim\isaac-sim-standalone-5.1.0-windows-x86_64\python.bat" simple_hover.py
```

You should see Isaac Sim open with a hovering quadcopter!

---

## 🆘 Troubleshooting

### "Symlink creation failed"
- Must run PowerShell as Administrator
- Enable Developer Mode in Windows Settings

### "Module not found: isaaclab"
- Reinstall: `& "C:\isaac-sim\...\python.bat" -m pip install -e source\isaaclab`
- Check symlink exists: `Test-Path IsaacLab\_isaac_sim`

### "CUDA out of memory"
- Reduce number of environments in config
- Close other applications
- Restart computer

---

## 📚 Next Steps

After successful installation:

1. Read [PD Controller Theory](02-pd-controller.md)
2. Try Phase 1: Basic Hover
3. Move to Phase 2: Waypoint Navigation
4. Start RL Training (Phase 3)

---

**Installation Time:** ~30-60 minutes  
**Disk Space Used:** ~40GB
