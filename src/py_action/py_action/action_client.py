# ============================================================
# action_client.py —— Python 动作客户端
#
# 本程序演示如何使用 Python 实现 ROS2 动作通信的客户端。
# 客户端向服务端发送目标（计算 10 阶斐波那契数列），
# 并通过异步回调方式接收服务端的响应和结果。
#
# 动作客户端的异步模式：
#   发送目标后不阻塞，通过 add_done_callback() 注册回调函数
#   当服务端响应或返回结果时，自动触发对应的回调。
#
# 核心知识点：
#   1. 导入 ActionClient 类和自定义 Fibonacci 动作接口
#   2. 创建 ActionClient 并等待服务端上线
#   3. 调用 send_goal_async() 异步发送目标
#   4. 通过 add_done_callback() 注册目标响应和结果回调
# ============================================================

import rclpy
from rclpy.action import ActionClient           # 动作客户端类
from rclpy.node import Node

from base_interfaces_demo.action import Fibonacci  # 自定义动作接口


class FibonacciActionClient(Node):
    """斐波那契动作客户端节点"""

    def __init__(self):
        super().__init__('fibonacci_action_client')

        # 【步骤1】创建动作客户端
        # 参数1：节点自身
        # 参数2：动作接口类型 Fibonacci
        # 参数3：动作名称 'fibonacci'（必须与服务端一致）
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        """发送目标到动作服务端"""
        # 构建目标消息：指定要计算的斐波那契阶数
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        # 【步骤2】等待服务端上线
        self._action_client.wait_for_server()

        # 【步骤3】异步发送目标
        # send_goal_async() 返回一个 Future 对象
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)

        # 【步骤4】注册回调：当服务端回复目标是否被接受时调用
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """目标响应回调：服务端接受还是拒绝了目标？"""
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('目标被拒绝')
            return

        self.get_logger().info('目标已被接受')

        # 【步骤5】目标被接受后，注册结果回调
        # get_result_async() 返回一个 Future，在任务完成后被触发
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """结果回调：任务结束后，接收最终结果"""
        result = future.result().result     # 获取 Fibonacci.Result 对象
        self.get_logger().info('最终结果（完整序列）: {0}'.format(result.sequence))
        rclpy.shutdown()                    # 收到结果后退出


def main(args=None):
    rclpy.init(args=args)

    action_client = FibonacciActionClient()
    action_client.send_goal(10)  # 请求计算 10 阶斐波那契数列

    rclpy.spin(action_client)    # 进入事件循环等待回调


if __name__ == '__main__':
    main()
