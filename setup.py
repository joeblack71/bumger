from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='bumger',
    version='1.0.0',
    author='Johnny A. Olivas'
    author_email='jolivas71@hotmail.com'
    description='Manage monthly receipts and payments for building maintenance',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: Ubuntu Xenial 16.0.4"
    )
    install_requires=[
        'flask', 'Flask-WeasyPrint', 'num2words',
    ],
)
