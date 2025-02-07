from setuptools import setup

package_name = 'proyecto_master_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='snowartz',
    maintainer_email='snowartz@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['master = proyecto_master_pkg.master:main',
                            'navigation = proyecto_master_pkg.navigation_test:main',
                            'manipulation = proyecto_master_pkg.manipulation_test:main',
                            'perception = proyecto_master_pkg.perception_test:main',
                            'control = proyecto_master_pkg.robot_controller:main',
                            'camara = proyecto_master_pkg.NodoCamara:main',
        ],
    },
)
