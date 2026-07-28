# ============================================================
# subscriber.py —— Python 话题订阅者
#
# 本程序演示如何使用 Python 实现 ROS2 话题通信的接收端。
# 订阅者持续监听 "chatter" 话题，收到消息后通过回调函数输出内容。
#
# 核心知识点：
#   1. 调用 create_subscription() 创建订阅者并绑定回调函数
#   2. 发布者与订阅者通过相同的"话题名称"建立通信关系
#   3. rclpy.spin() 使节点保持运行，持续等待消息到达
# ============================================================

import rclpy                         # ROS2 Python 客户端库
from rclpy.node import Node          # 节点基类
from std_msgs.msg import String      # 标准消息类型：字符串

class MinimalSubscriber(Node):
    """自定义订阅者节点，继承自 Node"""

    def __init__(self):
        # 调用父类构造函数，设置节点名称为 'minimal_subscriber'
        super().__init__('minimal_subscriber')

        # 【步骤1】创建订阅者
        # 参数1：消息类型——String
        # 参数2：要订阅的话题名称 'chatter'
        #          （必须与发布者的话题名一致才能接收到消息！）
        # 参数3：消息到达时的回调函数 listener_callback
        # 参数4：消息队列大小 10
        self.subscription = self.create_subscription(
            String, 'chatter', self.listener_callback, 10)

    def listener_callback(self, msg):
        """消息回调函数：每收到一条新消息时自动调用"""
        # msg.data 包含接收到的字符串内容
        self.get_logger().info(f'接收: "{msg.data}"')


def main(args=None):
    """程序入口：初始化 → 创建节点 → 进入循环 → 清理退出"""
    rclpy.init(args=args)                   # 【步骤1】初始化 rclpy 客户端库
    rclpy.spin(MinimalSubscriber())         # 【步骤2】创建订阅节点并进入事件循环
    rclpy.shutdown()                        # 【步骤3】程序结束时清理资源


if __name__ == '__main__':
    main()
