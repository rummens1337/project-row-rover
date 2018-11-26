from src.processing.database import Database, Column

db = Database()

db.select(table = "users", columns = [Column("id"), Column("password")])