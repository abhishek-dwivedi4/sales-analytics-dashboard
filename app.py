import os
from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Absolute path setup
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database.db')

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# 🔍 DEBUG ROUTE: Yeh check karne ke liye ki database connect hua ya nahi
@app.route('/api/debug')
def debug_db():
    try:
        conn = get_db_connection()
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        table_list = [t['name'] for t in tables]
        
        columns = []
        if 'sales' in table_list:
            cols = conn.execute("PRAGMA table_info(sales);").fetchall()
            columns = [c['name'] for c in cols]
            
        conn.close()
        return jsonify({"status": "Connected!", "db_path": db_path, "tables": table_list, "columns": columns})
    except Exception as e:
        return jsonify({"status": "Failed!", "error": str(e), "db_path": db_path})

# 1. Total Sales Route
@app.route('/api/total-sales')
def total_sales():
    conn = get_db_connection()
    try:
        total = conn.execute('SELECT SUM(Sales) as total FROM sales').fetchone()
        final_total = round(total['total'], 2) if total['total'] and total['total'] else 0
    except Exception as e:
        final_total = 0
    conn.close()
    return jsonify({"total_sales": final_total})

# 2. Total Orders Route
@app.route('/api/total-orders')
def total_orders():
    conn = get_db_connection()
    try:
        total = conn.execute('SELECT COUNT(*) as count FROM sales').fetchone()
        result = total['count'] if total else 0
    except Exception as e:
        result = 0
    conn.close()
    return jsonify({"total_orders": result})

# 3. Total Customers Route
@app.route('/api/total-customers')
def total_customers():
    conn = get_db_connection()
    try:
        total = conn.execute('SELECT COUNT(DISTINCT "Customer ID") as count FROM sales').fetchone()
        result = total['count'] if total else 0
    except Exception as e:
        result = 0
    conn.close()
    return jsonify({"total_customers": result})

# 4. Category Wise Sales Route
@app.route('/api/category-sales')
def category_sales():
    conn = get_db_connection()
    try:
        data = conn.execute('SELECT Category, SUM(Sales) as total FROM sales GROUP BY Category').fetchall()
        result = {row['Category']: round(row['total'], 2) for row in data}
    except Exception as e:
        result = {}
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)