from distutils.core import setup

# Enables automatic conversion to Python 3.x code if needed.
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

setup(
    name='cvxpy',
    version='0.1',
    author='Steven Diamond, Eric Chu, Stephen Boyd',
    author_email='stevend2@stanford.edu, echu508@stanford.edu, boyd@stanford.edu',
    packages=[  'cvxpy',
                'cvxpy.atoms',
                'cvxpy.atoms.elementwise',
                'cvxpy.atoms.nonlinear',
                'cvxpy.constraints',
                'cvxpy.expressions',
                'cvxpy.expressions.constants',
                'cvxpy.expressions.variables',
                'cvxpy.interface',
                'cvxpy.interface.numpy_interface',
                'cvxpy.interface.cvxopt_interface',
                'cvxpy.problems',
                'cvxpy.tests',
                'cvxpy.utilities'],
    package_dir={'cvxpy': 'cvxpy'},
        url='http://github.com/cvxgrp/cvxpy/',
    license='...',
    description='A domain-specific language for modeling convex optimization problems in Python.',
    long_description=open('README.md').read(),
    requires = ["cvxopt(>= 1.1.6)",
                "ecos(>=1.0)"], # this doesn't appear to do anything unfortunately
    cmdclass = {'build_py' : build_py}
)
