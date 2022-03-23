from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='messagemap',
    version='0.0.2',
    description='MessageMap.IO Interface to API of deployed Environment',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    author='Ben Adams',
    author_email='ben@messagemap.io',
    keywords=['Message Queue', 'Messages'],
    url='https://github.com/MessageMap/py-messagemap',
    download_url='https://pypi.org/project/messagemap/'
)

install_requires = [ "requests" ]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
