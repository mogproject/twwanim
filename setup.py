import sys
from setuptools import setup, find_packages

SRC_DIR = 'src'

# read the contents of the README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()


def get_version():
    sys.path[:0] = [SRC_DIR]
    return __import__('twwanim').__version__


setup(
    name='twwanim',
    version=get_version(),
    description='Twin-width animation tools.',
    author='Yosuke Mizutani',
    author_email='mogproj@gmail.com',
    license='Apache 2.0 License',
    url='https://github.com/mogproject/twwanim',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'networkx >= 3.1',
        'manim >= 0.18.0',
    ],
    tests_require=[
    ],
    package_dir={'': SRC_DIR},
    packages=find_packages(SRC_DIR),
    include_package_data=True,
    test_suite='tests',
    entry_points={
        'console_scripts': ['twwanim = twwanim.twwanim:run_main']
    }
)
