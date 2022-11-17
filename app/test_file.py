from unittest.mock import patch
from mysql_python import select

def test_select():
    rows = select(table="products")
    assert rows == []
    