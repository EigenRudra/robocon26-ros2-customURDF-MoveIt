import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro
from pathlib import Path

def generate_launch_description():
    pkg_name = 'my_bot_updated'
    pkg_share = get_package_share_directory(pkg_name)

    
    install_dir = get_package_share_directory(pkg_name)
    
    
    gz_resource_path_env = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            os.path.join(install_dir, '..'), 
            ':' + str(Path.home() / '.gazebo/models') 
        ]
    )

    #Parse XACRO
    xacro_file = os.path.join(pkg_share, 'urdf', 'my_bot_updated.urdf.xacro')
    doc = xacro.process_file(xacro_file)
    robot_desc = doc.toxml()

    #Launch Gazebo with custom world
    world_file = os.path.join(pkg_share, 'worlds', 'robocon.sdf')
    
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items(),
    )

    #Spawn robot
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'my_bot',
                   '-z', '1.0', 
                   '-x', '0.6165',
                   '-y', '1.0'],
        output='screen'
    )
    
    #Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher', 
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc,'use_sim_time': True}]
    )

    #Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
	    '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
            '/joint_states@sensor_msgs/msg/JointState@gz.msgs.Model',
        ],
        remappings=[
            ('/world/robocon_world/clock', '/clock'), 
        ],
        output='screen'
    )

    #Spawn Controllers
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    joint_trajectory_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller", "--controller-manager", "/controller_manager"],
    )

    return LaunchDescription([
        gz_resource_path_env,
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
        bridge,
        joint_state_broadcaster_spawner,
        joint_trajectory_controller_spawner
    ])
