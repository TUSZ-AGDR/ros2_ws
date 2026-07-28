// ============================================================
// param_demo.cpp —— C++ 参数演示
//
// 本程序演示 ROS2 的参数（Parameter）机制。
// 参数是节点的"配置变量"，可以在运行时动态读取和修改。
//
// 参数的特点：
//   1. 每个节点可以声明自己的参数（参数名 + 默认值）
//   2. 参数值可以在运行时通过命令行工具动态修改
//   3. 节点可以通过 get_parameter() 随时读取最新的参数值
//
// 使用方法：
//   启动节点：  ros2 run cpp_param param_demo
//   查看参数：  ros2 param list
//   读取参数：  ros2 param get /param_demo_node robot_name
//   动态修改：  ros2 param set /param_demo_node robot_name "my_robot"
//
// 核心知识点：
//   1. 调用 declare_parameter() 声明参数并设置默认值
//   2. 调用 get_parameter() 读取参数值
//   3. 参数支持多种类型：int、double、string、bool、数组等
// ============================================================

#include "rclcpp/rclcpp.hpp"

class ParamDemoNode : public rclcpp::Node
{
public:
  ParamDemoNode() : Node("param_demo_node")
  {
    // 【步骤1】声明参数
    // 参数1：参数名称 "robot_name"
    // 参数2：默认值 "robot_01"（如果用户从未修改过，就使用此值）
    // 模板参数 <std::string> 指定参数类型
    this->declare_parameter<std::string>("robot_name", "robot_01");

    // 【步骤2】读取参数值
    // get_parameter("参数名") 返回一个 Parameter 对象
    // .as_string() 将参数值转换为 string 类型
    std::string robot_name = this->get_parameter("robot_name").as_string();
    RCLCPP_INFO(this->get_logger(), "初始 robot_name 参数值: %s",
                robot_name.c_str());

    // 【步骤3】创建定时器每秒读取一次参数
    // 这样当用户在终端用 ros2 param set 修改参数后，
    // 下一轮回调就能读取到新值，验证参数的动态修改效果
    timer_ = this->create_wall_timer(
      std::chrono::seconds(1),
      std::bind(&ParamDemoNode::timer_callback, this));
  }

private:
  rclcpp::TimerBase::SharedPtr timer_;

  void timer_callback()
  {
    // 每次回调都重新读取参数，获取最新值
    std::string robot_name = this->get_parameter("robot_name").as_string();
    RCLCPP_INFO(this->get_logger(), "当前 robot_name 参数值: %s",
                robot_name.c_str());
  }
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ParamDemoNode>());  // 创建节点并进入循环
  rclcpp::shutdown();
  return 0;
}
