from setuptools import setup, find_packages  # Always prefer setuptools over distutils


setup(
    name='pymainichigo',
    version='1.0.2',

    description='Wallpaper generator for Go/Baduk/Weiqi positions',
    long_description='Generates and sets your wallpaper to a daily Go game, ' +
                     'with each move spaced out over the course of a whole day',

    url='https://github.com/apetresc/pymainichigo',

    author='Adrian Petrescu',
    author_email='apetresc@gmail.com',

    license='GPL',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(exclude=['test*']),

    install_requires=[
        'sgf==0.5',
        'pyyaml==3.12',
        'xvfbwrapper==0.2.9',
        'Jinja2==2.9.6',
        'feedparser==5.2.1',
        'requests==2.18.4'
    ],

    package_data={'pymainichigo': ['goban.pde.template', 'test.sgf']},

    entry_points={
        "console_scripts": [
            'pymainichigo=pymainichigo.main:main'
        ]
    },
)
