import versioneer
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('requirements.txt') as requirements_file:
    reqs = requirements_file.readlines()
REQUIREMENTS = [r.split('==')[0] for r in reqs] # lets the mamba solver solve versions


setup(
    name='jsonschema2md',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="Apache",
    description='Convert JSON Schemas to simple, human-readable Markdown documentation.',
    author="Ralf Gabriels",
    url='https://github.com/RalfG/jsonschema2md',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=REQUIREMENTS,
    keywords=["jsonschema2md", "JSON Schema", "Markdown", "Converter", "Parser", "Documentation"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
    ]
)