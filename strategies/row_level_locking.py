import psycopg2

def row_level_locking(thread_id, DB_CONFIG, iterations=10000):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    for _ in range(iterations):
        cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE;")
        counter = cursor.fetchone()[0] + 1
        cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = %s;", (counter, 1))
        conn.commit()
    cursor.close()
    conn.close()