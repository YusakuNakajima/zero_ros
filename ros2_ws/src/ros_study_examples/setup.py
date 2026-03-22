from setuptools import find_packages, setup

package_name = "ros_study_examples"


setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Yusaku Nakajima",
    maintainer_email="yusaku_nakajima@ap.eng.osaka-u.ac.jp",
    description="Canonical ROS 2 Python examples for the zero_ros slides.",
    license="CC-BY-NC-ND-4.0",
    entry_points={
        "console_scripts": [
            "jtc_demo = ros_study_examples.jtc_demo:main",
            "jtc_velocity_accel_demo = ros_study_examples.jtc_velocity_accel_demo:main",
            "jtc_with_ik_demo = ros_study_examples.jtc_with_ik_demo:main",
            "marker_display_demo = ros_study_examples.marker_display_demo:main",
            "tf_display_demo = ros_study_examples.tf_display_demo:main",
            "admittance_demo = ros_study_examples.admittance_demo:main",
        ],
    },
)
