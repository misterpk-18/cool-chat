class NotificationService:

    @staticmethod
    def create_like_notification(
        userid,
        postid
    ):

        print(
            f"Notification : User {userid} liked post {postid}"
        )

    @staticmethod
    def create_comment_notification(
        userid,
        postid
    ):

        print(
            f"Notification : User {userid} commented on post {postid}"
        )

    @staticmethod
    def create_follow_notification(
        followerid,
        followeeid
    ):

        print(
            f"Notification : User {followerid} followed {followeeid}"
        )