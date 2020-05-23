import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dempy',
    version='0.1',
    author="Miguel Teixeira, Pedro Pinho, Ricardo Moura",
    author_email="up201605150@fe.up.pt, up201605166@fe.up.pt, up201604912@fe.up.pt",
    description="A package that simplifies access and management of datasets and their annotations",
    url="https://github.com/miguelalexbt/dempy.git",
	license="MIT License",
	python_requires=">=3",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(
		include=['dempy.*', 'dempy'],
	),
    install_requires=[
        "requests>=2.23.0",
        "matplotlib>=3.2.1",
        "protobuf>=3.11.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )