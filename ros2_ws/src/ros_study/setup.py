from setuptools import find_packages, setup
import os
import glob
package_name = 'ros_study'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob.glob(os.path.join('launch', '*launch.py'))),
        (os.path.join('share', package_name, 'urdf'), glob.glob(os.path.join('urdf', '**', '*'), recursive=True)),
        (os.path.join('share', package_name, 'meshes'), glob.glob(os.path.join('meshes', '**', '*'), recursive=True)),
        (os.path.join('share', package_name, 'config'), glob.glob(os.path.join('config', '**', '*'), recursive=True)),
        (os.path.join('share', package_name, 'rviz'), glob.glob(os.path.join('rviz', '*.rviz'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'jtc_demo = ros_study.jtc_demo:main',
            'jtc_velocity_accel_demo = ros_study.jtc_velocity_accel_demo:main',
            'jtc_with_ik_demo = ros_study.jtc_with_ik_demo:main',
            'marker_display_demo = ros_study.marker_display_demo:main',
            'tf_display_demo = ros_study.tf_display_demo:main',
            'admittance_demo = ros_study.admittance_demo:main',
        ],
    },
)
