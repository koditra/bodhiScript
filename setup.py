from setuptools import setup

setup(
    name="bodhiscript",
    version="0.1.3",
    description="BodhiScript interpreter",
    long_description=(
        "A tiny interpreted language inspired by Hindi and Sanskrit that uses Java-like syntax."
    ),
    long_description_content_type="text/plain",
    author="bodhiScript contributors",
    url="https://github.com/koditra/bodhiScript",
    license="MIT",
    python_requires=">=3.8",
    package_dir={"": "interpreter"},
    py_modules=["bodhi"],
    entry_points={
        "console_scripts": [
            "bodhi=bodhi:main",
        ]
    },
)