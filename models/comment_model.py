from database.db import get_connection
import psycopg2.extras
import uuid


class CommentModel:

    @staticmethod
    def add_comment(
        postid,
        userid,
        commtxt,
        parent_comid=None
    ):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        if parent_comid:

            cursor.execute("""
                SELECT postid
                FROM comments
                WHERE comid=%s
            """,(
                parent_comid,
            ))

            parent = cursor.fetchone()

            if not parent:

                cursor.close()
                conn.close()

                return None, "Parent comment not found"

            if str(parent["postid"]) != str(postid):

                cursor.close()
                conn.close()

                return None, "Reply must be on the same post"

        comid = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO comments(
                comid,
                postid,
                userid,
                commtxt,
                parent_comid
            )
            VALUES(%s,%s,%s,%s,%s)
            RETURNING *
        """,(
            comid,
            postid,
            userid,
            commtxt,
            parent_comid
        ))

        comment = cursor.fetchone()

        conn.commit()

        cursor.close()
        conn.close()

        return comment, None

    @staticmethod
    def _rows_to_thread(rows):

        items = []

        for row in rows:

            d = dict(row)

            d["replies"] = []

            items.append(d)

        by_id = {
            x["comid"]: x
            for x in items
        }

        roots = []

        for d in items:

            pid = d.get("parent_comid")

            if pid and pid in by_id:

                by_id[pid]["replies"].append(
                    d
                )

            else:

                roots.append(d)

        return roots

    @staticmethod
    def get_comments_by_post(postid):

        conn = get_connection()

        cursor = conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        cursor.execute("""
            SELECT
                c.*,
                u.fullname AS author_fullname,
                u.username AS author_username
            FROM comments c
            LEFT JOIN users u
            ON u.userid = c.userid
            WHERE c.postid=%s
            ORDER BY c.createdat ASC
        """,(postid,))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return CommentModel._rows_to_thread(
            rows
        )
