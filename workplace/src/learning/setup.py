from setuptools import setup

package_name = 'learning'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mi',
    maintainer_email='mi@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'stand = learning.stand:main',
            'data_receive = learning.data_receive:main',
            'get_data = learning.get_data',
            'camera = learning.camera:main',
            'rgb_cam_suber = learning.rgb_cam_suber',
            'line_left = learning.line_left:main',
            'track = learning.track:main',
            'move_horizontal = learning.move_horizontal:main',
            'keeper = learning.keeper:main'
        ],
    },
)
