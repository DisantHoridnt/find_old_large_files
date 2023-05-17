from setuptools import setup, find_packages

setup(
    name="find_old_large_files",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'find_old_large_files=find_old_large_files:run',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A utility to find and remove large, old files.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="http://github.com/yourusername/find_old_large_files",
)
