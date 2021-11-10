from db.migrations import goods_item_migrations


def apply_migrations():
    print("Applying migrations")
    goods_item_migrations.apply_img_path_migration()
    goods_item_migrations.apply_price_migration()
