from setuptools import setup, find_packages
import os

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='dataloader',
      version='0.1.1',
      description='data loader',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/janclemenslab/dataloader',
      author='Jan Clemens',
      author_email='clemensjan@googlemail.com',
      license='MIT',
      # py_modules=['dataloader', 'dataloadercfg'],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=['pyyaml'],
      tests_require=['nose'],
      test_suite='nose.collector',
      package_data={'dataloader.config': ['default.yaml'],},
      include_package_data=True,
      zip_safe=False
      )
