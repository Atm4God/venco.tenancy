from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in tenant_management_app/__init__.py
from tenant_management_app import __version__ as version

setup(
	name="tenant_management_app",
	version=version,
	description="A tenant management app",
	author="Akinola Marvellous",
	author_email="tmarvellous41@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
