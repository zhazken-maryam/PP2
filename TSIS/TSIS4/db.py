import psycopg2
from config import load_config


def get_connection():
    """Creates PostgreSQL connection."""
    config = load_config()
    return psycopg2.connect(**config)


def create_tables():
    """Creates players and game_sessions tables."""
    sql = """
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER NOT NULL,
        level_reached INTEGER NOT NULL,
        played_at TIMESTAMP DEFAULT NOW()
    );
    """

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
    except Exception as error:
        print("DB create_tables error:", error)


def get_or_create_player(username):
    """Returns player id. Creates player if needed."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO players(username)
                    VALUES (%s)
                    ON CONFLICT (username) DO NOTHING;
                    """,
                    (username,)
                )

                cur.execute("SELECT id FROM players WHERE username=%s;", (username,))
                player_id = cur.fetchone()[0]

            conn.commit()
            return player_id

    except Exception as error:
        print("DB player error:", error)
        return None


def save_result(username, score, level):
    """Saves game result to database."""
    player_id = get_or_create_player(username)

    if player_id is None:
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO game_sessions(player_id, score, level_reached)
                    VALUES (%s, %s, %s);
                    """,
                    (player_id, score, level)
                )
            conn.commit()

    except Exception as error:
        print("DB save_result error:", error)


def get_personal_best(username):
    """Returns player's best score."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT COALESCE(MAX(gs.score), 0)
                    FROM game_sessions gs
                    JOIN players p ON gs.player_id = p.id
                    WHERE p.username = %s;
                    """,
                    (username,)
                )
                return cur.fetchone()[0]

    except Exception as error:
        print("DB personal best error:", error)
        return 0


def get_top_scores():
    """Returns top 10 scores."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT p.username, gs.score, gs.level_reached,
                           TO_CHAR(gs.played_at, 'YYYY-MM-DD HH24:MI')
                    FROM game_sessions gs
                    JOIN players p ON gs.player_id = p.id
                    ORDER BY gs.score DESC
                    LIMIT 10;
                    """
                )
                return cur.fetchall()

    except Exception as error:
        print("DB leaderboard error:", error)
        return []