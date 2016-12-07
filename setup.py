from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='celmo',
      version='11.16',
      description='Common envelope light module',
      url='https://github.com/pablogalaviz/celmo',
      author='Pablo Galaviz',
      author_email='pablogalavizv@gmail.com',
      license='GPLv3',
      packages=['celmo','celmo.interface','celmo.io','celmo.data'],
      install_requires=[
          'argparse',
          'configparser',
          'ipywidgets',
          'logging',
          'numpy',
          'yt',
      ],
      scripts=['bin/celmo_cmd.py'],
      include_package_data=True,
      zip_safe=False)