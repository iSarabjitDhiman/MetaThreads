<h1 align="center">MetaThreads</h1>

<p align="center">
<a href="https://choosealicense.com/licenses/mit/"> <img src="https://img.shields.io/badge/License-MIT-green.svg"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/pypi/pyversions/metathreads"></a>
<a href="https://pypi.org/project/metathreads/"> <img src="https://img.shields.io/pypi/v/metathreads"></a>
<a href="https://github.com/iSarabjitDhiman/MetaThreads/commits"> <img src="https://img.shields.io/github/last-commit/iSarabjitDhiman/MetaThreads"></a>
<a href="https://twitter.com/isarabjitdhiman"> <img src="https://img.shields.io/twitter/follow/iSarabjitDhiman?style=social"></a>

## Overview

MetaThreads is Meta Threads-API to interact with Instagram threads app, extract data and perform actions. The library is written in python. MetaThreads API lets you fetch user's threads, thread replies, user's data, user's friends. Actions like posting a thread, like/unlike threads etc. can easily be perfomed with the api. Check full list of features below.

> _Note_ : `Use it on Your Own Risk. Avoid using it in excess.` **_TRY TESTING IT WITH SOME DUMMY/FAKE ACCOUNT FIRST._**

## Installation

Install MetaThreads with pip

```python
pip install metathreads
```

## Usage/Examples

```python
python quickstart.py
```

OR

```python
from metathreads import MetaThreads

MetaThreads()
```

> ### Example

```python
from metathreads import MetaThreads

threads = MetaThreads()
threads.login("username","password")

# check logged in user
threads.me

# get thread details
threads.get_thread("thread_id or thread_url")
"""
Here is an example
thread_url > https://www.threads.net/t/CuP48CiS5sx
thread_id > 3138977881796614961

It works with both id and url.
thread.get_thread(3138977881796614961)
thread.get_thread(https://www.threads.net/t/CuP48CiS5sx)

YOU CAN ALSO THROW IN MULTIPLE INPUTS AT A SINGLE TIME (WORKS WITH EVERY METHOD i.e. liking, posting, deleting , extracting data - all functions), IT SUPPORTS ASYNC/AWAIT (CONCURRENT REQUESTS.)
Just make sure you don't hit the API rate limits.

So getting multiple threads is as easy as passing a list.

threads.get_thread([3138977881796614961,3140525365550562013])
"""

# like a thread
threads.like_thread(3138977881796614961)

# repost a thread
threads.repost_thread([3138977881796614961,3140525365550562013])

# post a thread
threads.post_thread(thread_caption="My First Thread..")

#CHECK DOCUMENTATION FOR FULL FUNCTIONALITY.
```

## Documentation

Check out step by step guide.

[Documentation](docs/docs.md)

## Configuration

> ### Example - Config Usage

```python
from metathreads import config

config.PROXY = {"http":"127.0.0.1","https":"127.0.0.1"}
config.TIMEOUT = 10

```

Check out configuration docs for the available settings.

[Configurations](docs/config.md)

## Features

- Get Threads
- Get Thread Replies
- Get User's Threads
- Get User's Threads Replies
- Get User's Data (Email, Bio, Name etc.)
- Get User's Followers/Following
- Like/Unlike Threads
- Follow/Unfollow Users
- Post / Delete Threads
- Repost Threads / Destroy Reposted Threads
- Perform User Search
- Get Notifications and much more.

## Authors

- [@iSarabjitDhiman](https://www.github.com/iSarabjitDhiman)

## Feedback

If you have any feedback, please reach out to us at hello@sarabjitdhiman.com or contact me on Social Media @iSarabjitDhiman

## Support

For support, email hello@sarabjitdhiman.com
