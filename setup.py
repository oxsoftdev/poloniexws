from setuptools import find_packages, setup

setup(
    name='poloniexws'
    , version='0.1'
    , author='sebastian'
    , author_email='oxsoftdev@gmail.com'
    , packages=find_packages()
    , url='https://github.com/oxsoftdev/poloniexws'
    , license='LICENSE.txt'
    , install_requires=[
        'dppy'
    ]
    , dependency_links=[
        'https://github.com/oxsoftdev/dppy/tarball/master#egg=dppy-0.1'
    ]
)

