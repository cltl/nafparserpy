from setuptools import setup, find_packages

setup(
    name='nafparserpy',
    version='0.1',
    description='python NAF parser',
    author='Sophie Arnoult',
    author_email='s.i.arnoult@vu.nl',
    packages=find_packages(include=['nafparserpy', 'nafparserpy.layers']),
    install_requires=[
        'lxml>=4.9.0'
    ],
    extras_require={
        'doc': ['pdoc3'],
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    package_data={'dtd': ['naf_v3.3.dtd']}
)

