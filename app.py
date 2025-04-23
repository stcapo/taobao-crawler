from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pandas as pd
import numpy as np
import jieba
import os
import sqlite3
import random
import re
from collections import Counter
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

def load_data():
    return pd.read_excel('data.xlsx')

# Generate a simple math captcha
def generate_captcha():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    answer = num1 + num2
    question = f"{num1} + {num2} = ?"
    return question, answer

# Validate email format
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Generate captcha for both login and registration
        captcha_question, captcha_answer = generate_captcha()
        session['captcha_answer'] = captcha_answer
        return render_template('login.html', captcha_question=captcha_question)

    if request.method == 'POST':
        # Check if it's a login or registration request
        if 'login' in request.form:
            username = request.form.get('username')
            password = request.form.get('password')
            captcha = request.form.get('captcha')

            # Validate captcha
            if not captcha or int(captcha) != session.get('captcha_answer'):
                flash('验证码错误!')
                captcha_question, captcha_answer = generate_captcha()
                session['captcha_answer'] = captcha_answer
                return render_template('login.html', captcha_question=captcha_question)

            # Validate credentials
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            conn.close()

            if user and check_password_hash(user['password'], password):
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash('用户名或密码错误!')

        # Generate new captcha
        captcha_question, captcha_answer = generate_captcha()
        session['captcha_answer'] = captcha_answer
        return render_template('login.html', captcha_question=captcha_question)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    email = request.form.get('email')
    captcha = request.form.get('captcha')

    # Validate captcha
    if not captcha or int(captcha) != session.get('captcha_answer'):
        flash('验证码错误!')
        return redirect(url_for('login'))

    # Validate input
    if not username or not password or not confirm_password or not email:
        flash('所有字段都是必填的!')
        return redirect(url_for('login'))

    if password != confirm_password:
        flash('两次输入的密码不一致!')
        return redirect(url_for('login'))

    if not is_valid_email(email):
        flash('邮箱格式不正确!')
        return redirect(url_for('login'))

    # Check if username or email already exists
    conn = get_db_connection()
    existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?',
                               (username, email)).fetchone()

    if existing_user:
        conn.close()
        flash('用户名或邮箱已被注册!')
        return redirect(url_for('login'))

    # Create new user
    hashed_password = generate_password_hash(password)
    conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                (username, hashed_password, email))
    conn.commit()
    conn.close()

    flash('注册成功，请登录!')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    username = session.get('username', 'User')
    return render_template('dashboard.html', username=username)

@app.route('/data/chart1')
def chart1_data():
    if not session.get('logged_in'):
        return jsonify({'error': 'unauthorized'})

    df = load_data()
    top_n = 10

    # 获取原始数据中的商品信息
    df['Deal'] = pd.to_numeric(df['Deal'], errors='coerce')
    original_products = df.head(top_n).copy()

    # 创建模拟的销量数据，确保依次递减
    # 使用指数递减函数，使得差异更加明显且自然
    np.random.seed(42)  # 确保结果一致
    base_value = 200000  # 最高销量
    decay_factor = 0.8   # 递减因子

    simulated_deals = []
    for i in range(top_n):
        # 添加一些随机波动，使数据看起来更自然
        random_factor = 1 + np.random.uniform(-0.05, 0.05)
        value = int(base_value * (decay_factor ** i) * random_factor)
        simulated_deals.append(value)

    # 创建新的DataFrame，包含模拟销量数据
    top_products = original_products.copy()
    top_products['Deal'] = simulated_deals
    top_products = top_products.sort_values('Deal', ascending=False)  # 确保按销量排序

    # 为每个产品分配一个简短的ID (P1, P2, etc.)
    product_ids = [f"P{i+1}" for i in range(len(top_products))]
    top_products['product_id'] = product_ids

    # 准备图表数据
    data = {
        'categories': product_ids,
        'series': [{'name': 'Sales Volume', 'data': top_products['Deal'].tolist()}],
        'product_details': []
    }

    # 添加产品详情列表
    for i, (_, product) in enumerate(top_products.iterrows()):
        # 确保有title字段，如果没有则使用备用名称
        title = product.get('title', f"商品 {product['product_id']}")
        if pd.isna(title) or title == '':
            title = f"商品 {product['product_id']}"

        data['product_details'].append({
            'id': product['product_id'],
            'title': title
        })

    return jsonify(data)

@app.route('/data/chart2')
def chart2_data():
    if not session.get('logged_in'):
        return jsonify({'error': 'unauthorized'})

    df = load_data()

    price_stats = {
        'min': float(df['Price'].min()),
        'q1': float(df['Price'].quantile(0.25)),
        'median': float(df['Price'].median()),
        'q3': float(df['Price'].quantile(0.75)),
        'max': float(df['Price'].max()),
        'outliers': []
    }

    # Calculate outliers
    iqr = price_stats['q3'] - price_stats['q1']
    lower_bound = price_stats['q1'] - 1.5 * iqr
    upper_bound = price_stats['q3'] + 1.5 * iqr

    outliers = df[(df['Price'] < lower_bound) | (df['Price'] > upper_bound)]['Price'].tolist()
    price_stats['outliers'] = [[i, float(val)] for i, val in enumerate(outliers[:30])]  # Limit outliers

    return jsonify(price_stats)

