import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    fishbot_navigation2_dir = get_package_share_directory('fishbot_navigation2')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    rviz_config_dir = os.path.join(
        nav2_bringup_dir , 'rviz2' , 'nav2_default_view.rviz'
    )
    
    # creatre 'launch' for load: sim-time:True ,map_path:....yaml,nav2_path :config
    use_sim_time = launch.substitutions.LaunchConfiguration(
        'use_sim_time' ,default = 'true'
    )
    map_yaml_path = launch.substitutions.LaunchConfiguration(
        'map' ,default = os.path.join(fishbot_navigation2_dir,'maps','room.yaml',)
    )
    nav2_paramers_path = launch.substitutions.LaunchConfiguration(
        'paramers_path' ,default = os.path.join(fishbot_navigation2_dir,'config','nav2_params.yaml')       
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument('use_sim_time' ,default_value = use_sim_time,description = "use simulation gazebo clock ")
        launch.actions.DeclareLaunchArgument('map' ,default_value = map_yaml_path,description = "full path for loading map")
        launch.actions.DeclareLaunchArgument('paramers_path' ,default_value = nav2_paramers_path, description = "full path for paramers to load")
        
        launch.actions.IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [nav2_bringup_dir,'/launch','/bringup_launch.py']
            ),

            # using launch arguments for changing paramers
            launch_argments={
            'map':map_yaml_path,
            'use_sim_time':use_sim_time,
            'paramers_path':nav2_paramers_path}.items(),
        ),
        launch_ros.actions.Node(
            package = "rviz2",
            executable = "rviz2",
            name = "rviz2",
            arguments = ['-d',rviz_config_dir],
            paramers = [{'use_sim_time': use_sim_time}],
            output = "screen"      
        ),

    ])




