import psycopg2
import threading
import time
from postgresConfig import DB_CONFIG

def setup_database():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_counter (
            user_id SERIAL PRIMARY KEY,
            counter INTEGER NOT NULL DEFAULT 0,
            version INTEGER NOT NULL DEFAULT 0
        )
    """)
    cursor.execute("DELETE FROM user_counter;")
    cursor.execute("ALTER SEQUENCE user_counter_user_id_seq RESTART WITH 1;")
    cursor.execute("INSERT INTO user_counter (counter, version) VALUES (0, 0);")
    conn.commit()
    cursor.close()
    conn.close()

def measure_time(update_function, name, threads=10, iterations=10000):
    thread_list = []
    start_time = time.time()
    for i in range(threads):
        thread = threading.Thread(target=update_function, args=(i, DB_CONFIG, iterations))
        thread_list.append(thread)
        thread.start()
    for thread in thread_list:
        thread.join()
    end_time = time.time()
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1;")
    final_counter = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    
    print(f"{name}: completed for {end_time - start_time:.2f} seconds, final value of counter: {final_counter}")

if __name__ == "__main__":
    setup_database()
    from strategies.lost_update import lost_update
    from strategies.in_place_update import in_place_update
    from strategies.row_level_locking import row_level_locking
    from strategies.optimistic_concurrency import optimistic_concurrency
    
    measure_time(lost_update, "Lost Update")
    setup_database()
    measure_time(in_place_update, "In-place Update")
    setup_database()
    measure_time(row_level_locking, "Row-Level Locking")
    setup_database()
    measure_time(optimistic_concurrency, "Optimistic Concurrency Control")
