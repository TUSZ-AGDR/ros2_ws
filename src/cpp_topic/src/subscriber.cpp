// ============================================================
// subscriber.cpp —— C++ 话题订阅者
//
// 本程序演示 ROS2 话题通信的接收端。
// 订阅者（Subscriber）持续监听名为 "chatter" 的话题，
// 一旦有消息到达，就通过回调函数打印消息内容。
//
// 核心知识点：
//   1. 调用 create_subscription() 创建订阅者
//   2. 注册回调函数处理接收到的消息
//   3. 订阅者和发布者通过相同的话题名称 "chatter" 建立联系
// ============================================================

#include "rclcpp/rclcpp.hpp"         // ROS2 C++ 客户端库头文件
#include "std_msgs/msg/string.hpp"   // 标准消息类型：字符串

// 自定义订阅者节点类，继承自 rclcpp::Node
class MinimalSubscriber : public rclcpp::Node
{
public:
  // 构造函数：初始化节点名称为 "minimal_subscriber"
  MinimalSubscriber() : Node("minimal_subscriber")
  {
    // 【步骤1】创建订阅者
    // 参数1：要订阅的话题名称 "chatter"（与发布者的话题名一致才能收到消息）
    // 参数2：消息队列长度 10
    // 参数3：消息到达时的回调函数 topic_callback
    //        std::placeholders::_1 是回调函数参数 msg 的占位符
    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "chatter", 10, std::bind(&MinimalSubscriber::topic_callback, this, std::placeholders::_1));
  }

private:
  // 消息回调函数：每当订阅的话题上有新消息到达，此函数自动被调用
  // 参数 msg：指向接收到的消息的共享指针
  void topic_callback(const std_msgs::msg::String::SharedPtr msg) const
  {
    RCLCPP_INFO(this->get_logger(), "接收: '%s'", msg->data.c_str()); // 打印接收到的消息内容
  }

  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_; // 订阅者智能指针
};

// 主函数：ROS2 程序的入口点
int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);                              // 初始化 ROS2 客户端库
  rclcpp::spin(std::make_shared<MinimalSubscriber>());   // 创建订阅节点并进入事件循环（阻塞等待消息）
  rclcpp::shutdown();                                    // 清理资源
  return 0;
}
