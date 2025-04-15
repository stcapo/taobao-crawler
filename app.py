from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pandas as pd
import numpy as np
import jieba
import os
from collections import Counter

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_data():
    return pd.read_excel('data.xlsx')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == '123456':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

@app.route('/data/chart1')
def chart1_data():
    if not session.get('logged_in'):
        return jsonify({'error': 'unauthorized'})
    
    df = load_data()
    top_n = 10
    
    top_products = df.sort_values('Deal', ascending=False).head(top_n)
    
    data = {
        'categories': [f"Product {i+1}" for i in range(len(top_products))],
        'series': [{'name': 'Sales Volume', 'data': top_products['Deal'].tolist()}]
    }
    
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
    
    location_stats = df.groupby('Location')['Deal'].sum().reset_index()
    location_stats = location_stats.sort_values('Deal', ascending=False)
    
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
    
    df = load_data()
    
    df['Sales'] = df['Price'] * df['Deal']
    
    bins = np.linspace(0, df['Sales'].max(), 10)
    labels = [f"{int(bins[i])}-{int(bins[i+1])}" for i in range(len(bins)-1)]
    df['SalesBin'] = pd.cut(df['Sales'], bins=bins, labels=labels, include_lowest=True)
    
    sales_distribution = df.groupby('SalesBin').size().reset_index(name='Count')
    
    data = {
        'categories': sales_distribution['SalesBin'].tolist(),
        'series': [{'name': 'Products Count', 'data': sales_distribution['Count'].tolist()}]
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