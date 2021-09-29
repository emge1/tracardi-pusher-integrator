from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-pusher-integrator',
    version='0.1',
    description='The purpose of this plugin is to connect Tracardi with Pusher Beams.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Marcin Gaca',
    author_email='emygeq@gmail.com',
    packages=['tracardi_pusher_integrator'],
    install_requires=[
        'pydantic',
        'tracardi_plugin_sdk',
        'pusher_push_notifications',
        'aiohttp',
        'tracardi'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords=['tracardi', 'plugin'],
    include_package_data=True,
    python_requires=">=3.8",
)
