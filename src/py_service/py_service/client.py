# ============================================================
# client.py —— Python 客户端
#
# 本程序演示如何使用 Python 实现 ROS2 服务通信的客户端。
# 客户端从命令行参数获取两个整数，向服务端发送"加法"请求，
# 等待并打印服务端返回的计算结果。
#
# 使用方法：
#   ros2 run py_service client 3 5
#   （3 和 5 是要相加的两个整数）
#
# 核心知识点：
#   1. 调用 create_client() 创建客户端
#   2. 调用 wait_for_service() 阻塞等待服务端上线
#   3. 调用 call_async() 异步发送请求
#   4. 调用 spin_until_future_complete() 等待响应到达
# ============================================================

import sys                                           # 读取命令行参数
import rclpy                                         # ROS2 Python 客户端库
from rclpy.node import Node                          # 节点基类
from base_interfaces_demo.srv import AddInts         # 自定义服务接口


class MinimalClient(Node):
    """自定义客户端节点，向服务端发送加法请求"""

    def __init__(self):
        super().__init__('minimal_client_py')

        # 【步骤1】创建客户端
        # 参数1：服务接口类型 AddInts
        # 参数2：服务名称 'add_ints'（必须与服务端的服务名一致）
        self.cli = self.create_client(AddInts, 'add_ints')

        # 【步骤2】等待服务端上线（阻塞等待）
        # wait_for_service() 返回 True 时表示服务端已就绪
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('服务连接中，请稍候...')

        self.req = AddInts.Request()  # 预先创建请求对象

    def send_request(self):
        """【步骤3】组织请求数据并通过异步方式发送"""
        self.req.num1 = int(sys.argv[1])    # 从命令行参数获取第一个加数
        self.req.num2 = int(sys.argv[2])    # 从命令行参数获取第二个加数
        # call_async() 异步发送请求，返回一个 Future 对象（类似"收据"）
        self.future = self.cli.call_async(self.req)


def main():
    rclpy.init()

    minimal_client = MinimalClient()
    minimal_client.send_request()  # 发送请求

    # 【步骤4】等待响应并处理结果
    # spin_until_future_complete() 阻塞等待直到服务端返回响应
    rclpy.spin_until_future_complete(minimal_client, minimal_client.future)

    try:
        response = minimal_client.future.result()   # 获取响应结果
    except Exception as e:
        # 如果请求失败（如服务端崩溃），捕获并打印异常
        minimal_client.get_logger().info('服务请求失败： %r' % (e,))
    else:
        # 请求成功，打印服务端返回的计算结果
        minimal_client.get_logger().info(
            '响应结果： %d + %d = %d' %
            (minimal_client.req.num1, minimal_client.req.num2, response.sum))

    rclpy.shutdown()


if __name__ == '__main__':
    main()
