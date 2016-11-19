from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='elopic',
    version='0.0.1',
    description='Rank your picture collection',
    long_description=readme,
    author='Matthias Manhertz',
    author_email='m@nhertz.de',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

