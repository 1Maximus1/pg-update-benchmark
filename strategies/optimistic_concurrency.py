import psycopg2

def optimistic_concurrency(thread_id, DB_CONFIG, iterations=10000):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    for _ in range(iterations):
        while True:
            cursor.execute("SELECT counter, version FROM user_counter WHERE user_id = 1;")
            counter, version = cursor.fetchone()
            counter += 1
            cursor.execute("UPDATE user_counter SET counter = %s, version = %s WHERE user_id = %s AND version = %s;", (counter, version + 1, 1, version))
            conn.commit()
            if cursor.rowcount > 0:
                break
    cursor.close()
    conn.close()