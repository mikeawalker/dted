
from setuptools import setup 
__version__ = "0.0.0"


setup( 
    name='dted', 
    version=__version__, 
    description='A package for working with  Digital Terrain Elevation Data (DTED)', 
    author='Mike Walker', 
    author_email='mike.walker', 
    packages=['src/dted'], 
    install_requires=[ 
        'numpy',  
        "matplotlib",
        "scipy"
    ], 
) 