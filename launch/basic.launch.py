import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

PACKAGE_NAME = "bugs_algorithm"
WORLD_NAME = "bug0.sdf"
SDF_MODEL_NAME = "vehicle"

def generate_launch_description():
    ld = LaunchDescription()

    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg = get_package_share_directory(PACKAGE_NAME)
    pkg = "/home/user/wasp_ws/src/bugs_algorithm"
    sdf_path = f"{pkg}/models/{SDF_MODEL_NAME}/model.sdf"

    resources = [
        os.path.join(pkg, "worlds"),
        os.path.join(pkg, "models")
    ]
    resource_env = SetEnvironmentVariable(name="IGN_GAZEBO_RESOURCE_PATH", value=":".join(resources))

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
            launch_arguments={'gz_args': f'-r -v 2 {WORLD_NAME}'}.items(),
    )

    
    # spawn sdf
    spawn_sdf = Node(package='ros_gz_sim', executable='create',
			arguments=['-name', 'vehicle',
				'-x', '0.0',
                '-y', '6.0',
				'-z', '1.0',
				'-Y', '-1.575',
				'-file', os.path.join(pkg, 'models', 'vehicle', 'model.sdf')],
			output='screen')

    ld.add_action(resource_env)
    ld.add_action(gazebo)
    ld.add_action(spawn_sdf)
    return ld
