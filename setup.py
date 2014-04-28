from setuptools import setup, find_packages

setup(
    name='contact_potion',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Fabric==1.8.3',
        'Flask==0.10.1',
        'Flask-WTF==0.9.5',
        'Flask-Mail==0.9.0',
        'gunicorn==18.0',
        'honcho==0.5.0'
    ]
)
