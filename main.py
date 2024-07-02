from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = my_secret = os.environ['FLASK_SECRET_KEY']
CORS(app)

ads = [
    {
        "id": 1,
        "title": "Bike for sale",
        "description": "A nice bike",
        "price": 100,
        "tags": ["bike", "motorcycle", "two wheeler"]
    },
    {
        "id": 2,
        "title": "Car for sale",
        "description": "A nice car",
        "price": 5000,
        "tags": ["car", "four wheeler"]
    },
    {
        "id": 3,
        "title": "Phone for sale",
        "description": "A nice phone",
        "price": 200,
        "tags": ["phone", "samsung"]
    },
]


####################################### DATABASE ########################################
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("BB.sqlite")
    except sqlite3.Error as e:
        print(e)
    return conn


####################################### USER AUTHENTICATION ########################################


def generate_hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def check_password(password, hashed_password):
    try:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    except ValueError as e:
        print("Error checking password:", e)
        return False


####################################### API CALLS ########################################
@app.route('/', methods=['GET'])
def welcome():
    return {"status": "connected"}


@app.route('/ads', methods=['GET'])
def get_ads():
    conn = db_connection()
    cur = conn.cursor()
    sql_query = "SELECT * FROM ads_master_table;"
    cur.execute(sql_query)
    ads = cur.fetchall()
    conn.close()

    ads_list = []
    for ad in ads:
        ad_dict = {
            "id": ad[0],
            "title": ad[1],
            "description": ad[2],
            "price": ad[3],
            "img_urls": ad[4].split(",") if ad[4] else [],
            "tags": ad[5].split(",") if ad[5] else [],
            "creation_date": ad[6],
            "deletion_date": ad[7],
            "published": ad[8]
        }
        ads_list.append(ad_dict)

    return jsonify(ads_list)


@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad_by_id(ad_id):
    conn = db_connection()
    cur = conn.cursor()
    sql_query = "SELECT * FROM ads_master_table WHERE id = ?;"
    cur.execute(sql_query, (ad_id, ))
    ad = cur.fetchone()
    conn.close()
    if ad:
        ad_dict = {
            "id": ad[0],
            "title": ad[1],
            "description": ad[2],
            "price": ad[3],
            "img_urls": ad[4].split(",") if ad[4] else [],
            "tags": ad[5].split(",") if ad[5] else [],
            "creation_date": ad[6],
            "deletion_date": ad[7],
            "published": ad[8]
        }
        return jsonify(ad_dict)
    else:
        return jsonify({"error": "Ad not found"}), 404


@app.route('/ads', methods=['POST'])
def create_ad():
    new_ad = request.json
    conn = db_connection()
    cur = conn.cursor()
    sql_query = '''
        INSERT INTO ads_master_table (title, description, price, tags, img_urls)
        VALUES (?, ?, ?, ?, ?);
    '''
    ad_data = (
        new_ad.get("title"), 
        new_ad.get("description"),
        new_ad.get("price"), 
        ",".join(new_ad.get("tags", [])),
        ",".join(new_ad.get("img_urls", []))
    )
    cur.execute(sql_query, ad_data)
    new_ad_id = cur.lastrowid
    conn.commit()
    conn.close()
    new_ad["id"] = new_ad_id
    return jsonify(new_ad), 201


@app.route('/ads/<int:ad_id>', methods=['PUT'])
def update_ad(ad_id):
    updated_ad = request.json
    conn = db_connection()
    cur = conn.cursor()
    sql_query = "SELECT * FROM ads_master_table WHERE id = ?;"
    cur.execute(sql_query, (ad_id, ))
    ad = cur.fetchone()
    if ad is None:
        conn.close()
        return jsonify({"error": "Ad not found"}), 404
    # Update ad in ads_master_table
    sql_query = '''
        UPDATE ads_master_table
        SET title = ?,
            description = ?,
            price = ?,
            tags = ?,
            img_urls = ?
        WHERE id = ?;
    '''
    ad_data = (updated_ad.get("title",
                              ad[1]), updated_ad.get("description", ad[2]),
               updated_ad.get("price", ad[3]), updated_ad.get("tags", ad[4]),
               updated_ad.get("img_urls", ad[5]), ad_id)
    cur.execute(sql_query, ad_data)
    conn.commit()
    conn.close()
    updated_ad["id"] = ad_id
    return jsonify(updated_ad), 200


@app.route('/ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    conn = db_connection()
    cur = conn.cursor()
    sql_query = "SELECT * FROM ads_master_table WHERE id = ?;"
    cur.execute(sql_query, (ad_id, ))
    ad = cur.fetchone()
    if ad is None:
        conn.close()
        return jsonify({"error": "Ad not found"}), 404
    sql_query = "DELETE FROM ads_master_table WHERE id = ?;"
    cur.execute(sql_query, (ad_id, ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Ad deleted successfully"}), 200


######################################## MAIN ###########################################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
