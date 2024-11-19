from setuptools import setup, find_packages

setup(
    name="satellite-imagery-downloader",
    version="0.1.0",
    description="A tool for downloading satellite imagery",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/artoriusss/satellite-imagery-downloader",
    packages=find_packages(include=["satellite_imagery_downloader", "satellite_imagery_downloader.*"]),
    package_dir={"satellite_imagery_downloader": "satellite_imagery_downloader"},  # Map top-level directory
    install_requires=[
        "numpy>=1.23.2",
        "opencv-python>=4.6.0.66",
        "requests>=2.28.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)