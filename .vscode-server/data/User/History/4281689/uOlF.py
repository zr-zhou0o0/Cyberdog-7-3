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
            'move_x = learning.move_x:main',
            'keeper = learning.keeper:main',
            'track = learning.track:main',
            'data_receive = learning.data_receive:main'
        ],
    },
)
