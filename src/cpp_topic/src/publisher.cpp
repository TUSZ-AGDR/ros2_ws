// ============================================================
// publisher.cpp —— C++ 话题发布者
//
// 本程序演示 ROS2 中最基本的通信模型：话题（Topic）通信
// 发布者（Publisher）以每秒一次的频率向名为 "chatter" 的话题
// 发布 String 类型消息，消息内容为 "Hello ROS2: " + 递增计数器
//
// 核心知识点：
//   1. 继承 rclcpp::Node 创建自定义节点
//   2. 调用 create_publisher() 创建发布者
//   3. 调用 create_wall_timer() 创建定时器驱动发布
//   4. 调用 publish() 发布消息到话题
//   5. rclcpp::spin() 让节点持续运行
// ============================================================

#include "rclcpp/rclcpp.hpp"         // ROS2 C++ 客户端库头文件
#include "std_msgs/msg/string.hpp"   // 标准消息类型：字符串

using namespace std::chrono_literals; // 允许使用 1s 这种字面量表示时间

// 自定义发布者节点类，继承自 rclcpp::Node
class MinimalPublisher : public rclcpp::Node
{
public:
  // 构造函数：初始化节点名称为 "minimal_publisher"，计数器从 0 开始
  MinimalPublisher() : Node("minimal_publisher"), count_(0)
  {
    // 【步骤1】创建发布者
    // 参数1：话题名称 "chatter"
    // 参数2：消息队列长度 10（用于缓存待发送的消息）
    publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);

    // 【步骤2】创建定时器，每隔 1 秒调用一次 timer_callback() 函数
    // std::bind 用于将类的成员函数绑定为回调函数
    timer_ = this->create_wall_timer(1s, std::bind(&MinimalPublisher::timer_callback, this));
  }

private:
  // 定时器回调函数：每隔 1 秒自动被调用一次
  void timer_callback()
  {
    auto msg = std_msgs::msg::String();                          // 创建一条 String 消息
    msg.data = "Hello ROS2: " + std::to_string(count_++);        // 填入消息内容（带递增计数）
    RCLCPP_INFO(this->get_logger(), "发布: '%s'", msg.data.c_str()); // 打印日志到终端
    publisher_->publish(msg);                                    // 【关键】发布消息到话题
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_; // 发布者智能指针
  rclcpp::TimerBase::SharedPtr timer_;                            // 定时器智能指针
  size_t count_;                                                  // 消息计数器
};

// 主函数：ROS2 程序的入口点
int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);                               // 【步骤1】初始化 ROS2 客户端库
  rclcpp::spin(std::make_shared<MinimalPublisher>());     // 【步骤2】创建节点实例并进入事件循环
  rclcpp::shutdown();                                     // 【步骤3】程序退出前清理资源
  return 0;
}
