# ============================================================
# turtlesim_mimic_launch.py —— Launch 文件示例（Python 格式）
#
# Launch 文件是 ROS2 中用于"一键启动多个节点"的脚本。
# 本文件演示如何同时启动两个 turtlesim 海龟模拟器和一个 mimic 节点，
# mimic 节点能够让第二个海龟自动模仿第一个海龟的运动轨迹。
#
# Launch 文件的两种写法：
#   1. Python 格式（本文件）：灵活，支持条件判断和循环
#   2. YAML 格式（见同目录 .yaml 文件）：简洁，适合简单场景
#
# 运行方式：
#   ros2 launch launch_example turtlesim_mimic_launch.py
#
# 核心知识点：
#   1. from launch_ros.actions import Node —— 导入节点启动动作
#   2. Node() 描述要启动的节点（包名、可执行文件、节点名、命名空间）
#   3. remappings 实现话题重映射（将不同命名空间的话题连接起来）
#   4. generate_launch_description() 返回 LaunchDescription
# ============================================================

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Launch 描述生成函数（函数名必须是这个，ROS2 框架会自动调用）

    返回一个 LaunchDescription 对象，其中包含要启动的所有节点。
    """

    return LaunchDescription([
        # ---------- 节点1：第一个海龟模拟器 ----------
        # 命名空间 turtlesim1 用于隔离同名话题，避免冲突
        Node(
            package='turtlesim',           # 功能包名称
            namespace='turtlesim1',        # 命名空间（该节点的话题都会加上 /turtlesim1 前缀）
            executable='turtlesim_node',   # 可执行文件名
            name='sim'                     # 节点名称
        ),

        # ---------- 节点2：第二个海龟模拟器 ----------
        # 与节点1的配置完全相同，仅命名空间不同
        Node(
            package='turtlesim',
            namespace='turtlesim2',        # 不同的命名空间，实现两个独立的海龟
            executable='turtlesim_node',
            name='sim'
        ),

        # ---------- 节点3：mimic 模仿节点 ----------
        # mimic 节点订阅第一个海龟的位姿，发布速度指令给第二个海龟
        # 效果：第二个海龟会完全复制第一个海龟的运动
        Node(
            package='turtlesim',
            executable='mimic',
            name='mimic',
            # remappings（话题重映射）：将默认话题映射到带命名空间的实际话题
            # mimic 默认从 /input/pose 读位姿，输出到 /output/cmd_vel
            # 重映射后：从 turtlesim1 的海龟读位姿，向 turtlesim2 的海龟发指令
            remappings=[
                ('/input/pose', '/turtlesim1/turtle1/pose'),   # 输入：读取海龟1的位姿
                ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'),  # 输出：控制海龟2的速度
            ]
        )
    ])
