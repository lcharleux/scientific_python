from setuptools import setup
import argiope

setup(name='scientific_python',
      version=argiope.__version__,
      description="Science oriented python",
      long_description="",
      author='Ludovic Charleux, Emile Roux',
      author_email='ludovic.charleux@univ-smb.fr',
      license='GPL v3',
      packages=['dummy'],
      zip_safe=False,
      include_package_data=True,
      url='https://github.com/lcharleux/scientific_python',
      install_requires=[
          "numpy",
          "scipy",
          "matplotlib",
          "pandas",
          "jupyter",
          "nbconvert"
          ],
      )
