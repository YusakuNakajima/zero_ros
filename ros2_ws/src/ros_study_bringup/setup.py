from glob import glob
import os

from setuptools import setup

package_name = "ros_study_bringup"


def package_files(directory):
    return glob(os.path.join(directory, "**", "*"), recursive=True)


setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), package_files("config")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Yusaku Nakajima",
    maintainer_email="yusaku_nakajima@ap.eng.osaka-u.ac.jp",
    description="Bringup launch files and controller configuration for the zero_ros slides.",
    license="CC-BY-NC-ND-4.0",
)
