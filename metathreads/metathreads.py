import httpx
import json
import datetime
from . import util
from . import config
from .request_util import generate_request_data
from .constants import Setting, Path


class MetaThreads:
    def __init__(self):
        self.session = httpx.Client(follow_redirects=True)
        self.session.headers.update(util.generate_headers())
        self.logged_in_user = None

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session):
        self._session = session
        config._DEFAULT_SESSION = session

    @property
    def me(self):
        return self.logged_in_user

    @property
    def user_id(self):
        return self.logged_in_user.get('pk', '')

    def login(self, username, password):
        """Log in with instagram credentials.

        Args:
            username (str): Instagram username/email.
            password (str/int): Instagram password.

        Returns:
            dict: Token data.
        """
        timestamp = int(datetime.datetime.now().timestamp())
        password = f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}'
        payload = {"client_input_params": {"password": password, "contact_point": username, "device_id": Setting.ANDROID_ID},
                   "server_params": {"credential_type": "password", 'device_id': Setting.ANDROID_ID},
                   'bk_client_context': {"bloks_version": Setting.BLOK_VERSION_ID, "styles_id": "instagram"},
                   'bloks_versioning_id': Setting.BLOK_VERSION_ID}

        payload = {keys: json.dumps(values) if isinstance(
            values, dict) else values for keys, values in payload.items()}

        response = generate_request_data(
            Path.LOGIN_URL, method="POST", data=payload)
        token_data, self.logged_in_user = util.get_auth_token(response)
        return token_data

    def thread_id_decorator(original_function):
        def wrapper(self, *args, **kwargs):
            args = list(args)
            args[0] = self.get_thread_id(args[0])
            args = tuple(args)
            return original_function(self, *args, **kwargs)
        return wrapper

    def user_id_decorator(original_function):
        def wrapper(self, *args, **kwargs):
            args = list(args)
            args[0] = self.get_user_id(args[0])
            args = tuple(args)
            return original_function(self, *args, **kwargs)
        return wrapper

    def get_thread_id(self, thread_url):
        if not isinstance(thread_url, list):
            thread_url = [thread_url]
        thread_ids = [*filter(lambda thread: thread if isinstance(
            thread, int) or thread.isnumeric() else None, thread_url)]
        if len(thread_ids) != len(thread_url):
            pending_ids = [
                thread for thread in thread_url if thread not in thread_ids]
            new_thread_ids = [*map(util.shortcode_to_id, pending_ids)]
            thread_ids = [*thread_ids, *new_thread_ids]
        return thread_ids if len(thread_ids) > 1 else thread_ids[0] if thread_ids else None

    @thread_id_decorator
    def get_thread(self, thread_id):
        """Get thread details.

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Thread details.
        """
        return generate_request_data(Path.THREAD_ENDPOINT, thread_id)

    @thread_id_decorator
    def get_thread_replies(self, thread_id, cursor=None):
        """Get thread replies.

        Args:
            thread_id (str/int): Thread ID or URL.
            cursor (str, optional): Last endcursor point. (To start from where you left off the last time). Defaults to None.

        Returns:
            dict: Thread replies dataset. i.e. people who replied to the thread and replied content.
        """
        params = {"count": 100}
        pagination_data = {"paging_token'": cursor}
        return generate_request_data(Path.THREAD_ENDPOINT, thread_id, params=params, pagination=pagination_data)

    @thread_id_decorator
    def get_thread_likes(self, thread_id):
        """Get thread likes.

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Dataset of users who liked the thread.
        """
        return generate_request_data(Path.THREAD_LIKERS, thread_id)

    def get_user_id(self, username):
        if not isinstance(username, list):
            username = [username]
        user_ids = [*filter(lambda user: user if isinstance(
            user, int) or user.isnumeric() else None, username)]
        if len(user_ids) != len(username):
            pending_users = [user for user in username if user not in user_ids]
            response = generate_request_data(
                Path.USER_PROFILE_ENDPOINT, pending_users)
            user_ids = [*user_ids, *[user['data']['user']['id']
                                     for user in response]]
        return user_ids if len(user_ids) > 1 else user_ids[0] if user_ids else None

    @user_id_decorator
    def get_user(self, user_id):
        """Get user information.

        Args:
            user_id (str/int): User ID or username.

        Returns:
            dict: User profile data.
        """
        params = {'is_prefetch': False, 'entry_point': 'profile',
                  'from_module': 'ProfileViewModel'}
        return generate_request_data(Path.USER_INFO_ENDPOINT, user_id, params=params)

    @user_id_decorator
    def get_user_threads(self, user_id, cursor=None):
        """Get threads posted by the user.

        Args:
            user_id (str/int): User ID or username.
            cursor (str, optional): Last endcursor point. (To start from where you left off the last time). Defaults to None.

        Returns:
            dict: Dataset of a user's posted threads from the user profile.
        """
        params = {"count": 100}
        pagination_data = {"max_id": cursor}
        return generate_request_data(Path.USER_THREAD_ENDPOINT, user_id, params=params, pagination=pagination_data)

    @user_id_decorator
    def get_user_threads_replies(self, user_id, cursor=None):
        """Get threads the user replied to.

        Args:
            user_id (str/int): User ID or username.
            cursor (str, optional): Last endcursor point. (To start from where you left off the last time). Defaults to None.

        Returns:
            dict: Dataset of threads the user replied to.
        """
        params = {"count": 100}
        pagination_data = {"max_id": cursor}
        return generate_request_data(Path.USER_THREAD_REPLIES_ENDPOINT, user_id, params=params, pagination=pagination_data)

    @user_id_decorator
    def get_user_friends(self, user_id, followers=False, following=False, cursor=None):
        """Get user followers/followings data

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
        if (not followers and not following) or (followers and following):
            raise Exception("Set one of the (followers,following) to True.")

        endpoint = Path.USER_FOLLOWERS_ENDPOINT if followers else Path.USER_FOLLOWING_ENDPOINT
        params = {'count': 100, 'include_user_count': True,
                  'search_surface': 'barcelona_following_graph_page'}
        pagination_data = {"max_id": cursor}
        return generate_request_data(endpoint, user_id, params=params, pagination=pagination_data)

    def search_user(self, search_query):
        """Perform a user search

        Args:
            search_query (str): Search query you want to perform. i.e. username/full name.

        Returns:
            dict: Search results.
        """
        params = {'search_surface': 'user_search_page',
                  'timezone_offset': 0, 'count': 100}
        additional_payload = {"params": {'q': search_query}}
        return generate_request_data(Path.SEARCH_USER_ENDPOINT, params=params, additional_payload=additional_payload)

    def get_notifications(self):
        """Get notification informations

        Returns:
            dict: Threads notifications.
        """
        params = {'feed_type': 'all', 'mark_as_seen': False,
                  'timezone_offset': 0, 'timezone_name': 'GMT'}
        return generate_request_data(Path.NOTIFICATIONS, params=params)

    # def send_inbox_seen(self):
    #     data = {"_uuid": Setting.DEVICE_ID}
    #     return generate_request_data(Path.INBOX, data=data, method="POST")

    @thread_id_decorator
    def repost_thread(self, thread_id):
        """Repost a thread

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Reposted thread data.
        """
        data = {"_uuid": Setting.DEVICE_ID}
        additional_payload = {"data": {'media_id': thread_id}}
        return generate_request_data(Path.REPOST_THREAD, data=data, additional_payload=additional_payload, method="POST")

    @thread_id_decorator
    def delete_repost(self, thread_id):
        """Delete/Destroy a reposted thread.

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Destroyed thread data.
        """
        data = {'_uuid': Setting.DEVICE_ID}
        additional_payload = {"data": {'original_media_id': thread_id}}
        return generate_request_data(Path.DELETE_REPOST, data=data, additional_payload=additional_payload, method="POST")

    def post_thread(self, thread_caption, reply_control="all"):
        """Post/Upload a new thread.

        Args:
            thread_caption (str): Thread caption/content to be posted.
            reply_control (str, optional): Choose who can reply to your thread. Defaults to "all". Available args ("all","followers","mentions")

        Returns:
            dict: Dataset of a newly posted thread.
        """
        reply_control = reply_control.lower()
        reply_control = 0 if reply_control == 'all' else 1 if reply_control == 'followers' else 2 if reply_control == 'mentions' else 0
        upload_id = int(datetime.datetime.now().microsecond *
                        datetime.datetime.now().microsecond)
        data = {"publish_mode": "text_post", "upload_id": upload_id, "text_post_app_info": {"reply_control": reply_control},
                "timezone_offset": 0, "_uid": self.user_id, "device_id": Setting.ANDROID_ID,
                "_uuid": Setting.DEVICE_ID, "caption": thread_caption, "audience": "default"}
        signed_data = {"signed_body": f"SIGNATURE.{json.dumps(data)}"}
        return generate_request_data(Path.POST_THREAD, data=signed_data, method="POST")

    @thread_id_decorator
    def delete_thread(self, thread_id):
        """Delete/Destroy a thread posted by the user. Note : Doesn't work with a reposted thread. Check delete_repost for that case.

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Dataset of a deleted thread.
        """
        if isinstance(thread_id, int) or isinstance(thread_id, str):
            if str(thread_id).find("_") == -1:
                thread_id = f"{thread_id}_{self.user_id}"
        if isinstance(thread_id, list):
            thread_id = [f"{item}_{self.user_id}" if str(thread_id).find(
                "_") == -1 else item for item in thread_id]
        params = {'media_type': 'TEXT_POST'}
        data = {"media_id": thread_id,
                "_uid": self.user_id, "_uuid": Setting.DEVICE_ID}
        signed_data = {"signed_body": f"SIGNATURE.{json.dumps(data)}"}
        return generate_request_data(Path.DELETE_THREAD, thread_id, params=params, data=signed_data, method="POST")

    @thread_id_decorator
    def like_thread(self, thread_id):
        """Like a thread.

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Liked thread data.
        """
        data = {"delivery_class": "organic", "tap_source": "button",
                "media_id": thread_id, "_uid": self.user_id, "_uuid": Setting.DEVICE_ID}
        signed_data = {"signed_body": f'SIGNATURE.{data}', "d": 0}
        return generate_request_data(Path.LIKE_THREAD, thread_id, data=signed_data, method="POST")

    @thread_id_decorator
    def unlike_thread(self, thread_id):
        """Unlike a thread.

        Args:
            thread_id (str/int): Thread ID or URL.

        Returns:
            dict: Unliked thread data.
        """
        data = {"delivery_class": "organic", "tap_source": "button",
                "media_id": thread_id, "_uid": self.user_id, "_uuid": Setting.DEVICE_ID}
        signed_data = {"signed_body": f'SIGNATURE.{data}', "d": 0}
        return generate_request_data(Path.UNLIKE_THREAD, thread_id, data=signed_data, method="POST")

    @user_id_decorator
    def follow(self, user_id):
        """Follow a user.

        Args:
            user_id (str/int): User ID or username.

        Returns:
            dict: Followed user data.
        """
        data = {"user_id": user_id, "_uid": self.user_id,
                "_uuid": Setting.DEVICE_ID}
        signed_data = {"signed_body": f'SIGNATURE.{data}', "d": 0}
        return generate_request_data(Path.FOLLOW_USER, user_id, data=signed_data, method="POST")

    @user_id_decorator
    def unfollow(self, user_id):
        """Unfollow a user.

        Args:
            user_id (str/int): User ID or username.

        Returns:
            dict: Unfollowed user data.
        """
        data = {"user_id": user_id, "_uid": self.user_id,
                "_uuid": Setting.DEVICE_ID}
        signed_data = {"signed_body": f'SIGNATURE.{data}', "d": 0}
        return generate_request_data(Path.UNFOLLOW_USER, user_id, data=signed_data, method="POST")


if __name__ == "__main__":
    pass
