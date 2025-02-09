class Query:
    @staticmethod
    def reset_primary_key(table):
        return f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1;"
