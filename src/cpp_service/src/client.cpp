// ============================================================
// client.cpp —— C++ 客户端
//
// 本程序演示 ROS2 服务通信的客户端实现。
// 客户端通过命令行参数获取两个整数，发送给服务端计算它们的和，
// 然后接收并打印服务端返回的结果。
//
// 使用方法：
//   ros2 run cpp_service client 3 5
//   （3 和 5 是要相加的两个整数）
//
// 核心知识点：
//   1. 调用 create_client() 创建客户端
//   2. 调用 wait_for_service() 等待服务端上线
//   3. 调用 async_send_request() 异步发送请求
//   4. 调用 spin_until_future_complete() 等待响应结果
// ============================================================

#include "rclcpp/rclcpp.hpp"                           // ROS2 C++ 客户端库
#include "base_interfaces_demo/srv/add_ints.hpp"       // 自定义服务接口：AddInts

using base_interfaces_demo::srv::AddInts;
using namespace std::chrono_literals;   // 允许使用 1s 字面量

class MinimalClient: public rclcpp::Node{
  public:
    MinimalClient():Node("minimal_client"){
      // 【步骤1】创建客户端，指定要调用的服务名称为 "add_ints"
      client = this->create_client<AddInts>("add_ints");
      RCLCPP_INFO(this->get_logger(),"客户端创建，等待连接服务端！");
    }

    // 【步骤2】等待服务端上线（阻塞等待，直到服务端可用或 ROS2 被强制退出）
    bool connect_server(){
      // wait_for_service() 返回 true 表示服务端已就绪
      // 参数 1s 是每次重试的超时时间
      while (!client->wait_for_service(1s))
      {
        if (!rclcpp::ok())   // 检查 ROS2 是否仍在正常运行
        {
          RCLCPP_INFO(rclcpp::get_logger("rclcpp"),"强制退出！");
          return false;
        }
        RCLCPP_INFO(this->get_logger(),"服务连接中，请稍候...");
      }
      return true;
    }

    // 【步骤3】组织请求数据并异步发送
    // 返回 std::future 对象，用于后续获取响应结果
    rclcpp::Client<AddInts>::FutureAndRequestId send_request(int32_t num1, int32_t num2){
      auto request = std::make_shared<AddInts::Request>();  // 创建请求对象
      request->num1 = num1;   // 填入第一个加数
      request->num2 = num2;   // 填入第二个加数
      return client->async_send_request(request);           // 异步发送请求
    }

  private:
    rclcpp::Client<AddInts>::SharedPtr client;   // 客户端智能指针
};

int main(int argc, char ** argv)
{
  // 检查命令行参数：需要恰好两个整数
  if (argc != 3){
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"),"请提交两个整型数据！");
    return 1;
  }

  rclcpp::init(argc,argv);

  auto client = std::make_shared<MinimalClient>();

  // 等待服务端连接
  bool flag = client->connect_server();
  if (!flag)
  {
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"),"服务连接失败！");
    return 0;
  }

  // 发送请求（arg[1]和arg[2]是命令行传入的两个加数）
  auto response = client->send_request(atoi(argv[1]),atoi(argv[2]));

  // 【步骤4】等待响应结果并处理
  // spin_until_future_complete() 会阻塞等待，直到服务端返回响应
  if (rclcpp::spin_until_future_complete(client,response) ==
      rclcpp::FutureReturnCode::SUCCESS)
  {
    RCLCPP_INFO(client->get_logger(),"请求正常处理");
    RCLCPP_INFO(client->get_logger(),"响应结果:%d!", response.get()->sum);
  } else {
    RCLCPP_INFO(client->get_logger(),"请求异常");
  }

  rclcpp::shutdown();
  return 0;
}
