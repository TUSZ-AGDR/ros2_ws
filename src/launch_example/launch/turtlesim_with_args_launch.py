# ============================================================
# turtlesim_with_args_launch.py —— 带启动参数的 Launch 文件
#
# 本文件演示如何在 Launch 文件中声明和使用启动参数（Launch Argument）。
# 启动参数允许用户在启动时动态指定配置值，而不需要修改代码。
#
# 本例：通过参数控制 turtlesim 海龟模拟器的背景颜色（RGB）。
#
# 运行方式（可在命令行自定义参数）：
#   ros2 launch launch_example turtlesim_with_args_launch.py
#   ros2 launch launch_example turtlesim_with_args_launch.py background_r:=255 background_b:=128
#
# 核心知识点：
#   1. DeclareLaunchArgument —— 声明一个启动参数（参数名、默认值）
#   2. LaunchConfiguration —— 在 Launch 文件中引用启动参数的值
#   3. parameters 参数 —— 将参数值传递给 ROS2 节点
# ============================================================

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    """
    声明启动参数 → 创建节点并传入参数 → 返回完整的 Launch 描述
    """

    # ---------- 声明启动参数 ----------
    # DeclareLaunchArgument 定义了一个可在 ros2 launch 命令行指定的参数
    # default_value 指定了用户不传参时的默认值

    # 背景红色分量（0-255）
    background_r_arg = DeclareLaunchArgument(
        'background_r',
        default_value=TextSubstitution(text='0')    # 默认：红色=0
    )

    # 背景绿色分量（0-255）
    background_g_arg = DeclareLaunchArgument(
        'background_g',
        default_value=TextSubstitution(text='255')  # 默认：绿色=255
    )

    # 背景蓝色分量（0-255）
    background_b_arg = DeclareLaunchArgument(
        'background_b',
        default_value=TextSubstitution(text='0')    # 默认：蓝色=0
    )
    # 三个参数默认值为 (0,255,0) → 绿色背景

    # ---------- 创建 turtlesim 节点 ----------
    # 将启动参数作为 ROS2 节点参数传入
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='sim',
        # parameters 列表中的 LaunchConfiguration 会读取启动参数的值
        # 然后作为 ROS2 参数传递给 nodes 节点
        parameters=[{
            'background_r': LaunchConfiguration('background_r'),
            'background_g': LaunchConfiguration('background_g'),
            'background_b': LaunchConfiguration('background_b'),
        }]
    )

    # 返回包含所有声明和节点的 LaunchDescription
    return LaunchDescription([
        background_r_arg,   # 必须先把参数声明加入描述，然后才是节点
        background_g_arg,
        background_b_arg,
        turtlesim_node,
    ])
