from setuptools import find_packages, setup

package_name = 'bag_recorder_py'

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
    # entry_points（入口点）：定义可通过 ros2 run 启动的可执行程序
    #
    # 运行示例：
    #   ros2 run bag_recorder_py demo01_writer_py  → 启动录制器
    #   ros2 run bag_recorder_py demo02_reader_py  → 启动回放器
    # ============================================================
    entry_points={
        'console_scripts': [
            'demo01_writer_py = bag_recorder_py.demo01_writer_py:main',
            'demo02_reader_py = bag_recorder_py.demo02_reader_py:main',
        ],
    },
)
