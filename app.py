import pytz
import sqlite3
import subprocess
from datetime import datetime
from flask import Flask, render_template, jsonify


app = Flask(__name__)

def graph_points(array_name):
    utc_timezone = pytz.timezone('UTC')
    current_time = datetime.now(utc_timezone).strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("SELECT price, Timestamp FROM price_graph")
    data = cursor.fetchall()
    format = '%Y-%m-%d %H:%M:%S'
    for dates in data:
        dateObject1 = datetime.strptime(current_time, format)
        dateObject2 = datetime.strptime(dates[1], format)

        hoursdifference = float('{:.6f}'.format((dateObject1 - dateObject2).total_seconds() / 3600))
        if hoursdifference <= 24.0:
            graph_data = {
                'time': hoursdifference,
                'value': dates[0]
            }

            array_name.append(graph_data)



def update_cards():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("")


@app.route("/")
def home():
  return render_template("home.html")

@app.route("/contact")
def contact():
  return render_template("contact.html")

@app.route("/disclaimer")
def disclaimer():
  return render_template("Disclaimer.html")


@app.route("/products")
def index():
    return render_template("index.html")
@app.route("/table",methods=["POST"])
def get_table_data():
    try:
        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("select * from price_table")
        data = cursor.fetchall()

        cursor.execute(f"UPDATE products set price_darkteal = ? WHERE ids = ?",(data[21][2],f"ppa1",))
        conn.commit()

        cursor.execute(f"UPDATE products set price_darkteal = ? WHERE ids = ?",(data[22][2],f"ppa2",))
        conn.commit()


        cursor.execute(f"UPDATE products set price_darkteal = ? WHERE ids = ?",(data[23][2],f"ppa3",))
        conn.commit()

        cursor.execute(f"UPDATE products set price_darkteal = ? WHERE ids = ?",(data[24][2],f"ppa4",))
        conn.commit()

        cursor.execute(f"UPDATE products set price_darkteal = ? WHERE ids = ?",(data[25][2],f"ppa5",))
        conn.commit()

        cursor.execute(f"UPDATE products set price_darkteal = ? WHERE ids = ?",(data[26][2],f"ppa5",))
        conn.commit()

        result = [{"spn1":data[0][2],"spn2":data[1][2],"spn3":data[2][2],"spn4":data[3][2],"spn5":data[4][2],"spn6":data[5][2],"spn7":data[6][2],"spn8":data[7][2],"spn9":data[8][2],"spn10":data[9][2],"spn11":data[10][2],"spn12":data[11][2],"cus1":data[12][2],"cus2":data[13][2],"cus3":data[14][2],"cus4":data[15][2],"cus5":data[16][2],"ppc1":data[17][2],"ppc2":data[18][2],"ppc3":data[19][2],"ppc4":data[20][2],"ppa1":data[21][2],"ppa2":data[22][2],"ppa3":data[23][2],"ppa4":data[24][2],"ppa5":data[25][2],"ppa6":data[26][2],"mak1":data[27][2],"mak2":data[28][2],"mak3":data[29][2],"mak4":data[30][2],"mak5":data[31][2],"date":data[32][2],"time":data[33][2]}]
        return jsonify(result)


    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/data", methods=["POST"])
def get_data():
    try:
        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        data = cursor.fetchall()
        conn.close()

        result = [{"image_path": row[1],"product_name" : row[2],"price_royalblue": row[3], "price_darkteal": row[4],"additional_price": row[6],"currency":row[5],"ids": row[7]} for row in data]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/graph", methods=["POST"])
def get_graph_data():
    result = []
    try:
        graph_points(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    scrape_process = subprocess.Popen(['python3', 'scrape.py'])

    app.run(host='0.0.0.0',port=8000,debug=True)