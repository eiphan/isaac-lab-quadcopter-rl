"""
Phase 2: Quadcopter Waypoint Navigation (Simplified)
=====================================================
Based on Phase 1's working PD controller, now with waypoint tracking!

KEY CHANGES FROM PHASE 1:
- Multiple waypoints instead of fixed hover height
- Waypoint sequencing logic
- Progress tracking and visualization

SAME AS PHASE 1:
- PD controller (proven to work!)
- Same physics and quadcopter setup
- Simple, clean code
"""

from isaacsim import SimulationApp

# Launch Isaac Sim FIRST
simulation_app = SimulationApp({"headless": False})

# Now import other modules
import numpy as np
from omni.isaac.core import World
from omni.isaac.core.prims import RigidPrim
from pxr import UsdGeom, UsdPhysics, Gf, PhysxSchema


class WaypointQuadcopter:
    """
    Quadcopter that navigates through waypoints using PD controller.
    
    This extends Phase 1's hovering to follow a sequence of waypoints.
    """
    
    def __init__(self, world, waypoints, start_position=[0, 0, 1.5]):
        """
        Initialize quadcopter with waypoints.
        
        Args:
            world: Isaac Sim World object
            waypoints: List of [x, y, z] positions to visit
            start_position: Starting position
        """
        self.world = world
        self.waypoints = np.array(waypoints, dtype=np.float32)
        self.num_waypoints = len(waypoints)
        self.current_waypoint_idx = 0
        self.waypoint_radius = 0.3  # Consider waypoint reached within 0.3m
        
        # Quadcopter parameters (same as Phase 1!)
        self.mass = 1.0  # kg
        self.max_thrust = 60.0  # N (4 rotors × 15N each)
        
        # PD Controller gains (same as Phase 1!)
        self.kp = 10.0
        self.kd = 5.0
        
        # Create quadcopter
        self._create_quadcopter(start_position)
        
        print("=" * 70)
        print("🚁 PHASE 2: WAYPOINT NAVIGATION")
        print("=" * 70)
        print(f"✅ Waypoints: {self.num_waypoints}")
        print(f"✅ Controller: PD (Kp={self.kp}, Kd={self.kd})")
        print(f"✅ Mass: {self.mass}kg, Max thrust: {self.max_thrust}N")
        print()
        print("🎯 Waypoint Path:")
        for i, wp in enumerate(self.waypoints):
            print(f"   {i+1}. [{wp[0]:.1f}, {wp[1]:.1f}, {wp[2]:.1f}]m")
        print("=" * 70)
        print()
    
    def _create_quadcopter(self, position):
        """Create quadcopter rigid body (same as Phase 1)."""
        stage = self.world.stage
        
        # Create quadcopter prim
        quad_path = "/World/Quadcopter"
        quad_prim = stage.DefinePrim(quad_path, "Xform")
        
        # Add cube geometry
        cube = UsdGeom.Cube.Define(stage, f"{quad_path}/Geom")
        cube.GetSizeAttr().Set(0.2)
        cube.AddTranslateOp().Set(Gf.Vec3f(position[0], position[1], position[2]))
        
        # Set blue color
        cube.GetDisplayColorAttr().Set([Gf.Vec3f(0.2, 0.5, 1.0)])
        
        # Add physics
        UsdPhysics.RigidBodyAPI.Apply(quad_prim)
        UsdPhysics.CollisionAPI.Apply(cube.GetPrim())
        UsdPhysics.MassAPI.Apply(quad_prim).GetMassAttr().Set(self.mass)
        
        # Create RigidPrim
        self.quad = RigidPrim(prim_path=quad_path, name="quadcopter")
    
    def get_current_target(self):
        """Get current waypoint target."""
        return self.waypoints[self.current_waypoint_idx]
    
    def check_waypoint_reached(self, position):
        """
        Check if current waypoint is reached.
        
        Returns:
            bool: True if waypoint reached
        """
        target = self.get_current_target()
        distance = np.linalg.norm(position - target)
        
        if distance < self.waypoint_radius:
            print(f"✅ Waypoint {self.current_waypoint_idx + 1} reached!")
            
            # Move to next waypoint (wrap around)
            self.current_waypoint_idx = (self.current_waypoint_idx + 1) % self.num_waypoints
            
            next_target = self.get_current_target()
            print(f"🎯 Next waypoint: [{next_target[0]:.1f}, {next_target[1]:.1f}, {next_target[2]:.1f}]m")
            print()
            
            return True
        
        return False
    
    def compute_control(self, position, velocity):
        """
        PD controller to reach current waypoint.
        
        Same logic as Phase 1, but target is dynamic (current waypoint).
        
        Args:
            position: Current position [x, y, z]
            velocity: Current velocity [vx, vy, vz]
            
        Returns:
            float: Thrust force in Newtons
        """
        # Get current target waypoint
        target_position = self.get_current_target()
        
        # Position error
        error_position = target_position - position
        
        # PD control
        # P term: proportional to position error
        # D term: proportional to velocity (want velocity = 0 at target)
        control = self.kp * error_position - self.kd * velocity
        
        # Gravity compensation (9.81 m/s² downward)
        gravity_compensation = self.mass * 9.81
        
        # Total thrust (only Z component, simplified)
        thrust_z = self.mass * control[2] + gravity_compensation
        
        # Clamp thrust to valid range
        thrust = np.clip(thrust_z, 0, self.max_thrust)

        #Full 3D force vector - apply mass scaling to all axes
        force = self.mass * control

        #Gravity compensation only in Z (gravity has no effect in X/Y)
        force[2] += gravity_compensation

        # Clamp all axes independently (for simplicity, we only apply thrust in Z, but this shows how to extend to 3D control)
        force = np.clip(force, -self.max_thrust, self.max_thrust)
        
        return force
    
    def apply_control(self):
        """Apply PD control to reach current waypoint."""
        # Get current state
        position = np.array(self.quad.get_world_pose()[0])
        velocity = np.array(self.quad.get_linear_velocity())
        
        # Check if waypoint reached
        self.check_waypoint_reached(position)
        
        # Compute control
        force = self.compute_control(position, velocity)
        
        # Apply force directly using USD/PhysX
        from omni.isaac.core.utils.prims import get_prim_at_path
        from pxr import PhysxSchema
        
        prim = get_prim_at_path(self.quad.prim_path)
        
        # Use PhysX force API
        if not prim.HasAPI(PhysxSchema.PhysxForceAPI):
            PhysxSchema.PhysxForceAPI.Apply(prim)
        
        force_api = PhysxSchema.PhysxForceAPI(prim)

        #force_api.GetForceEnabledAttr().Set(True)
        #force_api.GetForceAttr().Set(Gf.Vec3f(0.0, 0.0, float(thrust)))
        #force_api.GetWorldFrameEnabledAttr().Set(True)
        
        force_api.GetForceEnabledAttr().Set(True)
        force_api.GetForceAttr().Set(Gf.Vec3f(float(force[0]), float(force[1]), float(force[2])))
        force_api.GetWorldFrameEnabledAttr().Set(True)

