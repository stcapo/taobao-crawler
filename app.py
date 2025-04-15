from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
import numpy as np
import jieba
from wordcloud import WordCloud
import glob

app = Flask(__name__)
app.secret_key = 'your_secret_key'

os.makedirs('static/images', exist_ok=True)

def clear_old_charts():
    files = glob.glob('static/images/*.png')
    for f in files:
        try:
            os.remove(f)
        except:
            pass

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
    
    clear_old_charts()
    
    return render_template('dashboard.html')

@app.route('/chart1')
def chart1():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    df = load_data()
    top_n = 10
    
    top_products = df.sort_values('Deal', ascending=False).head(top_n)
    
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(top_products)), top_products['Deal'])
    plt.xticks(range(len(top_products)), [f"Product {i+1}" for i in range(len(top_products))], rotation=45)
    plt.title('Top Products by Sales Volume')
    plt.xlabel('Product')
    plt.ylabel('Sales Volume')
    plt.tight_layout()
    
    chart_path = 'static/images/chart1.png'
    plt.savefig(chart_path)
    plt.close()
    
    return jsonify({'chart': chart_path})

@app.route('/chart2')
def chart2():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    df = load_data()
    
    plt.figure(figsize=(10, 6))
    plt.boxplot(df['Price'].dropna())
    plt.title('Price Distribution')
    plt.ylabel('Price')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    chart_path = 'static/images/chart2.png'
    plt.savefig(chart_path)
    plt.close()
    
    return jsonify({'chart': chart_path})

@app.route('/chart3')
def chart3():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    df = load_data()
    
    df['Sales'] = df['Price'] * df['Deal']
    
    shop_stats = df.groupby('Shop').agg({'Deal': 'sum', 'Sales': 'sum'}).reset_index()
    shop_stats = shop_stats.sort_values('Sales', ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    x = range(len(shop_stats))
    ax.bar(x, shop_stats['Sales'], width=0.4, label='Sales Amount', align='center')
    ax.set_xticks(x)
    ax.set_xticklabels(shop_stats['Shop'], rotation=45, ha='right')
    ax.set_title('Top Shops by Sales Amount')
    ax.set_xlabel('Shop')
    ax.set_ylabel('Sales Amount')
    ax.legend()
    plt.tight_layout()
    
    chart_path = 'static/images/chart3.png'
    plt.savefig(chart_path)
    plt.close()
    
    return jsonify({'chart': chart_path})

@app.route('/chart4')
def chart4():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    df = load_data()
    
    location_stats = df.groupby('Location')['Deal'].sum().reset_index()
    location_stats = location_stats.sort_values('Deal', ascending=False)
    
    plt.figure(figsize=(12, 6))
    plt.bar(location_stats['Location'], location_stats['Deal'])
    plt.title('Sales Volume by Location')
    plt.xlabel('Location')
    plt.ylabel('Sales Volume')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    chart_path = 'static/images/chart4.png'
    plt.savefig(chart_path)
    plt.close()
    
    return jsonify({'chart': chart_path})

@app.route('/chart5')
def chart5():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    df = load_data()
    
    if not pd.api.types.is_bool_dtype(df['IsPostFree']):
        df['IsPostFree'] = df['IsPostFree'].astype(bool)
    
    postfree_stats = df.groupby('IsPostFree')['Deal'].sum()
    
    labels = []
    for key in postfree_stats.index:
        if key:
            labels.append('Free Shipping')
        else:
            labels.append('Non-Free Shipping')
    
    plt.figure(figsize=(10, 8))
    plt.pie(postfree_stats, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.title('Sales Volume: Free Shipping vs. Non-Free Shipping')
    plt.axis('equal')
    
    chart_path = 'static/images/chart5.png'
    plt.savefig(chart_path)
    plt.close()
    
    return jsonify({'chart': chart_path})

@app.route('/chart6')
def chart6():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    df = load_data()
    
    df['Sales'] = df['Price'] * df['Deal']
    
    bins = np.linspace(0, df['Sales'].max(), 10)
    labels = [f"{int(bins[i])}-{int(bins[i+1])}" for i in range(len(bins)-1)]
    df['SalesBin'] = pd.cut(df['Sales'], bins=bins, labels=labels, include_lowest=True)
    
    sales_distribution = df.groupby('SalesBin').size().reset_index(name='Count')
    
    plt.figure(figsize=(12, 6))
    plt.bar(sales_distribution['SalesBin'], sales_distribution['Count'])
    plt.title('Sales Amount Distribution')
    plt.xlabel('Sales Amount Range')
    plt.ylabel('Count of Products')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    chart_path = 'static/images/chart6.png'
    plt.savefig(chart_path)
    plt.close()
    
    return jsonify({'chart': chart_path})

@app.route('/chart7')
def chart7():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    df = load_data()
    
    all_titles = ' '.join(df['title'].dropna().astype(str))
    
    words = ' '.join(jieba.cut(all_titles))
    
    try:
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100, 
                             font_path='simhei.ttf').generate(words)
    except:
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100).generate(words)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    
    chart_path = 'static/images/chart7.png'
    plt.savefig(chart_path)
    plt.close()
    
    return jsonify({'chart': chart_path})

if __name__ == '__main__':
    app.run(debug=True)