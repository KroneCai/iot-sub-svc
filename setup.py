from setuptools import setup, find_packages

setup(
    name="iot_sub_svc",
    version="0.1.0",
    packages=find_packages(),
    package_dir={"iot_sub_svc": "iot-sub-svc"},
    install_requires=[
        "paho-mqtt",
        "sqlalchemy",
        "cryptography",
    ],
    python_requires=">=3.6",
)