from setuptools import find_packages, setup

setup(
    name='bumger',
    version='1.0.0',
    description='App to manage a commom property maintenance',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask', 'Flask-WeasyPrint', 'num2words',
    ],
)
