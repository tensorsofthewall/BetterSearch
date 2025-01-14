import sqlite3

class ChatDB:
    def __init__(self, chat_db_path="chat_db.db",**kwargs):
        self.chat_db_path = chat_db_path
        self.conn = sqlite3.connect(self.chat_db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
        
    def _create_tables(self):
        # Create tables if not existing
        # chats (chat_id, title)
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS chats (
                chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
            '''
        )
        
        # messages (message_id, chat_id, content, sent_at)        
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                input_str TEXT NOT NULL,
                out_str TEXT NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats(chat_id)
            )
            '''
        )
        
        self.conn.commit()
    
    
    def get_chat_data(self):
        self.cursor.execute(
            '''
            SELECT c.chat_id, c.title, m.message_id, m.input_str, m.out_str
            FROM chats c LEFT JOIN messages m ON c.chat_id = m.chat_id ORDER BY c.chat_id, m.message_id
            '''
        )
        rows = self.cursor.fetchall()
        chat_data = {}
        
        for row in rows:
            chat_id, title, message_id, input_str, out_str = row
            if chat_id not in chat_data:
                chat_data[chat_id] = {"title": title, "messages": []}
            if message_id:
                chat_data[chat_id]["messages"].append({"message_id": message_id, "input_str": input_str, "out_str": out_str})
        
        return chat_data

    def get_chat_title_list(self):
        self.cursor.execute('SELECT title from chats')
        return [row[0] for row in self.cursor.fetchall()]
    
    def save_chat_data(self, title, messages):
        
        # print("Title:", title)
        # print("Messages:", messages)
        self.conn.execute('BEGIN TRANSACTION')
        try:
            self.cursor.execute('INSERT INTO chats(title) VALUES (?)',(title,))
            # print("title inserted")
            chat_id = self.cursor.lastrowid
            self.cursor.executemany('INSERT INTO messages(chat_id, input_str, out_str) VALUES (?, ?, ?)', [(chat_id, message['input_str'], message['out_str']) for message in messages])
            # print("messages inserted")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")
            self.conn.rollback()
        
    def delete_all_data(self):
        self.cursor.execute('DELETE FROM messages')
        self.cursor.execute('DELETE FROM chats')
        
        # Reset autoincrement columns
        self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='messages'")
        self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='chats'")
        
        self.conn.commit()
        
    def delete_chat_data(self, chat_id):
        self.cursor.execute('DELETE FROM messages WHERE chat_id = ?', (chat_id,))
        self.cursor.execute('DELETE FROM chats WHERE chat_id = ?', (chat_id,))
        
        # Reset autoincrement for messages, only for the deleted chat
        self.cursor.execute(
            """
            UPDATE sqlite_sequence SET seq = seq (SELECT COALESCE(MAX(message_id), 0) FROM messages) where name='messages
            """
        )
        
        self.conn.commit()
        
    def update_chat_title(self, chat_id, new_title):
        self.cursor.execute('UPDATE chats SET title = ? WHERE chat_id = ?', (new_title, chat_id))
        self.conn.commit()

    def close(self):
        self.conn.close()