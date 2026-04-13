# Robocon 2026: Round 1 Submission

**Author:** Rudraneel Shee

**Objective:** Creating URDF of custom bot from Solidworks, configuring robotic arm movement using MoveIt

**NOTE: This is not the final repo. Will update soon.**

## Features
* **Robot Description:** Custom URDF/Xacro integrating a 6-DOF AR4 arm onto a custom tracked wheel drive chassis.
* **Physics Simulation:** Gazebo (Harmonic) integration with `gz_ros2_control` and accurate joint dynamics.
* **Motion Planning:** MoveIt 2 configuration with collision-aware inverse kinematics (OMPL) and time-optimal trajectory generation.
* **World:** Custom Robocon arena loaded via SDF.

## Dependencies
Ensure you have the following installed:
* ROS 2 Jazzy
* Gazebo (Harmonic)
* MoveIt 2 (`sudo apt install ros-jazzy-moveit`)
* `ros_gz` bridge packages
* `annin_ar4_description` (Required for AR4 arm meshes)

## Build Instructions
Clone this repository into the `src` folder of your ROS 2 workspace:
```bash
cd ~/ros2_ws/src
git clone https://github.com/EigenRudra/robocon26-ros2-customURDF-MoveIt.git
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

## Usage

Launch the complete simulation stack (Gazebo, `ros2_control`, MoveIt, and RViz) perfectly synchronized to simulation time:

```bash
ros2 launch my_bot_updated full_sim.launch.py
```

Use the interactive marker in RViz to set a goal pose for the arm, click Plan, and click Execute to see the simulated arm move in Gazebo.

## Acknowledgments & Credits

* **Robotic Arm:** The arm models, URDF macros, and base configurations used in this project are sourced from the excellent [ar4_ros_driver](https://github.com/ycheng517/ar4_ros_driver/) repository by [ycheng517](https://github.com/ycheng517). Huge thanks for providing the open-source ROS 2 driver and description packages for the Annin AR4 robot arm!


##Visuals

Click to watch the video
