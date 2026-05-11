from database.db import get_connection
import psycopg2.extras
import uuid


class FollowModel:

    @staticmethod
    def follow_user(
        followerid,
        followeeid
    ):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        followid = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO follower(
                followid,
                followerid,
                followeeid
            )
            VALUES(%s,%s,%s)
            RETURNING *
        """,(
            followid,
            followerid,
            followeeid
        ))

        follow = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return follow

    @staticmethod
    def unfollow_user(
        followerid,
        followeeid
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM follower
            WHERE followerid=%s
            AND followeeid=%s
        """,(followerid,followeeid))

        conn.commit()

        cursor.close()
        conn.close()

        return True