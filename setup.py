from setuptools import setup


setup(
    name = "supermeshing",
    version = "0.0.1",
    author = "Tom Gustafsson",
    description = ("Python wrapper to libsupermesh"),
    license = "BSD",
    keywords = "libsupermesh supermesh",
    url = "http://github.com/kinnala/supermeshing",
    packages = ['supermeshing'],
    package_data = {'': ['supermeshing_fortran.cpython-310-x86_64-linux-gnu.so']},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
