import pymysql

class UserRepostory:

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                user='root',
                                password='lucasgiovanini',
                                db='DBturismo',
                                cursorclass=pymysql.cursors.DictCursor)
