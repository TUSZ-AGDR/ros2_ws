cmake_minimum_required(VERSION 3.8)
project(base_interfaces_demo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# 导入 ROS2 接口生成工具，用于将 .srv 和 .action 文件编译为各语言可用的代码
find_package(rosidl_default_generators REQUIRED)

# ============================================================
# 生成自定义接口：将 .srv 和 .action 的定义编译为 C++ / Python 代码
# 编译后，其他功能包即可通过依赖本包来使用这些自定义消息类型
# ============================================================
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/AddInts.srv"                # 服务接口：两整数相加
  "action/Fibonacci.action"        # 动作接口：斐波那契数列计算
)

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

ament_package()
