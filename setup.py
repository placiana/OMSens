#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__ = """
This file is part of OpenModelica.
Copyright (c) 1998-CurrentYear, Open Source Modelica Consortium (OSMC),
c/o Linköpings universitet, Department of Computer and Information Science,
SE-58183 Linköping, Sweden.

All rights reserved.

THIS PROGRAM IS PROVIDED UNDER THE TERMS OF GPL VERSION 3 LICENSE OR
THIS OSMC PUBLIC LICENSE (OSMC-PL) VERSION 1.2.
ANY USE, REPRODUCTION OR DISTRIBUTION OF THIS PROGRAM CONSTITUTES
RECIPIENT'S ACCEPTANCE OF THE OSMC PUBLIC LICENSE OR THE GPL VERSION 3,
ACCORDING TO RECIPIENTS CHOICE.

The OpenModelica software and the Open Source Modelica
Consortium (OSMC) Public License (OSMC-PL) are obtained
from OSMC, either from the above address,
from the URLs: http://www.ida.liu.se/projects/OpenModelica or
http://www.openmodelica.org, and in the OpenModelica distribution.
GNU version 3 is obtained from: http://www.gnu.org/copyleft/gpl.html.

This program is distributed WITHOUT ANY WARRANTY; without
even the implied warranty of  MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE, EXCEPT AS EXPRESSLY SET FORTH
IN THE BY RECIPIENT SELECTED SUBSIDIARY LICENSE CONDITIONS OF OSMC-PL.

See the full OSMC Public License conditions for more details.
"""
__author__ = "Adeel Asghar, adeel.asghar@liu.se"
__maintainer__ = "https://openmodelica.org"
__status__ = "Production"

from setuptools import setup, find_packages
import os
import sys
from shutil import which
from subprocess import call


def build_python_binaries():
    try:
        omhome = os.path.split(os.path.split(os.path.realpath(which("omc")))[0])[0]
    except BaseException:
        omhome = None
    omhome = omhome or os.environ.get('OPENMODELICAHOME')
    
    if omhome is None:
        raise Exception("Failed to find OPENMODELICAHOME (searched for environment variable as well as the omc executable)")
    
    try:
        # Compile CURVI files
        if 0 != call(["gfortran", "-fPIC", "-c", "Rutf.for", "Rut.for", "Curvif.for"], cwd="omsens/fortran_interface"):
            raise Exception("Failed to compile CURVI files.")
        print("CURVI files compiled.")
        
        # Generate CURVIF python binary
        f2py_call = call(["f2py3", "-c", "-I.", "Curvif.o", "Rutf.o", "Rut.o", "-m", "curvif_simplified", "curvif_simplified.pyf", "Curvif_simplified.f90"], cwd="omsens/fortran_interface")
        if 0 != f2py_call:
            raise Exception("Failed to generate CURVIF python binary.")
        print("Generated CURVIF python binary.")
    except ImportError:
        print("Error installing OMSens.")


if 'sdist' not in sys.argv and 'egg_info' not in sys.argv:
    build_python_binaries()

setup(name='OMSens-placiana',
      python_requires='>=3.6',
      version='1.0.7',
      description='OpenModelica sensitivity analysis and optimization module',
      author='Rodrigo Castro',
      author_email='rcastro@dc.uba.ar',
      maintainer='Adeel Asghar',
      maintainer_email='adeel.asghar@liu.se',
      license="BSD, OSMC-PL 1.2, GPL (user's choice)",
      url='http://openmodelica.org/',
      install_requires=[
          'wheel',
          'six',
          'pytest',
          'matplotlib',
          'numpy',
          'pandas'
      ],
      # package_dir={'': 'omsens'},
      packages=find_packages('.'),
      zip_safe=False,
      include_package_data=True,
      package_data={
        "": ["omsens/fortran_interface/*.so"],
      }
)

