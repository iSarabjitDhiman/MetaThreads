<h1 align="center">Documentation</h1>

## Import & Initialize.

```python
from metathreads import MetaThreads
from metathreads import config # if want to change configurations.Check out config docs.

threads = MetaThreads()
threads.login("username or email","password")
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

# READ DOCUMENTATION FOR FULL FUNCTIONALITY.
```

## Get Logged In User Details.

```python
self.me

    """
        Returns logged in user information.

        Returns:
            dict: Currently logged in user's data.
    """
```

## Login into an account

```python
login(username, password)

    """
        Log in with Instagram credentials.

        Args:
            username (str): Instagram username/email.
            password (str/int): Instagram password.

        Returns:
            dict: Token data.
    """
```

## Get Notifications

```python
get_notifications()
    """
        Get notification informations

        Returns:
            dict: Threads notifications.
    """
```

> <h2 align="center">ALL OF THE FOLLOWING METHODS CAN TAKE A LIST OF MULITPLE INPUTS AS WELL.</h2>

## Get Thread(s) ID

```python
get_thread_id(thread_url)
# YOU DON'T NEED TO CALL IT MANUALLY. EVERYTIME YOU INPUT THREAD URL IN SOME METHOD/FUNCTION, IT CONVERTS THE URL TO THE THREAD ID ON ITS OWN. FEEL FREE TO USE IT, IF YOU STILL NEED THREAD ID FOR SOME REASON.
    """
        Get thread ID.

        Args:
            thread_url (str): Thread URL or Shortcode.

        Returns:
            str: Thread ID.
    """

```

## Get Thread(s) Details

```python
get_thread(thread_id)

    """
        Get thread details.

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Thread details.
    """
```

## Get Thread(s) Replies

```python
get_thread_replies(thread_id, cursor=None)

    """
        Get thread replies.

        Args:
            thread_id (str/int): Thread ID or URL.
            cursor (str, optional): Last endcursor point. (To start from where you left off the last time). Defaults to None.

        Returns:
            dict: Thread replies dataset. i.e. people who replied to the thread and replied content.
    """
```

## Get Thread(s) Likes

```python
get_thread_likes(thread_id)
    """
        Get thread likes.

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Dataset of users who liked the thread.
    """
```

## Get User ID of User(s)

```python
get_user_id(username)
# YOU DON'T NEED TO CALL IT MANUALLY. EVERYTIME YOU INPUT USERNAME IN SOME METHOD/FUNCTION, IT CONVERTS THE USERNAME TO THE USER ID ON ITS OWN. FEEL FREE TO USE IT, IF YOU STILL NEED USER ID FOR SOME REASON.

    """
        Get user ID of the user.

        Args:
            username (str): Threads/Instagram username.

        Returns:
            str: User ID.
    """
```

## Get User(s) Details i.e. username, fullname, bio, email etc.

```python
get_user(user_id)

    """
        Get user information.

        Args:
            user_id (str/int): User ID or username.

        Returns:
            dict: User profile data.
    """
```

## Get User(s) Threads

```python
get_user_threads(user_id, cursor=None)

    """
        Get threads posted by the user.

        Args:
            user_id (str/int): User ID or username.
            cursor (str, optional): Last endcursor point. (To start from where you left off the last time). Defaults to None.

        Returns:
            dict: Dataset of a user's posted threads from the user profile.
        """
```

## Get User(s) Thread Replies

```python
get_user_threads_replies(user_id, cursor=None)

    """
        Get threads the user replied to.

        Args:
            user_id (str/int): User ID or username.
            cursor (str, optional): Last endcursor point. (To start from where you left off the last time). Defaults to None.

        Returns:
            dict: Dataset of threads the user replied to.
    """
```

## Get User(s) Followers/Following

```python
get_user_friends(user_id, followers=False, following=False, cursor=None)

    """
        Get user followers/followings data

        Args:
            user_id (str/int): User ID or username.
            followers (bool, optional): Set to True, if want to get a list of user followers. Defaults to False.
            following (bool, optional): Set to True, if want to get a list of user following. Defaults to False.
            cursor (str, optional): Last endcursor point. (To start from where you left off the last time). Defaults to None.
        Raises:
            Exception: Set one of the (followers,following) to True.

        Returns:
            dict: User friends (followers/following) dataset.
    """
```

## Perform User(s) Search

```python
search_user(search_query)

    """
        Perform a user search

        Args:
            search_query (str): Search query you want to perform. i.e. username/full name.

        Returns:
            dict: Search results.
    """
```

## Repost Thread(s)

```python
repost_thread(thread_id)

    """
        Repost a thread

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Reposted thread data.
    """
```

## Delete Reposted Thread(s)

```python
delete_repost(thread_id)

    """
        Delete/Destroy a reposted thread.

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Destroyed thread data.
    """
```

## Post/Upload New Thread(s)

```python
post_thread(thread_caption, reply_control="all")

    """
        Post/Upload a new thread.

        Args:
            thread_caption (str): Thread caption/content to be posted.
            reply_control (str, optional): Choose who can reply to your thread. Defaults to "all". Available args ("all","followers","mentions")

        Returns:
            dict: Dataset of a newly posted thread.
    """
```

## Delete Thread(s) from User's Profile

```python
delete_thread(thread_id)

    """
        Delete/Destroy a thread posted by the user. Note : Doesn't work with a reposted thread. Check delete_repost for that case.

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Dataset of a deleted thread.
    """
```

## Like Thread(s)

```python
like_thread(thread_id)

    """
        Like a thread.

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Liked thread data.
    """
```

## Unlike Thread(s)

```python
unlike_thread(thread_id)

    """
        Unlike a thread.

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Unliked thread data.
    """
```

## Follow User(s)

```python
follow(user_id)

    """
        Follow a user.

        Args:
            user_id (str/int): User ID or username.

        Returns:
            dict: Followed user data.
    """
```

## Unfollow User(s)

```python
unfollow(user_id)

    """
        Unfollow a user.

        Args:
            user_id (str/int): User ID or username.

        Returns:
            dict: Unfollowed user data.
    """
```