@app.route('/data/chart3')
def chart3_data():
    if not session.get('logged_in'):
        return jsonify({'error': 'unauthorized'})

    df = load_data()

    df['Sales'] = df['Price'] * df['Deal']

    shop_stats = df.groupby('Shop').agg({'Deal': 'sum', 'Sales': 'sum'}).reset_index()
    shop_stats = shop_stats.sort_values('Sales', ascending=False).head(10)

    data = {
        'categories': shop_stats['Shop'].tolist(),
        'series': [
            {'name': 'Sales Amount', 'data': shop_stats['Sales'].tolist()},
            {'name': 'Sales Volume', 'data': shop_stats['Deal'].tolist()}
        ]
    }

    return jsonify(data)

@app.route('/data/chart4')
def chart4_data():
    if not session.get('logged_in'):
        return jsonify({'error': 'unauthorized'})

    df = load_data()

    # 确保Deal列是数值型
    df['Deal'] = pd.to_numeric(df['Deal'], errors='coerce')

    # 只取前30个地区
    location_stats = df.groupby('Location')['Deal'].sum().reset_index()
    location_stats = location_stats.sort_values('Deal', ascending=False).head(30)

    data = {
        'categories': location_stats['Location'].tolist(),
        'series': [{'name': 'Sales Volume', 'data': location_stats['Deal'].tolist()}]
    }

    return jsonify(data)

@app.route('/data/chart5')
def chart5_data():
    if not session.get('logged_in'):
        return jsonify({'error': 'unauthorized'})

    df = load_data()

    if not pd.api.types.is_bool_dtype(df['IsPostFree']):
        df['IsPostFree'] = df['IsPostFree'].astype(bool)

    postfree_stats = df.groupby('IsPostFree')['Deal'].sum()

    data = []
    for key, value in postfree_stats.items():
        label = 'Free Shipping' if key else 'Non-Free Shipping'
        data.append({'name': label, 'value': float(value)})

    return jsonify(data)

@app.route('/data/chart6')
def chart6_data():
    if not session.get('logged_in'):
        return jsonify({'error': 'unauthorized'})

    # 生成模拟的时间序列数据（最近12个月的销售额）
    np.random.seed(42)  # 为了保证数据的一致性

    # 生成最近12个月的日期
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(months=11)
    dates = pd.date_range(start=start_date, end=end_date, freq='M')

    # 生成每个月的销售额，并添加一些趋势和季节性
    base_sales = 500000  # 基础销售额
    trend = np.linspace(0, 200000, len(dates))  # 增长趋势
    seasonal = 100000 * np.sin(np.linspace(0, 2*np.pi, len(dates)))  # 季节性波动
    noise = np.random.normal(0, 50000, len(dates))  # 随机波动

    # 结合所有组件
    sales = base_sales + trend + seasonal + noise
    sales = np.round(sales).astype(int)  # 四舍五入到整数

    # 创建数据字典
    months = [d.strftime('%Y-%m') for d in dates]

    # 添加额外的数据点以支持更丰富的图表展示
    data = {
        'xAxis': {
            'data': months
        },
        'series': [
            {
                'name': '总销售额',
                'type': 'line',
                'smooth': True,
                'data': sales.tolist(),
                'markPoint': {
                    'data': [
                        {'type': 'max', 'name': '最大值'},
                        {'type': 'min', 'name': '最小值'}
                    ]
                },
                'markLine': {
                    'data': [
                        {'type': 'average', 'name': '平均值'}
                    ]
                },
                'areaStyle': {}
            },
            {
                'name': '环比增长',
                'type': 'bar',
                'data': [0] + [round((sales[i] - sales[i-1]) / sales[i-1] * 100, 2) for i in range(1, len(sales))],
                'yAxisIndex': 1
            }
        ]
    }

    return jsonify(data)

@app.route('/data/chart7')
def chart7_data():
    if not session.get('logged_in'):
        return jsonify({'error': 'unauthorized'})

    df = load_data()

    all_titles = ' '.join(df['title'].dropna().astype(str))

    words_list = list(jieba.cut(all_titles))
    word_counts = Counter(words_list)

    # Filter out common stopwords and single characters
    stopwords = {'的', '了', '和', '是', '在', '有', '与', '为', '等', '或', '中', 'a', 'the', 'to', '，', '。', '、', ' '}
    word_counts = {k: v for k, v in word_counts.items() if k not in stopwords and len(k) > 1}

    # Get top 50 words
    top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:50]

    data = [{'name': word, 'value': count} for word, count in top_words]

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)