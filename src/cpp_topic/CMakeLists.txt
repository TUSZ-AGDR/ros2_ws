cmake_minimum_required(VERSION 3.8)
project(cpp_topic)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)     # ROS2 C++ 客户端库
find_package(std_msgs REQUIRED)   # 标准消息类型（包含 std_msgs/msg/String）

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
# 编译 publisher 可执行文件
# add_executable(输出文件名, 源文件路径)
# ============================================================
add_executable(publisher src/publisher.cpp)
# 为 publisher 目标链接所需的依赖库（rclcpp 和 std_msgs）
ament_target_dependencies(publisher rclcpp std_msgs)

# ============================================================
# 编译 subscriber 可执行文件
# ============================================================
add_executable(subscriber src/subscriber.cpp)
# 为 subscriber 目标链接所需的依赖库
ament_target_dependencies(subscriber rclcpp std_msgs)

# ============================================================
# 将生成的可执行文件安装到 lib/<包名> 目录
# 这样 ros2 run 命令才能找到并执行它们
# ============================================================
install(TARGETS
  publisher
  subscriber
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
