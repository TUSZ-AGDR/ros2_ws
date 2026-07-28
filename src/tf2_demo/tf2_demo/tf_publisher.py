# ============================================================
# tf_publisher.py —— TF2 坐标变换发布者
#
# 本程序演示 ROS2 中的 TF2（坐标变换系统）。
# TF2 是机器人系统中用于描述"各个部件之间的空间位置关系"的框架，
# 类似于机器人的"骨骼系统"——定义了谁在哪、朝向哪个方向。
#
# 本例：发布一个动态的坐标变换关系——
#   父坐标系：base_link（机器人的基座，通常是机器人中心）
#   子坐标系：test_link（一个测试用的"部件"，相对于 base_link 运动）
#
# 变换效果：
#   test_link 位于 base_link 沿 X 轴 1 米处，
#   并绕 Y 轴持续旋转（模拟一个运动中的部件）。
#
# 可视化查看：
#   ros2 run tf2_demo tf_publisher &
#   ros2 run tf2_tools view_frames   # 生成坐标系关系图
#   ros2 run rviz2 rviz2            # 在 RViz 中可视化坐标系
#
# 核心知识点：
#   1. 导入 tf2_ros.TransformBroadcaster（变换广播器）
#   2. 使用 geometry_msgs.msg.TransformStamped 描述变换
#   3. 变换 = 平移(translation) + 旋转(rotation)
#   4. 旋转使用"四元数"(x,y,z,w) 表示，避免万向节锁死问题
# ============================================================

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped  # 标准变换消息类型
import tf2_ros                                   # TF2 ROS 接口
import math


class TFPublisher(Node):
    """TF2 坐标变换发布节点"""

    def __init__(self):
        super().__init__('tf_publisher')

        # 【步骤1】创建变换广播器（TransformBroadcaster）
        # 它会将你定义的坐标变换关系广播给所有订阅者
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        # 【步骤2】创建定时器，以 10Hz 的频率发布变换
        # 频率越高，变换越平滑
        self.timer = self.create_timer(0.1, self.broadcast_tf)

        self.angle = 0.0  # 初始旋转角度（弧度）

    def broadcast_tf(self):
        """定时回调：构建并发布一条变换消息"""

        # 【步骤3】创建 TransformStamped（带时间戳的变换）消息
        t = TransformStamped()

        # --- 时间戳和坐标系标识 ---
        t.header.stamp = self.get_clock().now().to_msg()  # 当前时间戳
        t.header.frame_id = 'base_link'     # 父坐标系（参考系）
        t.child_frame_id = 'test_link'      # 子坐标系（被描述的坐标系）
        # 含义：test_link 在 base_link 坐标系中的位置和姿态

        # --- 【步骤4】设置平移（translation）：test_link 在 base_link 中的位置 ---
        # 单位：米
        t.transform.translation.x = 1.0     # 沿 X 轴正方向 1 米
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0

        # --- 【步骤5】设置旋转（rotation）：test_link 相对于 base_link 的姿态 ---
        # 使用四元数（Quaternion）表示旋转，由 4 个分量组成：(x, y, z, w)

        self.angle += 0.1                     # 每 0.1 秒增加 0.1 弧度
        if self.angle > 2 * math.pi:          # 超过一圈后归零
            self.angle -= 2 * math.pi

        # 手动计算绕 Y 轴旋转的四元数（避免引入外部依赖库）
        # 公式：绕 Y 轴旋转 θ → q = (0, sin(θ/2), 0, cos(θ/2))
        cy = math.cos(self.angle * 0.5)
        sy = math.sin(self.angle * 0.5)
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = sy            # Y 轴分量
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = cy            # 标量分量

        # 【步骤6】发送变换
        # 广播后，所有 TF2 监听者都能接收到这个坐标关系
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = TFPublisher()
    rclpy.spin(node)     # 进入事件循环，持续发布变换
    rclpy.shutdown()


if __name__ == '__main__':
    main()
