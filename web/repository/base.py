from odmantic import AIOEngine


class BaseRepository:

    def __init__(self, database: AIOEngine):
        self.database = database
