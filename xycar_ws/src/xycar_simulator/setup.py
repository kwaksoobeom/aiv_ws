from setuptools import setup

package_name = 'xycar_simulator'

setup(
    name=package_name,
    version='0.1.0',
    py_modules=['pygame_gui', 'reeds_shepp'],
    package_dir={'': 'scripts'},
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=[],
    zip_safe=True,
    maintainer='kwaksoobeom',
    maintainer_email='soobeom@example.com',
    description='Parking simulator using Pygame and Reeds-Shepp path',
    license='MIT',
    entry_points={
        'console_scripts': [
            'xycar_gui = pygame_gui:main',
        ],
    },
)
