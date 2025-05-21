import vecs

class VecsClient():
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_client(self):
        return vecs.create_client(self.db_connection)

    
