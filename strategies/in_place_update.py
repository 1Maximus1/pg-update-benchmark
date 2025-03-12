import psycopg2

def in_place_update(thread_id, DB_CONFIG, iterations=10000):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    for _ in range(iterations):
        cursor.execute("UPDATE user_counter SET counter = counter + 1 WHERE user_id = 1;")
        conn.commit()
    cursor.close()
    conn.close()