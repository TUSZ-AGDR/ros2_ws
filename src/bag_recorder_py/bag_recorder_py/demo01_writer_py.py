# ============================================================
# demo01_writer_py.py —— ROS2 Bag 录制器
#
# ROS2 Bag 是 ROS2 的"数据记录与回放"工具，类似一个"行车记录仪"。
# 它可以记录机器人运行时的所有话题数据到文件（.db3 格式/SQLite），
# 之后可以回放这些数据来调试、测试算法，而不需要重新运行机器人。
#
# 本程序演示如何通过 Python API 创建 Bag 录制器：
#   订阅 /turtle1/cmd_vel 话题（小海龟的速度指令），
#   并将收到的消息写入 Bag 文件中。
#
# Bag 文件存放位置：当前工作目录下的 my_bag_py/ 文件夹
#
# 使用方法：
#   1. 先启动 turtlesim：  ros2 run turtlesim turtlesim_node
#   2. 启动本录制器：      ros2 run bag_recorder_py demo01_writer_py
#   3. 控制海龟移动：      ros2 run turtlesim turtle_teleop_key
#   4. 停止录制：          Ctrl+C
#
# 核心知识点：
#   1. 导入 rosbag2_py（Python 的 Bag 操作库）
#   2. 配置 StorageOptions（存储路径和格式）
#   3. 使用 SequentialWriter 创建 Bag 写入器
#   4. 在回调中调用 writer.write() 将消息序列化后写入 Bag
# ============================================================

import rclpy
from rclpy.node import Node
from rclpy.serialization import serialize_message  # 消息序列化工具
from geometry_msgs.msg import Twist                # 速度指令消息类型
import rosbag2_py                                  # ROS2 Bag Python API


class SimpleBagRecorder(Node):
    """Bag 录制器节点：订阅话题并将数据记录到 Bag 文件"""

    def __init__(self):
        super().__init__('simple_bag_recorder_py')

        # ---------- 【步骤1】创建 Bag 写入器 ----------
        self.writer = rosbag2_py.SequentialWriter()

        # 【步骤2】配置存储选项
        # uri：Bag 文件的存储路径
        # storage_id：存储格式，'sqlite3' 是 ROS2 默认的 Bag 格式
        storage_options = rosbag2_py._storage.StorageOptions(
            uri='my_bag_py',           # 在当前目录下创建 my_bag_py 文件夹
            storage_id='sqlite3')      # 使用 SQLite3 数据库格式存储

        # ConverterOptions：消息序列化格式设置
        # 两个参数分别为输出序列化格式和输入序列化格式，留空表示使用默认的 cdr 格式
        converter_options = rosbag2_py._storage.ConverterOptions('', '')

        # 打开 Bag 文件准备写入
        self.writer.open(storage_options, converter_options)

        # 【步骤3】声明要录制的话题
        # 需要提供话题名称、消息类型和序列化格式
        topic_info = rosbag2_py._storage.TopicMetadata(
            name='/turtle1/cmd_vel',                    # 要录制的话题名称
            type='geometry_msgs/msg/Twist',             # 消息类型（完整路径）
            serialization_format='cdr')                 # 序列化格式（cdr 是 ROS2 默认）

        self.writer.create_topic(topic_info)  # 在 Bag 文件中创建该话题的"通道"

        # 【步骤4】创建订阅者，监听 /turtle1/cmd_vel 话题
        # 当收到消息时，自动调用 topic_callback 将消息写入 Bag
        self.subscription = self.create_subscription(
            Twist, '/turtle1/cmd_vel', self.topic_callback, 10)

    def topic_callback(self, msg):
        """消息回调：每收到一条消息，就写入 Bag 文件"""
        self.writer.write(
            '/turtle1/cmd_vel',                    # 话题名称
            serialize_message(msg),                # 将 ROS2 消息序列化为字节流
            self.get_clock().now().nanoseconds)    # 记录当前时间戳（纳秒）


def main(args=None):
    rclpy.init(args=args)
    sbr = SimpleBagRecorder()
    rclpy.spin(sbr)       # 进入事件循环，持续录制
    rclpy.shutdown()


if __name__ == '__main__':
    main()
