from setuptools import setup, find_packages

setup(
    name="fdm_lid_driven_cavity_flow",
    version="0.0.1",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
