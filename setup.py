from setuptools import setup

setup(
    name="bodhi-script",
    version="0.1.1",
    py_modules=["bodhi"],
    entry_points={
        "console_scripts": [
            "bodhi=bodhi:main",
        ],
    },
)