from setuptools import setup


setup(
    name = "supermeshing",
    version = "0.0.1",
    author = "Tom Gustafsson",
    # author_email = ".com",
    description = ("An demonstration of how to create, document, and publish "
                                   "to the cheese shop a5 pypi.org."),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://github.com/kinnala/supermeshing",
    packages = ['supermeshing'],
    package_data = {'': ['supermeshing_fortran.cpython-310-x86_64-linux-gnu.so']},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
