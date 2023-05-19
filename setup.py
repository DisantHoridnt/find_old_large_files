from setuptools import setup, find_packages

setup(
    name="find_old_large_files",
    version="0.3.0",  # Increment the version here
    packages=find_packages(),
    install_requires=["tqdm"],
    entry_points={
        'console_scripts': [
            'find_old_large_files=find_old_large_files:run',
        ],
    },
    author="Disant Upadhyay",
    author_email="disantupadhyay07@gmail.com",
    description="A utility to find and remove large, old files.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="http://github.com/PrinceDisant/find_old_large_files",
)
