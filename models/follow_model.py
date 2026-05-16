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
    
    @staticmethod
    def get_follower_count(followeeid):
        conn = get_connection()

        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute("""
        SELECT COUNT(1) FROM follower WHERE followeeid=%s
        """,(followeeid,))

        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row["count"] if row else 0

    @staticmethod
    def get_following_count(followerid):
        conn = get_connection()

        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute("""
        SELECT COUNT(1) FROM follower WHERE followerid=%s
        """,(followerid,))

        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row["count"] if row else 0

    @staticmethod
    def check_follow(followerid, followeeid):
        conn = get_connection()

        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute("""
        SELECT 1 FROM follower
        WHERE followerid=%s AND followeeid=%s
        LIMIT 1
        """,(followerid, followeeid))

        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row is not None



