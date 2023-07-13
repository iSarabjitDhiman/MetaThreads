from metathreads import MetaThreads
from metathreads import config


def main():
    #config.TIMEOUT = 5
    #config.PROXY = {'http': 'proxy_here', 'https': 'proxy_here'}
    threads = MetaThreads()
    username = None
    password = None
    if not all([username, password]):
        username = str(input("Enter Your Username or Email :"))
        password = str(input("Enter Your Password :"))
    threads.login(username, password)

    # check logged in user
    print(f"Logged In User {threads.me}")

    # get thread details
    print(threads.get_thread(3138977881796614961))
    #threads.get_thread("thread_id or thread_url")
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

    # # like a thread
    # threads.like_thread(3138977881796614961)

    # # repost a thread
    # threads.repost_thread([3138977881796614961, 3140525365550562013])

    # # post a thread
    # threads.post_thread(thread_caption="My First Thread..")

    # CHECK DOCUMENTATION FOR FULL FUNCTIONALITY.


if __name__ == "__main__":
    main()
