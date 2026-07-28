// ============================================================
// action_server.cpp —— C++ 动作服务端
//
// 本程序演示 ROS2 的第三种通信模型：动作（Action）通信
// 动作是服务的高级形式，适用于"长时间运行的任务"，支持：
//   1. 提交任务目标（Goal）
//   2. 执行过程中实时反馈进度（Feedback）
//   3. 任务完成后返回最终结果（Result）
//   4. 随时取消正在执行的任务（Cancel）
//
// 本例实现一个"斐波那契数列计算器"：
//   客户端指定阶数(如 10) → 服务端逐项计算 →
//   每计算一项就反馈当前序列 → 全部完成后返回完整序列
//
// 核心知识点：
//   1. 使用 rclcpp_action::create_server() 创建动作服务端
//   2. 绑定三类回调：handle_goal（接收目标）、handle_cancel（处理取消）、
//      handle_accepted（启动执行线程）
//   3. 在独立线程中执行耗时任务，通过 publish_feedback() 发布反馈
//   4. 通过 succeed() / canceled() 通知客户端任务最终状态
// ============================================================

#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <base_interfaces_demo/action/fibonacci.hpp>

class FibonacciActionServer : public rclcpp::Node
{
public:
  // 类型别名，简化后续书写
  using Fibonacci = base_interfaces_demo::action::Fibonacci;
  using GoalHandleFibonacci = rclcpp_action::ServerGoalHandle<Fibonacci>;

  FibonacciActionServer() : Node("fibonacci_action_server")
  {
    // 【步骤1】创建动作服务端，绑定三类回调函数
    //   回调1：handle_goal    —— 收到新目标时调用，决定接受还是拒绝
    //   回调2：handle_cancel  —— 收到取消请求时调用，决定是否允许取消
    //   回调3：handle_accepted —— 目标被接受后调用，在此启动实际计算任务
    this->action_server_ = rclcpp_action::create_server<Fibonacci>(
      this,
      "fibonacci",
      std::bind(&FibonacciActionServer::handle_goal, this,
                std::placeholders::_1, std::placeholders::_2),
      std::bind(&FibonacciActionServer::handle_cancel, this,
                std::placeholders::_1),
      std::bind(&FibonacciActionServer::handle_accepted, this,
                std::placeholders::_1));
  }

private:
  rclcpp_action::Server<Fibonacci>::SharedPtr action_server_;

  // ---------- 回调1：处理新目标请求 ----------
  // 返回值决定是否接受该任务目标
  rclcpp_action::GoalResponse handle_goal(
    const rclcpp_action::GoalUUID & uuid,
    std::shared_ptr<const Fibonacci::Goal> goal)
  {
    RCLCPP_INFO(this->get_logger(), "收到目标，阶数: %d", goal->order);
    (void)uuid;  // 不使用 uuid，显式标记以避免编译器警告
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;  // 接受并立即执行
  }

  // ---------- 回调2：处理取消请求 ----------
  // 返回值决定是否允许取消
  rclcpp_action::CancelResponse handle_cancel(
    const std::shared_ptr<GoalHandleFibonacci> goal_handle)
  {
    RCLCPP_INFO(this->get_logger(), "收到取消请求");
    (void)goal_handle;
    return rclcpp_action::CancelResponse::ACCEPT;  // 接受取消请求
  }

  // ---------- 回调3：目标被接受后，启动新线程执行任务 ----------
  // 使用独立线程避免阻塞 ROS2 的主事件循环
  void handle_accepted(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
  {
    // std::thread 创建并分离线程（detach 后线程在后台独立运行）
    std::thread{
      std::bind(&FibonacciActionServer::execute, this, std::placeholders::_1),
      goal_handle
    }.detach();
  }

  // ---------- 核心执行逻辑：在独立线程中计算斐波那契数列 ----------
  void execute(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
  {
    const auto goal = goal_handle->get_goal();
    auto feedback = std::make_shared<Fibonacci::Feedback>();  // 反馈消息
    auto result = std::make_shared<Fibonacci::Result>();       // 最终结果

    // 斐波那契数列初始化：前两项为 0 和 1
    int a = 0, b = 1;
    feedback->partial_sequence.push_back(a);
    feedback->partial_sequence.push_back(b);

    rclcpp::Rate loop_rate(1);  // 控制每秒发布一次反馈

    for (int i = 2; i < goal->order; ++i) {

      // 【重要】每轮循环检查是否收到了取消请求
      if (goal_handle->is_canceling()) {
        result->sequence = feedback->partial_sequence;     // 保存当前已计算的结果
        goal_handle->canceled(result);                     // 通知客户端：任务已取消
        RCLCPP_INFO(this->get_logger(), "目标已取消");
        return;
      }

      // 计算下一个斐波那契数
      int next = a + b;
      a = b;
      b = next;
      feedback->partial_sequence.push_back(next);

      // 发布进度反馈，通知客户端当前计算到哪儿了
      goal_handle->publish_feedback(feedback);
      RCLCPP_INFO(this->get_logger(), "发布反馈，当前序列长度: %zu",
                  feedback->partial_sequence.size());

      loop_rate.sleep();  // 休眠以维持 1Hz 的反馈频率
    }

    // 任务完成：将最终结果通过 succeed() 发送给客户端
    if (rclcpp::ok()) {
      result->sequence = feedback->partial_sequence;
      goal_handle->succeed(result);
      RCLCPP_INFO(this->get_logger(), "目标执行完成");
    }
  }
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<FibonacciActionServer>());  // 创建服务端并进入循环
  rclcpp::shutdown();
  return 0;
}
