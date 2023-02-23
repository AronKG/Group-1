from setuptools import setup, find_packages

setup(
    name='my_flask_app',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      'Flask==2.2.2',
      'flask-socketio==5.3.2'
    ],
    entry_points={
        'console_scripts': [
            'my_flask_app=my_flask_app.app:main'
        ]
    },
    classifiers=[
        'Development Status :: v0.1.1',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
