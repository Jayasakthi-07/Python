"""Library Book Management System using Python and SQLite.

Connects to library.db, creates the Book table, inserts sample records,
runs queries, updates and deletes records, then commits and closes.
"""

import sqlite3

DB_NAME = "library.db"

SAMPLE_BOOKS = [
    (1, "Python Basics", "John Smith", "Programming", 450),
    (2, "Database Systems", "R. Kumar", "Database", 600),
    (3, "Machine Learning", "David Lee", "AI", 750),
    (4, "Web Development", "Anita Rao", "Programming", 550),
    (5, "Data Science", "Mary John", "AI", 800),
]


def display(title, rows):
    """Print a heading followed by the given book rows as a table."""
    print(f"\n{title}")
    print("-" * 72)
    print(f"{'BookID':<8}{'Title':<20}{'Author':<14}{'Category':<14}{'Price (Rs.)':>12}")
    print("-" * 72)
    if not rows:
        print("No records found.")
    for book_id, book_title, author, category, price in rows:
        print(f"{book_id:<8}{book_title:<20}{author:<14}{category:<14}{price:>12.2f}")
    print("-" * 72)


def main():
    # 1. Connect to the SQLite database (created if it does not exist)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print(f"Connected to database '{DB_NAME}'.")

    try:
        # 2. Create the Book table (dropped first so the program can be re-run)
        cursor.execute("DROP TABLE IF EXISTS Book")
        cursor.execute(
            """
            CREATE TABLE Book (
                BookID   INTEGER PRIMARY KEY,
                Title    TEXT NOT NULL,
                Author   TEXT NOT NULL,
                Category TEXT NOT NULL,
                Price    REAL NOT NULL
            )
            """
        )
        print("Table 'Book' created.")

        # 3. Insert the five sample records using a parameterized query
        cursor.executemany(
            "INSERT INTO Book (BookID, Title, Author, Category, Price) VALUES (?, ?, ?, ?, ?)",
            SAMPLE_BOOKS,
        )
        conn.commit()
        print(f"{cursor.rowcount} records inserted.")

        # 4. Display all book records
        cursor.execute("SELECT * FROM Book")
        display("All Book Records:", cursor.fetchall())

        # 5. Display books belonging to the Programming category
        cursor.execute("SELECT * FROM Book WHERE Category = ?", ("Programming",))
        display("Books in the 'Programming' Category:", cursor.fetchall())

        # 6. Display books priced above Rs. 500
        cursor.execute("SELECT * FROM Book WHERE Price > ?", (500,))
        display("Books Priced Above Rs. 500:", cursor.fetchall())

        # 7. Update the price of 'Python Basics' from 450 to 500
        cursor.execute(
            "UPDATE Book SET Price = ? WHERE Title = ?", (500, "Python Basics")
        )
        print(f"\nUpdated price of 'Python Basics' to Rs. 500 ({cursor.rowcount} row affected).")

        # 8. Delete the book record with BookID 4
        cursor.execute("DELETE FROM Book WHERE BookID = ?", (4,))
        print(f"Deleted book with BookID 4 ({cursor.rowcount} row affected).")

        # 9. Display all records after updating and deleting
        cursor.execute("SELECT * FROM Book")
        display("All Book Records After Update and Delete:", cursor.fetchall())

        # 10. Commit the changes
        conn.commit()
        print("\nChanges committed successfully.")

    except sqlite3.Error as error:
        conn.rollback()
        print(f"Database error: {error}")

    finally:
        # 10. Close the database connection
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
