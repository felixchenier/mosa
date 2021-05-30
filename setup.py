"""Setup tool for compiling the mosa module in a pip-accessible package."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("mosa/VERSION", "r") as fh:
    version = fh.read()


setuptools.setup(
    name='mosa',
    version=version,
    description=('Private module for the Mobility and Adaptive Sports '
                 'Research Lab.'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/felixchenier/mosa',
    author='Félix Chénier',
    author_email='chenier.felix@uqam.ca',
    license='Apache',
        license_files=['LICENSE.txt', 'NOTICE.txt'],
    packages=setuptools.find_packages(),
    package_data={
        'mosa': ['VERSION'],
    },
    project_urls={
        'Source': 'https://github.com/felixchenier/mosa/',
        'Tracker': 'https://github.com/felixchenier/mosa/issues',
    },
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.8',
)
