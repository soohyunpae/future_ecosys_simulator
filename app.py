from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
import pytz
from collections import Counter
import sys
import io

# LED 관련 임포트를 주석 처리
# import board
# import neopixel

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)

# LED 초기화 코드를 주석 처리
# pixels = neopixel.NeoPixel(board.D18, 30, brightness=0.2, auto_write=False)

def init_db():
    conn = sqlite3.connect('ideas.db', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.text_factory = str
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ideas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 idea TEXT NOT NULL,
                 category TEXT NOT NULL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_all_ideas():
    conn = sqlite3.connect('ideas.db', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("SELECT * FROM ideas ORDER BY timestamp DESC")
    ideas = c.fetchall()
    conn.close()
    return ideas

def analyze_ideas(ideas):
    all_text = ' '.join([idea[1] for idea in ideas])
    words = all_text.lower().split()
    common_words = Counter(words).most_common(10)
    category_counts = Counter([idea[2] for idea in ideas])
    time_distribution = Counter([idea[3].split()[1].split(':')[0] for idea in ideas])
    return {
        'common_words': common_words,
        'category_counts': dict(category_counts),
        'time_distribution': dict(time_distribution)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        idea = request.form['idea']
        category = request.form['category']
        local_time = datetime.now(pytz.timezone('Asia/Seoul'))
        conn = sqlite3.connect('ideas.db', detect_types=sqlite3.PARSE_DECLTYPES)
        conn.text_factory = str
        c = conn.cursor()
        c.execute("INSERT INTO ideas (idea, category, timestamp) VALUES (?, ?, ?)",
                  (idea, category, local_time.strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

    ideas = get_all_ideas()
    local_tz = pytz.timezone('Asia/Seoul')
    ideas = [(idea[0], idea[1], idea[2],
              datetime.strptime(idea[3], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC).astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S'))
             for idea in ideas]
    analysis_results = analyze_ideas(ideas)

    # LED 패턴 생성 및 적용 코드를 주석 처리
    # category_counts = analysis_results['category_counts']
    # total_ideas = sum(category_counts.values())
    # led_pattern = []
    # for category, count in category_counts.items():
    #     ratio = count / total_ideas if total_ideas > 0 else 0
    #     if category == 'Environment':
    #         color = (0, 255, 0)  # Green
    #     elif category == 'Technology':
    #         color = (0, 0, 255)  # Blue
    #     elif category == 'Society':
    #         color = (255, 255, 0)  # Yellow
    #     elif category == 'Culture':
    #         color = (255, 0, 255)  # Purple
    #     else:
    #         color = (255, 255, 255)  # White
    #     led_pattern.extend([color] * int(30 * ratio))
    # 
    # led_pattern = led_pattern[:30]
    # if len(led_pattern) < 30:
    #     led_pattern.extend([(0, 0, 0)] * (30 - len(led_pattern)))
    # 
    # pixels.fill((0, 0, 0))
    # for i, color in enumerate(led_pattern):
    #     pixels[i] = color
    # pixels.show()

    return render_template('index.html', ideas=ideas, analysis_results=analysis_results)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_idea(id):
    conn = sqlite3.connect('ideas.db', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("DELETE FROM ideas WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/change_led', methods=['POST'])
def change_led():
    category = request.json['category']
    # LED 변경 코드를 주석 처리
    # if category == 'Environment':
    #     pattern = [(0, 255, 0)] * 30  # Green
    # elif category == 'Technology':
    #     pattern = [(0, 0, 255)] * 30  # Blue
    # elif category == 'Society':
    #     pattern = [(255, 255, 0)] * 30  # Yellow
    # elif category == 'Culture':
    #     pattern = [(255, 0, 255)] * 30  # Purple
    # else:
    #     pattern = [(0, 0, 0)] * 30  # Off
    # 
    # for i, color in enumerate(pattern):
    #     pixels[i] = color
    # pixels.show()
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
