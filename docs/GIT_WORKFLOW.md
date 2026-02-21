# Git Workflow Guide

Step-by-step guide for version control throughout this project.

---

## 🎯 Git Strategy

We'll use **feature-based development** with clear commit messages showing your learning progression.

### Branch Strategy

```
main (stable, showcase-ready code)
├── phase1-pd-hover
├── phase2-pd-waypoint
├── phase3-rl-hover
└── phase4-rl-waypoint
```

---

## 📋 Initial Setup

### Step 1: Configure Git

```powershell
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify
git config --list
```

### Step 2: Initial Commit

```powershell
cd C:\Users\eiphan\Documents\03_NUS\CEG5003\00_REPO\isaac-lab-quadcopter-rl

# Check status
git status

# Add all files
git add .

# Commit with meaningful message
git commit -m "Initial commit: Project structure and documentation"

# Push to GitHub
git push origin main
```

---

## 🔄 Workflow for Each Phase

### Phase 1: Basic Hover (Example)

#### Step 1: Create Feature Branch

```powershell
# Create and switch to new branch
git checkout -b phase1-pd-hover

# Verify you're on the new branch
git branch
```

#### Step 2: Work on Code

```powershell
# Create files in 01_basic_hover/
# Write code, test, debug...

# Check what changed
git status
git diff
```

#### Step 3: Commit Your Work

```powershell
# Stage specific files
git add 01_basic_hover/simple_hover.py
git add 01_basic_hover/README.md

# Commit with descriptive message
git commit -m "feat: Implement basic PD hover controller

- Add quadcopter rigid body with physics
- Implement PD controller for vertical control
- Add gravity compensation
- Test: Successfully hovers at 1.5m ±0.05m
- Document: PD gains and tuning process"

# Push to GitHub
git push origin phase1-pd-hover
```

#### Step 4: Merge to Main (When Ready)

```powershell
# Switch back to main
git checkout main

# Merge your feature branch
git merge phase1-pd-hover

# Push to GitHub
git push origin main

# Delete feature branch (optional)
git branch -d phase1-pd-hover
git push origin --delete phase1-pd-hover
```

---

## 📝 Commit Message Guidelines

Use **Conventional Commits** format:

```
<type>: <subject>

<body>

<footer>
```

### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `refactor`: Code restructuring
- `test`: Adding tests
- `perf`: Performance improvement

### Examples:

**Good Commits:**
```bash
git commit -m "feat: Add waypoint navigation controller

- Implement waypoint sequencing logic
- Add PD control for position tracking
- Test with 5 waypoints in 30 seconds
- Results: 95% waypoint accuracy"
```

```bash
git commit -m "fix: Resolve quadcopter instability at low heights

- Increase derivative gain from 2.0 to 3.0
- Add minimum thrust threshold
- Prevents oscillations below 0.5m"
```

```bash
git commit -m "docs: Add PD controller mathematical derivation

- Explain position/velocity error calculation
- Document gain tuning methodology  
- Add comparison with LQR controller"
```

**Bad Commits:**
```bash
git commit -m "update"  # Too vague!
git commit -m "fixed stuff"  # What stuff?
git commit -m "asdfasdf"  # Not helpful!
```

---

## 🏷️ Using Tags for Milestones

Tag important milestones:

```powershell
# Tag when phase is complete
git tag -a v1.0-pd-hover -m "Phase 1 Complete: PD Hover Controller

- Stable hovering at 1.5m
- PD controller fully documented
- Ready for supervisor review"

# Push tags
git push origin v1.0-pd-hover

# List all tags
git tag
```

---

## 📊 Showcase Progress

### Create Release on GitHub

After each phase:

1. Go to your repo on GitHub
2. Click **"Releases"** → **"Create a new release"**
3. Choose your tag (e.g., `v1.0-pd-hover`)
4. Title: "Phase 1: PD Hover Controller"
5. Description:
   ```markdown
   ## Phase 1 Complete! ✅
   
   Implemented a PD controller for quadcopter hovering.
   
   ### Key Achievements:
   - Stable hover at 1.5m (±0.05m error)
   - Hand-tuned PD gains (Kp=1.5, Kd=2.0)
   - GPU-accelerated parallel simulation
   
   ### Demo:
   ![Hover Demo](path/to/screenshot.png)
   
   ### Next Steps:
   - Phase 2: Waypoint navigation
   ```

6. Attach demo video or screenshots
7. Publish release

---

## 🔍 Useful Git Commands

### Check Status

```powershell
git status              # What changed?
git log --oneline -10   # Last 10 commits
git diff                # Show changes
```

### Undo Changes

```powershell
# Undo uncommitted changes to a file
git checkout -- filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - CAREFUL!
git reset --hard HEAD~1
```

### View History

```powershell
# Beautiful commit history
git log --graph --oneline --all

# See who changed what
git blame filename.py

# See changes in a specific commit
git show COMMIT_HASH
```

---

## 📅 Recommended Commit Frequency

| Phase | Activity | Commit Frequency |
|-------|----------|-----------------|
| Development | Writing code | Every working feature |
| Debugging | Fixing bugs | After each fix |
| Documentation | Writing docs | After each section |
| Testing | Running experiments | After successful run |

**Rule of Thumb:** Commit when you can write a meaningful commit message!

---

## 🎓 Learning Git as You Go

### Week 1: Basic Commands
- `git status`, `git add`, `git commit`, `git push`

### Week 2: Branching
- `git branch`, `git checkout`, `git merge`

### Week 3: History
- `git log`, `git diff`, `git tag`

### Week 4: Advanced
- `git rebase`, `git cherry-pick`, `git stash`

---

## 💡 Pro Tips

1. **Commit often** - Small commits are better than large ones
2. **Write descriptive messages** - Your future self will thank you
3. **Use branches** - Experiment without fear
4. **Tag milestones** - Easy to find important versions
5. **Push daily** - GitHub is your backup!

---

## 📚 Resources

- [Git Book](https://git-scm.com/book/en/v2)
- [GitHub Docs](https://docs.github.com)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

**Remember:** Git is your project's time machine. Use it well! 🚀
