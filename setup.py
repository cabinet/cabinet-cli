from setuptools import setup

setup(
    name='cabinet-cli',
    version='0.1',
    py_modules=['cli'],
    include_package_data=True,
    install_requires=[
        'cabinet-cli',
    ],
    entry_points='''
        [console_scripts]
        cab=cli:cli
    ''',
)
