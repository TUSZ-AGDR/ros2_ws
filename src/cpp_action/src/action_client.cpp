// ============================================================
// action_client.cpp —— C++ 动作客户端
//
// 本程序演示如何使用 C++ 实现 ROS2 动作通信的客户端。
// 客户端向动作服务端发送目标（计算5阶斐波那契数列），
// 并注册三类回调来接收：目标响应、进度反馈、最终结果。
//
// 动作通信适合长时间任务，它的三个状态回调：
//   1. goal_response_callback  —— 服务端接受/拒绝了目标？
//   2. feedback_callback        —— 任务执行的实时进度如何？
//   3. result_callback          —— 任务成功/失败/被取消？最终结果是什么？
//
// 核心知识点：
//   1. 调用 rclcpp_action::create_client() 创建动作客户端
//   2. 调用 wait_for_action_server() 等待服务端就绪
//   3. 配置 SendGoalOptions 绑定三类回调
//   4. 调用 async_send_goal() 异步发送目标
// ============================================================

#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <base_interfaces_demo/action/fibonacci.hpp>

class FibonacciActionClient : public rclcpp::Node
{
public:
  using Fibonacci = base_interfaces_demo::action::Fibonacci;
  using GoalHandleFibonacci = rclcpp_action::ClientGoalHandle<Fibonacci>;

  FibonacciActionClient() : Node("fibonacci_action_client")
  {
    // 【步骤1】创建动作客户端，指定动作名称 "fibonacci"
    this->client_ptr_ = rclcpp_action::create_client<Fibonacci>(this, "fibonacci");
  }

  void send_goal(int order)
  {
    // 【步骤2】等待动作服务端上线（最多等待 5 秒）
    if (!this->client_ptr_->wait_for_action_server(std::chrono::seconds(5))) {
      RCLCPP_ERROR(this->get_logger(), "动作服务端未就绪");
      return;
    }

    // 构建目标消息
    auto goal_msg = Fibonacci::Goal();
    goal_msg.order = order;  // 设置要计算的斐波那契阶数
    RCLCPP_INFO(this->get_logger(), "发送目标，阶数: %d", order);

    // 【步骤3】配置三类回调函数
    auto send_goal_options = rclcpp_action::Client<Fibonacci>::SendGoalOptions();

    // 回调1：目标响应 —— 服务端接受了还是拒绝了我们的目标？
    send_goal_options.goal_response_callback =
      std::bind(&FibonacciActionClient::goal_response_callback, this,
                std::placeholders::_1);

    // 回调2：进度反馈 —— 任务执行过程中的实时进度更新
    send_goal_options.feedback_callback =
      std::bind(&FibonacciActionClient::feedback_callback, this,
                std::placeholders::_1, std::placeholders::_2);

    // 回调3：最终结果 —— 任务结束后（成功/失败/取消）接收最终状态
    send_goal_options.result_callback =
      std::bind(&FibonacciActionClient::result_callback, this,
                std::placeholders::_1);

    // 【步骤4】异步发送目标（不阻塞主线程）
    this->client_ptr_->async_send_goal(goal_msg, send_goal_options);
  }

private:
  rclcpp_action::Client<Fibonacci>::SharedPtr client_ptr_;

  // ---------- 回调1：目标响应回调 ----------
  // 服务端收到目标后立即回调，告知目标是否被接受
  void goal_response_callback(const GoalHandleFibonacci::SharedPtr & goal_handle)
  {
    if (!goal_handle) {
      RCLCPP_ERROR(this->get_logger(), "目标被拒绝");
    } else {
      RCLCPP_INFO(this->get_logger(), "目标已被接受");
    }
  }

  // ---------- 回调2：进度反馈回调 ----------
  // 服务端在执行过程中周期性地发布反馈，此回调接收并打印进度
  void feedback_callback(
    GoalHandleFibonacci::SharedPtr,
    const std::shared_ptr<const Fibonacci::Feedback> feedback)
  {
    RCLCPP_INFO(this->get_logger(), "收到反馈，当前序列长度: %zu",
                feedback->partial_sequence.size());
  }

  // ---------- 回调3：最终结果回调 ----------
  // 任务执行完毕后回调，告知最终状态（成功/取消/失败）和结果数据
  void result_callback(const GoalHandleFibonacci::WrappedResult & result)
  {
    switch (result.code) {
      case rclcpp_action::ResultCode::SUCCEEDED:
        RCLCPP_INFO(this->get_logger(), "任务成功，最终序列长度: %zu",
                    result.result->sequence.size());
        break;
      case rclcpp_action::ResultCode::CANCELED:
        RCLCPP_INFO(this->get_logger(), "任务被取消");
        break;
      default:
        RCLCPP_ERROR(this->get_logger(), "任务执行失败");
        break;
    }
    rclcpp::shutdown();  // 收到最终结果后关闭程序
  }
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto client = std::make_shared<FibonacciActionClient>();
  client->send_goal(5);   // 请求计算 5 阶斐波那契数列
  rclcpp::spin(client);   // 进入事件循环，等待回调触发
  rclcpp::shutdown();
  return 0;
}
