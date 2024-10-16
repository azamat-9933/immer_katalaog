import datetime

import psycopg2

from configs import *


def insert_user_telegram_id(telegram_id):
    conn = psycopg2.connect(
        database=DB_NAME,
        port=DB_PORT,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    now = datetime.datetime.now()

    cursor.execute("""
    INSERT INTO bot_botuser(telegram_id)
    VALUES (%s);
    """, (telegram_id,))

    conn.commit()


def get_users_telegram_ids():
    conn = psycopg2.connect(
        database=DB_NAME,
        port=DB_PORT,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    cursor.execute("""
    SELECT telegram_id
    FROM bot_botuser;
    """)

    return [user[0] for user in cursor.fetchall()]


def get_user_language(telegram_id):
    conn = psycopg2.connect(
        database=DB_NAME,
        port=DB_PORT,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    cursor.execute("""
    SELECT interface_lang
    FROM bot_botuser
    WHERE telegram_id = %s;
    """, (telegram_id,))

    return cursor.fetchone()[0]


def update_user_language(telegram_id, language):
    conn = psycopg2.connect(
        database=DB_NAME,
        port=DB_PORT,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE bot_botuser
    SET interface_lang = %s
    WHERE telegram_id = %s;
    """, (language, telegram_id))

    conn.commit()


def get_all_contacts():
    conn = psycopg2.connect(
        database=DB_NAME,
        port=DB_PORT,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, phone, position
    FROM bot_contact;
    """)

    data = cursor.fetchall()
    return [{'name': contact[0], 'phone': contact[1], 'position': contact[2]} for contact in data]


def get_all_categories_names(language):
    conn = psycopg2.connect(
        database=DB_NAME,
        port=DB_PORT,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT name_{language}
    FROM bot_category
    WHERE parent_id IS NULL;
    """)

    return [category[0] for category in cursor.fetchall()]


def get_subcategories_by_category_name(category_name, language):
    conn = psycopg2.connect(
        database=DB_NAME,
        port=DB_PORT,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT name_{language}
    FROM bot_category
    WHERE parent_id = (SELECT id FROM bot_category WHERE name_{language} = %s);
    """, (category_name,))

    return [subcategory[0] for subcategory in cursor.fetchall()]




def get_product_info(product_model_name, language):
    conn = psycopg2.connect(
        database=DB_NAME,
        port=DB_PORT,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT name_{language}, description_{language}, model, price
    FROM bot_product
    WHERE model = %s;
    """, (product_model_name,))

    return cursor.fetchone()


def get_product_all_photos(product_id):
    conn = psycopg2.connect(
        database=DB_NAME,
        port=DB_PORT,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT image
    FROM bot_productimage
    WHERE product_id = %s;
    """, (product_id,))

    return ["media/" + photo[0] for photo in cursor.fetchall()]




def get_all_sale_products(language):
    conn = psycopg2.connect(
        database=DB_NAME,
        port=DB_PORT,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT id, name_{language}, model, description_{language}, price
        FROM bot_product
        WHERE action = True;
        """)
    product_data = cursor.fetchall()
    data = []

    for product in product_data:
        product_id, name, model, description, price = product
        photos = get_product_all_photos(product_id)
        data.append({
            'id': product_id,
            'name': name,
            'model': model,
            'description': description,
            'price': price,
            'photos': photos
        })

    return data


def get_all_products(language, category_name):
    conn = psycopg2.connect(
        database=DB_NAME,
        port=DB_PORT,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT id, name_{language}, model, description_{language}, price
    FROM bot_product
    WHERE category_id = (SELECT id FROM bot_category WHERE name_{language} = %s);
    """, (category_name,))

    product_data = cursor.fetchall()
    data = []

    for product in product_data:
        product_id, name, model, description, price = product
        photos = get_product_all_photos(product_id)
        data.append({
            'id': product_id,
            'name': name,
            'model': model,
            'description': description,
            'price': price,
            'photos': photos
        })

    return data


get_all_products(language="uz", category_name="Dazmol")
