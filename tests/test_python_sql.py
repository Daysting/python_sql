import unittest
import sqlite3
from python_sql import (
    create_connection,
    create_table,
    select_us_numbers,
    update_phone_types,
    delete_xx_records,
    drop_phone_table,
)


class TestPythonSQL(unittest.TestCase):
    def setUp(self):
        # use an in-memory database for isolation
        self.conn = create_connection(':memory:')
        create_table(self.conn)
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
        cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 25)")
        cursor.execute("INSERT INTO users (name, age) VALUES ('XXCharlie', 35)")
        self.conn.commit()

    def test_sequence_of_operations(self):
        # initial data
        initial = select_us_numbers(self.conn)
        self.assertEqual(len(initial), 3)

        # add phone_type column
        update_phone_types(self.conn)
        after_add = select_us_numbers(self.conn)
        # each row should have 4 columns now (id, name, age, phone_type)
        self.assertTrue(all(len(row) == 4 for row in after_add))

        # delete names starting with XX
        delete_xx_records(self.conn)
        after_delete = select_us_numbers(self.conn)
        self.assertFalse(any(row[1].startswith('XX') for row in after_delete))

        # drop phone_type column; sqlite may raise or simply keep the column
        try:
            drop_phone_table(self.conn)
            after_drop = select_us_numbers(self.conn)
            # if drop succeeded, rows should revert back to 3 columns
            self.assertTrue(all(len(row) == 3 for row in after_drop))
        except sqlite3.OperationalError:
            # older sqlite versions do not support DROP COLUMN, skip
            self.skipTest("SQLite version does not support DROP COLUMN")

    def tearDown(self):
        self.conn.close()


if __name__ == '__main__':
    unittest.main()
