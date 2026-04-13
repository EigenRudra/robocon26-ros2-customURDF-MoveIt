from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import SetParameter
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    my_bot_pkg = get_package_share_directory('my_bot_updated')
    moveit_pkg = get_package_share_directory('my_bot_moveit_config')

    return LaunchDescription([
        SetParameter(name='use_sim_time', value=True),

        #Launch Gazebo, Bridges, and Controllers
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(my_bot_pkg, 'launch', 'sim.launch.py'))
        ),
        
        #Launch MoveIt
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(moveit_pkg, 'launch', 'move_group.launch.py'))
        ),
        
        #Launch RViz 
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(moveit_pkg, 'launch', 'moveit_rviz.launch.py'))
        )
    ])
