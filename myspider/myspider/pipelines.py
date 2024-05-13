import sqlite3

class MyspiderPipeline(object):

    def open_spider(self, spider):
        self.conn = sqlite3.connect('mydatabase.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS mytable (title TEXT, link TEXT)')

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        self.c.execute('INSERT INTO mytable (title, link) VALUES (?, ?)', 
                       (item['title'], item['link']))
        return item
