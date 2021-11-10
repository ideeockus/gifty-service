from db.migrations import img_path_migration


def apply_migrations():
    print("Applying migrations")
    img_path_migration.apply_img_path_migration()
