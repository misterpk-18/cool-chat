from models.post_model import PostModel


class FeedService:

    @staticmethod
    def get_feed():

        posts = PostModel.get_all_posts()

        return {
            "success":True,
            "feed":posts
        }