# ============================================================
# tf_listener.py —— TF2 坐标变换监听者
#
# 本程序演示如何使用 TF2 查询两个坐标系之间的空间变换关系。
# 监听者每隔 0.5 秒查询一次 base_link → test_link 的变换，
# 并打印 test_link 在 base_link 坐标系中的位置。
#
# TF2 的查询-监听模型：
#   发布者（tf_publisher.py）：持续广播坐标系之间的变换
#   监听者（本文件）：通过 Buffer + TransformListener 接收并缓存变换，
#                    再调用 lookup_transform() 查询任意两帧之间的关系
#
# 核心知识点：
#   1. 创建 tf2_ros.Buffer（变换缓存区）存储接收到的变换数据
#   2. 创建 tf2_ros.TransformListener（变换监听器）订阅 /tf 话题
#   3. 调用 buffer.lookup_transform(目标帧, 源帧, 时间) 查询变换
#   4. 使用 try-except 处理变换尚不可用的情况
# ============================================================

import rclpy
from rclpy.node import Node
import tf2_ros
from tf2_ros import TransformException  # TF2 异常类


class TFListener(Node):
    """TF2 变换监听节点"""

    def __init__(self):
        super().__init__('tf_listener')

        # 【步骤1】创建 TF2 缓存区（Buffer）
        # Buffer 会自动存储收到的所有变换数据，供后续查询
        self.tf_buffer = tf2_ros.Buffer()

        # 【步骤2】创建变换监听器（TransformListener）
        # 它会自动订阅 /tf 和 /tf_static 话题，
        # 将收到的变换消息存入 Buffer 中
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # 【步骤3】创建定时器，每 0.5 秒查询一次变换
        self.timer = self.create_timer(0.5, self.query_transform)

    def query_transform(self):
        """查询并打印 base_link → test_link 的变换"""
        try:
            # 【步骤4】查询变换
            # lookup_transform(目标帧, 源帧, 时间点)
            # 含义：查询源帧(test_link)在目标帧(base_link)坐标系下的位置和姿态
            # 参数 rclpy.time.Time() 表示"查找最新可用的变换"
            transform = self.tf_buffer.lookup_transform(
                'base_link',            # 目标帧（相当于"从谁的角度看"）
                'test_link',            # 源帧（要查询的坐标系）
                rclpy.time.Time()       # 时间点（最新的可用变换）
            )

            # 打印平移分量（test_link 在 base_link 下的 x, y, z 位置）
            self.get_logger().info(
                f'translation: x={transform.transform.translation.x:.3f}, '
                f'y={transform.transform.translation.y:.3f}, '
                f'z={transform.transform.translation.z:.3f}'
            )

        except TransformException as e:
            # 如果变换尚不可用（发布者还没启动、或数据还没到达），
            # 捕获异常并给出提示而不是崩溃
            self.get_logger().warn(f'无法获取变换: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = TFListener()
    rclpy.spin(node)     # 进入事件循环，每 0.5 秒查询一次变换
    rclpy.shutdown()


if __name__ == '__main__':
    main()
