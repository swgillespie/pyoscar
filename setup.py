try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="PyOscar",
      version='0.1',
      description='Python Oscar API bindings',
      author='Sean Gillespie',
      author_email='sean.william.g@gmail.com',
      url='https://github.com/swgillespie/pyoscar',
      py_modules=['pyoscar'],
      requires=['requests'],
      license='MIT',
      )