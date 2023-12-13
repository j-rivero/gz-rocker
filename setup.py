import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gz-rocker",
    version="0.0.1",
    packages=setuptools.find_packages(),
    package_data={'gz_rocker': ['templates/*.em']},
    author="Ashton Larkin, Jose Luis Rivero",
    author_email="42042756+adlarkin@users.noreply.github.com, jrivero@openrobotics.org",
    description="Plugins for rocker that enable the use of Gazebo libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/j-rivero/gz-rocker",
    license='Apache 2.0',
    install_requires=[
        'rocker',
    ],
    entry_points={
        'rocker.extensions': [
            'gazebo = gz_rocker.gazebo:Gazebo',
            'vol = gz_rocker.vol:Vol',
        ]
    }
)
