import sys, os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.dbclient import DBClient


def test_dbclient():
    dbfile = f"test_dbclient_{os.getpid()}.db"
    db = DBClient(dbfile)

    sql = db.extract_sql("create_tables.sql")
    assert "CREATE TABLE" in sql.upper()

    db.execute(
        sql="CREATE TABLE IF NOT EXISTS tmp_test (id INTEGER PRIMARY KEY, val TEXT);",
        commit=True,
        script=True,
    )
    db.execute(
        sql="INSERT INTO tmp_test (val) VALUES (?);", params=("hello",), commit=True
    )

    rows = db.execute(sql="SELECT val FROM tmp_test WHERE id = 1;", fetch=True)

    assert rows is not None

    assert rows[0][0] == "hello"
