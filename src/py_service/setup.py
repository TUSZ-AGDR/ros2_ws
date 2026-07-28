from setuptools import find_packages, setup

package_name = 'py_service'

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
    # entry_points（入口点）：定义可以通过 ros2 run 启动的可执行程序
    #
    # 运行示例：
    #   ros2 run py_service server    → 启动服务端
    #   ros2 run py_service client 3 5 → 启动客户端，请求计算 3+5
    # ============================================================
    entry_points={
        'console_scripts': [
            'server = py_service.server:main',
            'client = py_service.client:main'
        ],
    },
)
