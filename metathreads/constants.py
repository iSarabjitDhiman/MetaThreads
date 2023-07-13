
class Setting:
    BLOK_VERSION_ID = "5f56efad68e1edec7801f630b5c122704ec5378adbee6609a448f105f34a9c73"
    ANDROID_ID = ""
    DEVICE_ID = ""


class Path:
    HOST = "i.instagram.com"
    API_URL = "https://i.instagram.com/api/v1/"
    LOGIN_URL = "bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/"
    # endpoints
    USER_PROFILE_ENDPOINT = "https://www.instagram.com/api/v1/users/web_profile_info/?username={}"
    THREAD_ENDPOINT = "text_feed/{}/replies/"
    THREAD_LIKERS = "media/{}/likers/"
    USER_THREAD_ENDPOINT = "text_feed/{}/profile/"
    USER_THREAD_REPLIES_ENDPOINT = "text_feed/{}/profile/replies/"
    USER_INFO_ENDPOINT = "users/{}/info"
    SEARCH_USER_ENDPOINT = "users/search/"
    USER_FOLLOWERS_ENDPOINT = "friendships/{}/followers/"
    USER_FOLLOWING_ENDPOINT = "friendships/{}/following/"
    # actions
    FOLLOW_USER = "friendships/create/{}/"
    UNFOLLOW_USER = "friendships/destroy/{}/"
    NOTIFICATIONS = "text_feed/text_app_notifications/"
    INBOX = "text_feed/text_app_inbox_seen/"
    LIKE_THREAD = "media/{}/like/"
    UNLIKE_THREAD = "media/{}/unlike/"
    REPOST_THREAD = "repost/create_repost/"
    DELETE_REPOST = "repost/delete_text_app_repost/"
    POST_THREAD = "media/configure_text_only_post/"
    DELETE_THREAD = "media/{}/delete/"


if __name__ == "__main__":
    pass
