import pydantic_pony
from setuptools import find_packages, setup


def read(f):
    return open(f, 'r', encoding='utf-8').read()


# https://pip.pypa.io/en/latest/user_guide/#fixing-conflicting-dependencies
INSTALL_REQUIREMENTS = read('requirements.txt').splitlines()

setup(
    name='pydantic-pony',
    version=pydantic_pony.__version__,
    description='Tools to generate Pydantic models from Pony ORM models.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/bali-framework/pydantic-pony',
    author='Josh.Yu',
    author_email='josh.yu_8@live.com',
    license='MIT',
    install_requires=INSTALL_REQUIREMENTS,
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(
        exclude=[
            'tests',
            'tests.*',
        ]
    ),
    include_package_data=True,
    zip_safe=False,
)
