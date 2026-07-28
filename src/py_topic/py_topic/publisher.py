# ============================================================
# publisher.py —— Python 话题发布者
#
# 本程序演示如何使用 Python 实现 ROS2 话题通信的发布端。
# 发布者以 1 秒为周期，向话题 "chatter" 持续发送 String 消息。
#
# 核心知识点：
#   1. 继承 rclpy.node.Node 创建自定义节点
#   2. 调用 create_publisher() 创建发布者
#   3. 调用 create_timer() 创建定时器驱动周期性发布
#   4. 调用 publish() 将消息发送到话题
#   5. rclpy.spin() 使节点持续运行，等待回调触发
# ============================================================

import rclpy                         # ROS2 Python 客户端库
from rclpy.node import Node          # 节点基类
from std_msgs.msg import String      # 标准消息类型：字符串

class MinimalPublisher(Node):
    """自定义发布者节点，继承自 Node"""

    def __init__(self):
        # 调用父类构造函数，设置节点名称为 'minimal_publisher'
        super().__init__('minimal_publisher')

        # 【步骤1】创建发布者
        # 参数1：消息类型 String
        # 参数2：话题名称 'chatter'（订阅者通过同名话题接收消息）
        # 参数3：消息队列大小 10（用于缓存待发送的消息）
        self.publisher_ = self.create_publisher(String, 'chatter', 10)

        # 【步骤2】创建定时器，每 1.0 秒调用一次 timer_callback()
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.count = 0  # 消息计数器，每条消息编号递增

    def timer_callback(self):
        """定时器回调：每秒自动执行一次，发布一条消息"""
        msg = String()                                      # 创建一个 String 消息对象
        msg.data = f'Hello ROS2: {self.count}'              # 填入消息内容（带编号）
        self.get_logger().info(f'发布: "{msg.data}"')        # 在终端打印日志
        self.publisher_.publish(msg)                        # 【关键】将消息发布到话题
        self.count += 1                                     # 计数器加 1


def main(args=None):
    """程序入口：初始化 → 创建节点 → 进入循环 → 清理退出"""
    rclpy.init(args=args)               # 【步骤1】初始化 rclpy 客户端库
    rclpy.spin(MinimalPublisher())      # 【步骤2】创建发布节点并进入事件循环
    rclpy.shutdown()                    # 【步骤3】程序结束时清理资源


if __name__ == '__main__':
    main()
