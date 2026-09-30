from setuptools import setup

setup(
    name="bodhi-script",
    version="0.1.0",
    packages=["interpreter"],
    entry_points={
        "console_scripts": [
            "bodhi=interpreter.bodhi:main",
        ],
    },
)