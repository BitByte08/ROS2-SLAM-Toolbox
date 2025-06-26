from setuptools import find_packages, setup

package_name = 'encoder_broadcaster'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/static_laser_tf.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bitbyte08',
    maintainer_email='bitbyte08@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'static_odom_tf_node = encoder_broadcaster.static_odom_tf_node:main'
        ],
    },
)
