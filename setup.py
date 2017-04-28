from setuptools import setup, find_packages

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


def requirements():
    with open('requirements.txt') as f:
        install_requires = [line.strip() for line in f]
    return install_requires

setup(
    name='Shifter',
    version='1.00',
    description='Command line tool for F0 transformation of a waveform',
    long_description=readme(),
    url='https://github.com/k2kobayashi/Shifter',
    author='Kazuhiro KOBAYASHI',
    author_email='root.4mac@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=requirements(),
    entry_points={'console_scripts': ['shifter = shifter.main:main']},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    keywords=['Speech', 'F0', 'Waveform'],
)
