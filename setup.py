from setuptools import find_packages, setup

setup(
    name='netbox_metrics',
    version='0.1',
    description='Custom Prometheus metrics for Netbox',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
