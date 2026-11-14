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
    sql = """SELECT m.id,
                    m.content,
                    m.title,
                    m.date,
                    u.username
             FROM messages m
             Left join users u on m.user_id = u.id
             WHERE m.content LIKE ?
              or m.title Like ?
	      or u.username Like ?
             ORDER BY m.date DESC
         """
    return db.query(sql, ["%" + query + "%", "%" + query + "%", "%" + query + "%"])
