# ============================================================
# action_server.py —— Python 动作服务端
#
# 本程序演示如何使用 Python 实现 ROS2 动作通信的服务端。
# 动作（Action）是服务的升级版，专为"长时间任务"设计，
# 支持实时反馈进度和随时取消任务。
#
# 本例功能：根据客户端指定的阶数，逐项计算斐波那契数列，
# 每计算一项就反馈一次当前序列，全部完成后返回完整结果。
#
# 动作的三大要素：
#   Goal（目标）    —— 客户端提交的任务参数（如：要算多少项）
#   Feedback（反馈）—— 服务端在执行过程中实时返回的进度信息
#   Result（结果）  —— 任务全部完成后返回的最终数据
#
# 核心知识点：
#   1. 导入 ActionServer 类和自定义 Fibonacci 动作接口
#   2. 创建 ActionServer 并绑定 execute_callback 回调
#   3. 在回调中通过 goal_handle.publish_feedback() 发布进度
#   4. 通过 goal_handle.succeed() 标记任务完成并返回结果
# ============================================================

import time

import rclpy
from rclpy.action import ActionServer           # 动作服务端类
from rclpy.node import Node

from base_interfaces_demo.action import Fibonacci  # 自定义动作接口


class FibonacciActionServer(Node):
    """斐波那契动作服务端节点"""

    def __init__(self):
        super().__init__('fibonacci_action_server')

        # 【步骤1】创建动作服务端
        # 参数1：节点自身
        # 参数2：动作接口类型 Fibonacci
        # 参数3：动作名称 'fibonacci'
        # 参数4：执行回调函数 execute_callback
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        """动作执行回调：当客户端提交目标后自动调用

        参数 goal_handle：包含客户端请求（goal_handle.request.order）
        以及发布反馈和设置结果的方法
        """
        self.get_logger().info('开始执行斐波那契计算...')

        # 初始化反馈消息（包含已计算的部分序列）
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]  # 斐波那契数列前两项

        # 从第 3 项开始计算（i 从 1 开始，对应实际索引 1，即数列第 2 项之后）
        for i in range(1, goal_handle.request.order):
            # 每一项 = 前两项之和
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] +
                feedback_msg.partial_sequence[i-1])

            self.get_logger().info(
                '反馈进度: {0}'.format(feedback_msg.partial_sequence))

            # 【步骤2】发布反馈，将当前进度实时通知客户端
            goal_handle.publish_feedback(feedback_msg)

            time.sleep(1)  # 模拟计算耗时，每 1 秒计算一项

        # 【步骤3】标记任务成功完成
        goal_handle.succeed()

        # 构建并返回最终结果（完整的斐波那契序列）
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result


def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(fibonacci_action_server)  # 进入事件循环，等待客户端提交目标


if __name__ == '__main__':
    main()
