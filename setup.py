from setuptools import setup

setup(name="akdev_compiler",
      version='1.0',
      description='Compiler design tools of https://akdev.ir',
      url='https://github.com/amirkabiri/regex-engine',
      author='Amir Kabiri',
      author_email='akabiridev@gmail.com',
      license='MIT',
      packages=['akdev_compiler'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
