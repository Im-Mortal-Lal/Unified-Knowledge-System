from database.connection import get_connection


def save_message(session_id, role, message):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ChatHistory
        (
            SessionId,
            Role,
            Message
        )

        VALUES (?, ?, ?)
        """,
        session_id,
        role,
        message
    )

    conn.commit()
    conn.close()


def load_messages(session_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT Role,
               Message

        FROM ChatHistory

        WHERE SessionId = ?

        ORDER BY TimeStamp ASC
        """,
        session_id
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_chat(session_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM ChatHistory

        WHERE SessionId=?
        """,
        session_id
    )

def get_all_sessions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            SessionId,
            MIN(CASE WHEN Role='user' THEN Message END) AS Title
        FROM ChatHistory
        GROUP BY SessionId
        ORDER BY MAX(TimeStamp) DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_chat_title(session_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP 1 Message
        FROM ChatHistory
        WHERE SessionId = ?
        AND Role = 'user'
        ORDER BY TimeStamp ASC
    """, (session_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row.Message[:35]

    return "New Chat"

    conn.commit()
    conn.close()