cmake_minimum_required(VERSION 3.8)
project(cpp_action)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)               # ROS2 C++ 客户端库
find_package(rclcpp_action REQUIRED)        # ROS2 动作通信库
find_package(base_interfaces_demo REQUIRED) # 自定义接口（包含 Fibonacci 动作定义）

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# ============================================================
# 编译 action_server 可执行文件：动作服务端，提供斐波那契计算
# ============================================================
add_executable(action_server src/action_server.cpp)
ament_target_dependencies(action_server rclcpp rclcpp_action base_interfaces_demo)

# ============================================================
# 编译 action_client 可执行文件：动作客户端，请求计算斐波那契
# ============================================================
add_executable(action_client src/action_client.cpp)
ament_target_dependencies(action_client rclcpp rclcpp_action base_interfaces_demo)

# 将生成的可执行文件安装到 lib/<包名> 目录
install(TARGETS
  action_server
  action_client
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
