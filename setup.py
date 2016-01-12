from setuptools import find_packages, setup

setup(name ='wmg-strowger',
      version='0.1',
      author='CMRF',
      packages=find_packages(),
      install_requires = [
          'nose',
          'sqlalchemy'
      ]
  )

