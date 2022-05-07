from setuptools import setup, find_packages

VERSION = "0.5.2"
EXTRAS_REQUIRE = {
    "tests": ["pytest", "mock", "Flask==2.0.1", "tornado", "bottle==0.12.19"],
    "lint": ["flake8==3.9.2", "flake8-bugbear==21.4.3", "pre-commit~=2.4"],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["lint"] + ["tox"]


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name="apispec-webframeworks",
    version=VERSION,
    description="Web framework plugins for apispec.",
    long_description=read("README.rst"),
    author="Steven Loria",
    author_email="sloria1@gmail.com",
    url="https://github.com/marshmallow-code/apispec-webframeworks",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"apispec_webframeworks": ["py.typed"]},
    install_requires=["apispec[yaml]>=2.0.0"],
    python_requires=">=3.6",
    extras_require=EXTRAS_REQUIRE,
    license="MIT",
    zip_safe=False,
    keywords=[
        "apispec",
        "swagger",
        "openapi",
        "specification",
        "documentation",
        "spec",
        "rest",
        "api",
        "web",
        "flask",
        "tornado",
        "bottle",
        "frameworks",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    test_suite="tests",
    project_urls={
        "Funding": "https://opencollective.com/marshmallow",
        "Issues": "https://github.com/marshmallow-code/apispec-webframeworks/issues",
    },
)
