import sqlite3
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# DB Initialization
def init_db():
    conn = sqlite3.connect('swarm_node.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS earnings (
            worker_id TEXT PRIMARY KEY,
            tasks_completed INTEGER,
            tokens REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completed_tasks (
            task_id INTEGER PRIMARY KEY,
            worker_id TEXT,
            task_type TEXT,
            result_summary TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

pending_tasks = [
    {"task_id": 1, "type": "text", "data": "SwarmNode AI optimizes idle compute power efficiently."},
    {"task_id": 2, "type": "image_data", "data": "image_raw_bytes_4096_jpg"},
    {"task_id": 3, "type": "text", "data": "Critical error connection timeout in cluster node."},
    {"task_id": 4, "type": "image_data", "data": "high_res_photo_1080p_png"},
    {"task_id": 5, "type": "text", "data": "Distributed edge nodes save bandwidth and cloud server costs."}
]

HTML_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <title>SwarmNode Ultimate Persistent AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: white; padding: 20px; }
        .card { background: #1e293b; border-radius: 10px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h1 { color: #38bdf8; text-align: center; }
        .status { color: #22c55e; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 10px; border: 1px solid #334155; text-align: left; }
        th { background: #0284c7; }
        .token { color: #fbbf24; font-weight: bold; }
    </style>
    <script>setTimeout(function(){ location.reload(); }, 3000);</script>
</head>
<body>
    <h1>🌐 SwarmNode Persistent Ecosystem</h1>
    <div class="card">
        <h3>Server Status: <span class="status">ONLINE (SQLite Active)</span></h3>
        <p>Pending Tasks in Queue: <b>{{ pending_count }}</b></p>
    </div>

    <div class="card">
        <h3>💰 Active Worker Node Wallets (Saved to DB)</h3>
        <table>
            <tr>
                <th>Worker ID</th>
                <th>Tasks Completed</th>
                <th>Total Earned Balance</th>
            </tr>
            {% for w in earnings %}
            <tr>
                <td><b>{{ w[0] }}</b></td>
                <td>{{ w[1] }}</td>
                <td class="token">{{ w[2] }} SWARM Tokens ($)</td>
            </tr>
            {% else %}
            <tr><td colspan="3">No active worker nodes registered yet.</td></tr>
            {% endfor %}
        </table>
    </div>
    
    <div class="card">
        <h3>⚡ Persistent Processed Workloads</h3>
        <table>
            <tr>
                <th>Task ID</th>
                <th>Worker ID</th>
                <th>Type</th>
                <th>Result Summary</th>
            </tr>
            {% for t in completed %}
            <tr>
                <td>Task #{{ t[0] }}</td>
                <td><b>{{ t[1] }}</b></td>
                <td>{{ t[2] }}</td>
                <td>{{ t[3] }}</td>
            </tr>
            {% else %}
            <tr><td colspan="4">No tasks processed yet.</td></tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    conn = sqlite3.connect('swarm_node.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM earnings')
    earnings = cursor.fetchall()
    cursor.execute('SELECT * FROM completed_tasks')
    completed = cursor.fetchall()
    conn.close()
    
    return render_template_string(
        HTML_DASHBOARD, 
        pending_count=len(pending_tasks), 
        completed=completed,
        earnings=earnings
    )

@app.route('/get_task', methods=['GET'])
def get_task():
    if pending_tasks:
        task = pending_tasks.pop(0)
        return jsonify({"status": "available", "task": task})
    else:
        return jsonify({"status": "empty", "message": "No pending tasks"})

@app.route('/submit_result', methods=['POST'])
def submit_result():
    data = request.get_json()
    task_id = data.get("task_id")
    worker_id = data.get("worker_id", "Node-Unknown")
    task_type = data.get("type")
    result = str(data.get("result"))
    
    conn = sqlite3.connect('swarm_node.db')
    cursor = conn.cursor()
    
    # Save completed task
    cursor.execute('INSERT OR REPLACE INTO completed_tasks VALUES (?, ?, ?, ?)', 
                   (task_id, worker_id, task_type, result))
    
    # Update earnings
    cursor.execute('SELECT tasks_completed, tokens FROM earnings WHERE worker_id = ?', (worker_id,))
    row = cursor.fetchone()
    if row:
        new_count = row[0] + 1
        new_tokens = row[1] + 10.0
        cursor.execute('UPDATE earnings SET tasks_completed = ?, tokens = ? WHERE worker_id = ?', 
                       (new_count, new_tokens, worker_id))
    else:
        cursor.execute('INSERT INTO earnings VALUES (?, ?, ?)', (worker_id, 1, 10.0))
        
    conn.commit()
    conn.close()
    
    print(f"[✓] Task {task_id} saved to SQLite DB by [{worker_id}]!")
    return jsonify({"status": "success", "reward": 10.0})

if __name__ == '__main__':
    print("Master AI Server running on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000)

