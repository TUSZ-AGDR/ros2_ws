# ============================================================
# server.py —— Python 服务端
#
# 本程序演示如何使用 Python 实现 ROS2 服务通信的服务端。
# 服务端提供"两整数相加"的功能（服务名：add_ints），
# 收到客户端请求后计算 num1 + num2 并返回 sum。
#
# 服务通信的"一问一答"模型：
#   客户端发出请求(Request) → 服务端处理后返回响应(Response)
#   （与话题通信的持续数据流不同，服务是一次性的）
#
# 核心知识点：
#   1. 导入并使用自定义服务接口（base_interfaces_demo.srv.AddInts）
#   2. 调用 create_service() 创建服务端并绑定回调函数
#   3. 回调函数接收 request，计算后返回 response
# ============================================================

import rclpy                                         # ROS2 Python 客户端库
from rclpy.node import Node                          # 节点基类
from base_interfaces_demo.srv import AddInts         # 自定义服务接口


class MinimalService(Node):
    """自定义服务节点，提供两数相加服务"""

    def __init__(self):
        super().__init__('minimal_service_py')

        # 【步骤1】创建服务端
        # 参数1：服务接口类型 AddInts
        # 参数2：服务名称 'add_ints'（客户端通过此名称查找服务）
        # 参数3：回调函数 add_two_ints_callback，处理客户端请求
        self.srv = self.create_service(AddInts, 'add_ints', self.add_two_ints_callback)
        self.get_logger().info("服务端启动！")

    def add_two_ints_callback(self, request, response):
        """服务回调函数：处理客户端请求并返回响应

        参数：
            request  —— 客户端发来的请求，包含 num1 和 num2 两个整数
            response —— 要返回给客户端的响应，需要填入 sum 字段

        返回值：
            填充好 sum 的 response 对象
        """
        # 【关键】计算并填写响应
        response.sum = request.num1 + request.num2
        self.get_logger().info(
            '请求数据:(%d,%d),响应结果:%d' % (request.num1, request.num2, response.sum))
        return response


def main():
    """程序入口：初始化 → 创建服务端节点 → 进入事件循环等待请求"""
    rclpy.init()                                # 初始化 rclpy
    minimal_service = MinimalService()          # 创建服务端节点
    rclpy.spin(minimal_service)                 # 进入事件循环，阻塞等待客户端请求
    rclpy.shutdown()                            # 清理资源


if __name__ == '__main__':
    main()
