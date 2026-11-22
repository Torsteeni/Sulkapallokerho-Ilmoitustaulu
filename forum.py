import db
def get_thread(thread_id):
    sql = "SELECT id, title FROM threads WHERE id = ?"
    return db.query(sql, [thread_id])[0]

def get_messages(thread_id):
    sql = """SELECT m.id, m.content, m.sent_at, m.user_id, u.username
             FROM messages m, users u
             WHERE m.user_id = u.id AND m.thread_id = ?
             ORDER BY m.id"""
    return db.query(sql, [thread_id])

def search(query):
    sql = """SELECT 
             m.id, m.content, m.title, m.date, u.username, m.location, m.event_date, m.event_time
             FROM messages m
             LEFT JOIN users u ON m.user_id = u.id
             WHERE m.event_date = ?
             ORDER BY m.event_date ASC
         """

    return db.query(sql, [query])
