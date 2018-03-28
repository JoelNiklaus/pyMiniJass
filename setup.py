from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

    setup(
        name='pyMiniJass',
        version='0.0.1',
        description='pyMiniJass is a minified version of the Schieber Jass game.',
        long_description=readme,
        author='Samuel Kurath',
        author_email='samuel.kurath@gmail.com',
        url='https://github.com/Murthy10/pyMiniJass',
        license='MIT',
        packages=find_packages(exclude=('tests', 'docs')),
        scripts=['bin/pyMiniJass'],
    )
