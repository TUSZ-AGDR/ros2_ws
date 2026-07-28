from setuptools import find_packages, setup

package_name = 'py_topic'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robot',
    maintainer_email='maintainer@example.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    # ============================================================
    # entry_points（入口点）：定义可以通过 ros2 run 命令启动的可执行程序
    #
    # 格式：'可执行文件名 = 包名.模块名:函数名'
    # 安装后运行示例：
    #   ros2 run py_topic publisher
    #   ros2 run py_topic subscriber
    # ============================================================
    entry_points={
        'console_scripts': [
            # publisher 可执行文件 → 调用 py_topic.publisher 模块中的 main() 函数
            'publisher = py_topic.publisher:main',
            # subscriber 可执行文件 → 调用 py_topic.subscriber 模块中的 main() 函数
            'subscriber = py_topic.subscriber:main'
        ],
    },
)
