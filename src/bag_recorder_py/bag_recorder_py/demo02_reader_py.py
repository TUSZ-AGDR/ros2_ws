# ============================================================
# demo02_reader_py.py —— ROS2 Bag 回放器（读取器）
#
# 本程序演示如何通过 Python API 读取之前录制的 Bag 文件。
# 逐条读取 Bag 中存储的每条消息，并打印话题名、时间戳和数据内容。
#
# 使用方法：
#   确保 my_bag_py/ 文件夹存在（由 demo01_writer_py 生成），
#   然后运行本程序读取其中的数据：
#     ros2 run bag_recorder_py demo02_reader_py
#
# 核心知识点：
#   1. 使用 SequentialReader 创建 Bag 读取器
#   2. 配置与写入时相同的 StorageOptions
#   3. 使用 has_next() + read_next() 循环逐条读取消息
#   4. 每条消息包含三元组：(话题名, 序列化数据, 时间戳)
# ============================================================

import rclpy
from rclpy.node import Node
import rosbag2_py                                  # ROS2 Bag Python API
from rclpy.logging import get_logger               # ROS2 日志工具


class SimpleBagPlayer(Node):
    """Bag 回放器节点：读取 Bag 文件中的所有消息并打印"""

    def __init__(self):
        super().__init__('simple_bag_player_py')

        # ---------- 【步骤1】创建 Bag 读取器 ----------
        self.reader = rosbag2_py.SequentialReader()

        # 【步骤2】配置与写入时相同的存储选项
        # uri 必须指向之前录制的 Bag 文件夹
        storage_options = rosbag2_py._storage.StorageOptions(
            uri='my_bag_py',           # Bag 文件路径（与录制时的一致）
            storage_id='sqlite3')      # 存储格式

        converter_options = rosbag2_py._storage.ConverterOptions('', '')

        # 打开 Bag 文件准备读取
        self.reader.open(storage_options, converter_options)

    def read(self):
        """逐条读取并打印 Bag 中的所有消息"""
        # 【步骤3】循环读取消息
        # has_next() 检查是否还有未读的消息
        while self.reader.has_next():
            # read_next() 返回三元组：
            #   topic    —— 消息所属的话题名称
            #   data     —— 序列化后的消息字节流
            #   timestamp —— 消息录制时的时间戳（纳秒）
            topic, data, timestamp = self.reader.read_next()
            get_logger("rclpy").info(
                f"话题={topic}, 时间戳={timestamp}, 数据={data}")


def main(args=None):
    rclpy.init(args=args)
    reader = SimpleBagPlayer()
    reader.read()        # 一次性读取所有消息并输出
    rclpy.shutdown()


if __name__ == '__main__':
    main()
