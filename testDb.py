from src.processing.database import Database, Column

db = Database()

res = db.select(table = "user", columns = [Column("id"), Column("password")], joins = [], where = "`user_name` = 'michel'")

print(res[0]['user_password'])