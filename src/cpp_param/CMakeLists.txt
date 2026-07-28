cmake_minimum_required(VERSION 3.8)
project(cpp_param)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)     # ROS2 C++ 客户端库（参数功能内置其中）

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
# 编译 param_demo 可执行文件：演示参数的声明、读取与动态修改
# ============================================================
add_executable(param_demo src/param_demo.cpp)
ament_target_dependencies(param_demo rclcpp)

# 将生成的可执行文件安装到 lib/<包名> 目录
install(TARGETS
  param_demo
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
