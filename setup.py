import sys

# dirty hack, always use wheel
sys.argv.append('bdist_wheel')

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='python-permissions',
    version='0.1',
    description='Extension to simplify the way how to deal with user groups and permissions per group for users',
    long_description=readme(),
    classifiers=[
        'Development Status :: 0.1 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Topic :: Permissions',
    ],
    url='https://github.com/sergeyglazyrindev/permissions-module',
    author='Sergey Glazyrin',
    author_email='sergey.glazyrin.dev@gmail.com',
    license='MIT',
    package_dir={'': 'src'},
    packages=['permissions', ],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': ['nose', 'mock'],
    },
    test_suite='tests',
    install_requires=['redis==2.10.3', 'redis-beautified-ext==0.1'],
    dependency_links=['https://github.com/sergeyglazyrindev/redissimplified/blob/master#egg=redis-beautified-ext==0.1']
)
