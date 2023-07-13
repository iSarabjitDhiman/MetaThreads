<h1 align="center">Configuration</h1>

# Importing

```python
from metathreads import config
```

> ### Example - Config Usage

```python
from metathreads import MetaThreads
from metathreads import config

config.PROXY = {"http":"127.0.0.1","https":"127.0.0.1"}
config.TIMEOUT = 10

threads = MetaThreads()
threads.login("username","password")

print(threads.get_user('zuck'))

```

## Request Timeout

```python
# request timeout - in seconds
config.TIMEOUT = 5
```

## Using Proxies

```python
# Example {"http":"proxy_here","https":"proxy_here"} Accepts python dictionary.
config.PROXY = None
```
