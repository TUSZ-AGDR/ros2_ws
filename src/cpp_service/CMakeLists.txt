cmake_minimum_required(VERSION 3.8)
project(cpp_service)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)               # ROS2 C++ 客户端库
find_package(base_interfaces_demo REQUIRED) # 自定义接口包（包含 AddInts 服务定义）

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
# 编译 server 可执行文件：服务端，提供两数相加的功能
# ============================================================
add_executable(server src/server.cpp)
ament_target_dependencies(server rclcpp base_interfaces_demo)

# ============================================================
# 编译 client 可执行文件：客户端，向服务端发送请求
# ============================================================
add_executable(client src/client.cpp)
ament_target_dependencies(client rclcpp base_interfaces_demo)

# 将生成的可执行文件安装到 lib/<包名> 目录
install(TARGETS
  server
  client
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
