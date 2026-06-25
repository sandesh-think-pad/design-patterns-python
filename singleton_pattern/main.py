from singleton import DatabaseConnection


def main() -> None:
    print("=" * 45)
    print("  Singleton Pattern — Database Connection")
    print("=" * 45)

    db1 = DatabaseConnection()
    db2 = DatabaseConnection()

    print(f"  Same instance: {db1 is db2}")

    print(f"  → {db1.connect()}")
    print(f"  → {db2.query('SELECT * FROM users')}")

    print("=" * 45)


if __name__ == "__main__":
    main()
