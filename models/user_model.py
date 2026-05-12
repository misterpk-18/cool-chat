from database.db import get_connection
import psycopg2.extras
import bcrypt
import uuid


class UserModel:

    @staticmethod
    def create_user(
        username,
        email,
        password,
        fullname,
        bio="",
        profpicurl=""
    ):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        userid = str(uuid.uuid4())

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute("""
            INSERT INTO users(
                userid,
                username,
                email,
                password,
                fullname,
                bio,
                profpicurl
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s)
            RETURNING *
        """,(
            userid,
            username,
            email,
            hashed_password,
            fullname,
            bio,
            profpicurl
        ))

        user = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return user

    @staticmethod
    def get_user_by_id(userid):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        cursor.execute("""
            SELECT *
            FROM users
            WHERE userid=%s
        """,(userid,))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user

    @staticmethod
    def search_users_by_name(
        query,
        limit=20
    ):

        q = (query or "").strip()

        if not q:

            return []

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        pattern = f"%{q}%"

        cursor.execute("""
            SELECT
                userid,
                username,
                fullname,
                bio,
                profpicurl
            FROM users
            WHERE fullname ILIKE %s
            OR username ILIKE %s
            ORDER BY fullname ASC
            LIMIT %s
        """,(
            pattern,
            pattern,
            limit
        ))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    @staticmethod
    def get_public_profile_by_id(userid):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        cursor.execute("""
            SELECT
                userid,
                username,
                fullname,
                bio,
                profpicurl
            FROM users
            WHERE userid=%s
        """,(userid,))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user

    @staticmethod
    def get_user_by_username(username):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username=%s
        """,(username,))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user

    @staticmethod
    def get_user_by_email(email):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        cursor.execute("""
            SELECT *
            FROM users
            WHERE email=%s
        """,(email,))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user

    @staticmethod
    def login_user(
        username_or_email,
        password
    ):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username=%s
            OR email=%s
        """,(
            username_or_email,
            username_or_email
        ))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:

            return None

        is_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password"].encode("utf-8")
        )

        if is_valid:

            return user

        return None

    @staticmethod
    def update_profile(
        userid,
        username,
        fullname,
        bio,
        profpicurl
    ):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        cursor.execute("""
            UPDATE users
            SET
                username=%s,
                fullname=%s,
                bio=%s,
                profpicurl=%s
            WHERE userid=%s
            RETURNING *
        """,(
            username,
            fullname,
            bio,
            profpicurl,
            userid
        ))

        updated_user = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return updated_user

    @staticmethod
    def delete_user(userid):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM users
            WHERE userid=%s
        """,(userid,))

        conn.commit()

        cursor.close()
        conn.close()

        return True