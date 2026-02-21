"""
Stable Flying Quadcopter for Isaac Sim 5.1
This version has proper control limits and won't fly to space!
"""
# flake8: noqa: E402
# Isaac Sim requires SimulationApp to be imported first

from isaacsim import SimulationApp

# Launch Isaac Sim
simulation_app = SimulationApp({"headless": False})

import numpy as np
from omni.isaac.core import World
from omni.isaac.core.prims import RigidPrim
from pxr import UsdGeom, UsdPhysics, Gf, PhysxSchema





class StableQuadcopter:
    """A stable quadcopter with proper control"""

    def __init__(self, world, position=[0, 0, 1.5]):
        self.world = world
        self.position = np.array(position, dtype=float)
        self.prim_path = "/World/Quadcopter/body"

        # Physical parameters
        self.mass = 1.0  # kg
        self.gravity = 9.81  # m/s²

        # Create geometry
        self._create_quadcopter_geometry()

        # Control parameters
        self.target_height = 1.5

        # RigidPrim initialized later
        self.body = None

    def _create_quadcopter_geometry(self):
        """Create the quadcopter body"""

        # Create cube
        cube_geom = UsdGeom.Cube.Define(self.world.stage, self.prim_path)
        cube_geom.GetSizeAttr().Set(0.2)  # 20cm cube - easier to see
        cube_geom.AddTranslateOp().Set(Gf.Vec3d(float(self.position[0]),
                                                float(self.position[1]),
                                                float(self.position[2])))

        # Bright blue color
        cube_geom.GetDisplayColorAttr().Set([Gf.Vec3f(0.1, 0.5, 1.0)])

        # Add physics
        rigid_body_api = UsdPhysics.RigidBodyAPI.Apply(cube_geom.GetPrim())
        #rigid_body_api.GetLinearDampingAttr().Set(0.1)  # Add air resistance
        #rigid_body_api.GetAngularDampingAttr().Set(0.1)

        # Add mass
        mass_api = UsdPhysics.MassAPI.Apply(cube_geom.GetPrim())
        mass_api.GetMassAttr().Set(self.mass)

        # Add collision
        collision_api = UsdPhysics.CollisionAPI.Apply(cube_geom.GetPrim())
        #collision_api.GetCollisionEnabledAttr().Set(True)

        # PhysX settings - KEEP GRAVITY ON
        physx_rigid_body = PhysxSchema.PhysxRigidBodyAPI.Apply(
            cube_geom.GetPrim())
        # Higher solver iterations for better stability
        #physx_rigid_body.GetSolverPositionIterationCountAttr().Set(8)
        #physx_rigid_body.GetSolverVelocityIterationCountAttr().Set(2)

        # Don't disable gravity - we'll fight it with control

        print(f"✅ Quadcopter created at {self.position}")

    def initialize(self):
        """Initialize after world.reset()"""
        self.body = RigidPrim(prim_path=self.prim_path, name="quad_body")
        print(f"✅ Quadcopter ready to fly!")

    def hover_control(self):
        """Stable PD controller with velocity limits"""
        if self.body is None:
            return 0.0, 0.0, 0.0

        # Get state
        position, _ = self.body.get_world_pose()
        velocity = self.body.get_linear_velocity()

        current_height = float(position[2])
        current_vz = float(velocity[2]) if velocity is not None else 0.0

        # PD Control
        height_error = self.target_height - current_height

        # Proportional: Want to move toward target
        kp = 1.5
        desired_velocity = kp * height_error

        # Limit desired velocity
        max_velocity = 2.0  # Max 2 m/s vertical speed
        desired_velocity = np.clip(
            desired_velocity, -max_velocity, max_velocity)

        # Derivative: Damping
        kd = 2.0
        velocity_error = desired_velocity - current_vz

        # Control output (acceleration to apply)
        acceleration = kd * velocity_error

        # Limit acceleration
        max_accel = 5.0
        acceleration = np.clip(acceleration, -max_accel, max_accel)

        # Total acceleration needed (including gravity compensation)
        total_accel = acceleration + self.gravity

        # Convert to velocity change for this timestep
        dt = 1.0 / 60.0  # 60 Hz physics
        velocity_change = total_accel * dt

        # Apply new velocity
        new_vz = current_vz + velocity_change

        # CRITICAL: Limit absolute velocity to prevent runaway
        new_vz = np.clip(new_vz, -3.0, 3.0)

        # Set velocity (keep x,y zero for stability)
        new_velocity = np.array([0.0, 0.0, new_vz], dtype=np.float32)
        self.body.set_linear_velocity(new_velocity)

        return current_height, new_vz, height_error


def main():
    """Main simulation"""

    # Create world
    world = World(physics_dt=1.0/60.0, rendering_dt=1.0/60.0)
    world.scene.add_default_ground_plane()

    print("=" * 70)
    print("🚁 STABLE QUADCOPTER - Isaac Sim 5.1")
    print("=" * 70)

    # Create quadcopter
    # Start just above ground to avoid initial collision issues
    quadcopter = StableQuadcopter(world, position=[0, 0, 0.2])

    # Set camera view
    from omni.isaac.core.utils.viewports import set_camera_view
    import time
    time.sleep(0.5)

    eye = np.array([4.0, 4.0, 3.0])
    target = np.array([0.0, 0.0, 1.5])
    set_camera_view(
        eye=eye, target=target,
        camera_prim_path="/OmniverseKit_Persp")

    # Initialize physics
    print("🔄 Starting physics...")
    world.reset()

    # Initialize quadcopter
    quadcopter.initialize()

    print("🚀 FLIGHT STARTED!")
    print("   🎯 Target: 1.5m hover height")
    print("   👀 Watch the BLUE CUBE hover!")
    print("   ⏹️  Close window to stop")
    print("=" * 70)

    frame_count = 0

    try:
        while simulation_app.is_running():
            world.step(render=True)

            if world.is_playing():
                height, vz, error = quadcopter.hover_control()

                # Status every second
                if frame_count % 60 == 0:
                    if abs(error) < 0.1 and abs(vz) < 0.1:
                        status = "✅ HOVERING"
                    elif error > 0:
                        status = "↑ ASCENDING"
                    else:
                        status = "↓ DESCENDING"

                    print(f"[{frame_count:5d}] H:{height:5.2f}m "
                          f"V:{vz:+5.2f}m/s E:{error:+5.2f}m {status}")

                frame_count += 1

    except KeyboardInterrupt:
        print("\n⚠️  Stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n🛑 Shutting down...")
    simulation_app.close()
    print("✅ Done!")


if __name__ == "__main__":
    main()