def main():
    """Run Phase 2: Waypoint Navigation."""
    
    # Create world
    world = World()
    world.scene.add_default_ground_plane()
    
    print("\n🌍 Creating simulation world...")
    
    # Define waypoints (same as Isaac Lab version planned)
    waypoints = [
        [0.0, 0.0, 1.5],    # Start
        [2.0, 0.0, 1.5],    # Right
        [2.0, 2.0, 2.0],    # Forward + Up
        [0.0, 2.0, 2.0],    # Left
        [0.0, 0.0, 1.5],    # Back to start
    ]
    
    # Create quadcopter
    quad = WaypointQuadcopter(world, waypoints=waypoints)
    
    # Reset world
    world.reset()
    
    print("🎮 Controls:")
    print("   - Watch the quadcopter navigate waypoints")
    print("   - Close window to exit")
    print()
    print("▶️  Starting simulation...\n")
    
    # Simulation loop
    step_count = 0
    
    while simulation_app.is_running():
        # Step world
        world.step(render=True)
        
        # Apply control every step
        if world.is_playing():
            quad.apply_control()
            step_count += 1
            
            # Print status every 100 steps (~1 second at 100Hz)
            if step_count % 100 == 0:
                pos = quad.quad.get_world_pose()[0]
                target = quad.get_current_target()
                distance = np.linalg.norm(np.array(pos) - target)
                print(f"[{step_count:5d}] Position: [{pos[0]:5.2f}, {pos[1]:5.2f}, {pos[2]:5.2f}]m | "
                      f"Target: [{target[0]:5.2f}, {target[1]:5.2f}, {target[2]:5.2f}]m | "
                      f"Distance: {distance:5.2f}m")
    
    simulation_app.close()
    print("\n✅ Phase 2 complete!")


if __name__ == "__main__":
    main()
