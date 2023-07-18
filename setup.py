from setuptools import setup

VERSION = "0.0.2"
SHORT_DESCRIPTION = "MetaThreads is Meta Threads-API to interact with Instagram threads app, extract data and perform actions. The library is written in python. MetaThreads API lets you fetch user's threads, thread replies, user's data, user's friends. Actions like posting a thread, like/unlike threads etc. can easily be perfomed with the api."

with open("requirements.txt") as file:
    dependencies = file.read().splitlines()
with open("README.md", "r") as file:
    DESCRIPTION = file.read()


setup(
    name="metathreads",
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Sarabjit Dhiman",
    author_email="hello@sarabjitdhiman.com",
    license="MIT",
    url="https://github.com/iSarabjitDhiman/MetaThreads",
    packages=["metathreads"],
    keywords=["metathreads", "threads-api", "threadsapi",
              "meta threads api", "threads api",
              "instagram threads", "threads-api-python", "insta-threads"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
    ],
    install_requires=dependencies,
    python_requires=">=3"
)
