// ============================================================
// server.cpp —— C++ 服务端
//
// 本程序演示 ROS2 的第二种通信模型：服务（Service）通信
// 服务端提供"两整数相加"的功能，等待客户端发送请求。
//
// 服务通信与话题通信的核心区别：
//   话题：单向、持续的数据流（发布者 → 订阅者），适合传感器数据
//   服务：请求-响应模式（客户端 → 服务端 → 客户端），适合一次性计算
//
// 核心知识点：
//   1. 使用自定义服务接口（base_interfaces_demo/srv/AddInts）
//   2. 调用 create_service() 创建服务端并绑定回调函数
//   3. 回调函数接收 "请求(Request)"，返回 "响应(Response)"
// ============================================================

#include "rclcpp/rclcpp.hpp"                           // ROS2 C++ 客户端库
#include "base_interfaces_demo/srv/add_ints.hpp"       // 自定义服务接口：AddInts

using base_interfaces_demo::srv::AddInts;               // 简化类型名

using std::placeholders::_1;   // 占位符1：对应回调函数中的 req 参数
using std::placeholders::_2;   // 占位符2：对应回调函数中的 res 参数

class MinimalService: public rclcpp::Node{
  public:
    MinimalService():Node("minimal_service"){
      // 【步骤1】创建服务端
      // 参数1：服务名称 "add_ints"（客户端通过此名称找到服务端）
      // 参数2：回调函数 add()，当客户端请求到达时自动调用
      //        使用 std::bind 绑定成员函数，_1 和 _2 分别对应 req 和 res
      server = this->create_service<AddInts>("add_ints",
        std::bind(&MinimalService::add, this, _1, _2));
      RCLCPP_INFO(this->get_logger(),"add_ints 服务端启动完毕，等待请求提交...");
    }
  private:
    rclcpp::Service<AddInts>::SharedPtr server;  // 服务端智能指针

    // 服务回调函数：处理客户端请求并填写响应
    // req：客户端发来的请求，包含 num1 和 num2 两个整数
    // res：要返回给客户端的响应，需要填入 sum 字段
    void add(const AddInts::Request::SharedPtr req,
             const AddInts::Response::SharedPtr res){
      res->sum = req->num1 + req->num2;          // 【关键】计算两数之和，写入响应
      RCLCPP_INFO(this->get_logger(),
        "请求数据:(%d,%d),响应结果:%d", req->num1, req->num2, res->sum);
    }
};

int main(int argc, char const *argv[])
{
  rclcpp::init(argc,argv);                      // 初始化 ROS2
  auto server = std::make_shared<MinimalService>();  // 创建服务端节点
  rclcpp::spin(server);                         // 进入事件循环，等待客户端请求
  rclcpp::shutdown();                           // 清理资源
  return 0;
}
