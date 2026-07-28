# ============================================================
# param_demo.py —— Python 参数演示
#
# 本程序演示 ROS2 中如何使用参数（Parameter）。
# 参数是节点的"配置开关"，可以在不重新编译的情况下动态调整节点行为。
#
# 参数操作（在终端中使用）：
#   查看所有参数：  ros2 param list
#   读取某个参数：  ros2 param get /param_demo_node robot_name
#   动态修改参数：  ros2 param set /param_demo_node robot_name "turtlebot"
#
# 核心知识点：
#   1. 调用 declare_parameter() 声明参数和默认值
#   2. 调用 get_parameter() 读取参数当前值
#   3. 在定时器中重复读取参数，观察运行时动态修改的效果
# ============================================================

import rclpy
from rclpy.node import Node

class ParamDemoNode(Node):
    """参数演示节点"""

    def __init__(self):
        super().__init__('param_demo_node')

        # 【步骤1】声明参数并设置默认值
        # 参数名 'robot_name'，默认值 'robot_01'
        # 如果用户从不修改，节点就使用默认值
        self.declare_parameter('robot_name', 'robot_01')

        # 【步骤2】读取参数的初始值
        # .value 属性返回参数的当前值
        robot_name = self.get_parameter('robot_name').value
        self.get_logger().info(f'初始 robot_name 参数值: {robot_name}')

        # 【步骤3】创建定时器，每秒读取一次参数
        # 这样当你通过 ros2 param set 修改参数后，
        # 下一轮回调就能看到最新的值
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        """定时回调：读取并打印参数当前值"""
        robot_name = self.get_parameter('robot_name').value
        self.get_logger().info(f'当前 robot_name 参数值: {robot_name}')


def main(args=None):
    rclpy.init(args=args)
    node = ParamDemoNode()
    rclpy.spin(node)     # 进入事件循环，定时器每秒触发一次
    rclpy.shutdown()


if __name__ == '__main__':
    main()
