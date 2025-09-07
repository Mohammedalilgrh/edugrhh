import os
import json
import logging
from flask import Flask, request, Response, jsonify
from flask_socketio import SocketIO
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Set environment variables directly in the file
os.environ['TEACHER_ID'] = '6968612778'  # Replace with your Telegram user ID
os.environ['BOT_TOKEN'] = '8388497886:AAHYfD-OJ6Ka4vh1KF4N0-0T-Aos6Gp2wfQ'  # Replace with your bot token
os.environ['API_ID'] = '21706160'  # Replace with your Telegram API ID
os.environ['API_HASH'] = '548b91f0e7cd2e44bbee05190620d9f4'  # Replace with your Telegram API hash
os.environ['RENDER_EXTERNAL_HOSTNAME'] = 'your-app-name.onrender.com'  # Replace with your Render app URL

# Initialize SocketIO
socketio = SocketIO(
    app,
    async_mode='eventlet',
    cors_allowed_origins="*",
    logger=False,
    engineio_logger=False
)

# State management
hand_requests = set()
teacher_ws = None
student_connections = {}

# Function to set webhook
def set_webhook():
    webhook_url = f"{BASE_URL}/webhook/{BOT_TOKEN}"
    logger.info(f"Setting webhook to: {webhook_url}")
    response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}")
    if response.status_code == 200 and response.json().get('ok'):
        logger.info("Webhook set successfully")
    else:
        logger.error(f"Failed to set webhook: {response.json()}")

# Health check endpoint for Render.com
@app.route('/health')
def health():
    """Health check endpoint for Render.com"""
    return jsonify({"status": "ok", "environment": "production"}), 200

# Telegram webhook endpoint
@app.route(f'/webhook/{BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    """Handle Telegram bot updates"""
    try:
        update = request.json
        logger.info(f"Received update: {json.dumps(update)}")
        
        # Handle commands
        if 'message' in update and 'text' in update['message']:
            chat_id = update['message']['chat']['id']
            text = update['message']['text']
            
            if text == '/start':
                response = {
                    "method": "sendMessage",
                    "chat_id": chat_id,
                    "text": "Welcome to EduClass! 🎓\n\nClick the menu button below to open the classroom.",
                    "reply_markup": {
                        "inline_keyboard": [[
                            {"text": "Open Classroom", "web_app": {"url": f"{BASE_URL}/miniapp"}}
                        ]]
                    }
                }
                return jsonify(response)
                
        return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f"Error handling webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Mini App HTML (fully embedded)
MINI_APP_HTML = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EduClass - Professional Smartboard</title>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ 
      margin: 0; 
      font-family: -apple-system, system-ui, sans-serif; 
      background: #f8f9fa;
      color: #212529;
      min-height: 100vh;
      padding-bottom: 70px;
    }}
    .container {{
      max-width: 800px;
      margin: 0 auto;
      padding: 15px;
    }}
    #canvas {{ 
      display: none;
      width: 100%; 
      height: 70vh; 
      background: white; 
      border-radius: 8px;
      margin: 15px 0;
      border: 1px solid #dee2e6;
      touch-action: none;
    }}
    .alert {{ 
      background: #4cc9f0; 
      color: #000; 
      padding: 16px; 
      border-radius: 8px; 
      text-align: center;
      font-weight: bold;
      margin: 10px 0;
      display: none;
      animation: pulse 2s infinite;
      cursor: pointer;
    }}
    @keyframes pulse {{ 
      0% {{ box-shadow: 0 0 0 0 rgba(76, 201, 240, 0.7); }}
      70% {{ box-shadow: 0 0 0 12px rgba(76, 201, 240, 0); }}
      100% {{ box-shadow: 0 0 0 0 rgba(76, 201, 240, 0); }}
    }}
    .controls {{ 
      padding: 15px; 
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }}
    button {{
      width: 100%;
      padding: 14px;
      margin: 8px 0;
      border: none;
      border-radius: 8px;
      font-weight: 600;
      font-size: 16px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    #hand-btn {{
      background: #4361ee;
      color: white;
    }}
    #clear-btn {{
      background: #e63946;
      color: white;
      display: none;
    }}
    .teacher-only {{ display: none; }}
    .student-only {{ display: block; }}
    .compliance-banner {{
      background: #d4edda;
      color: #155724;
      padding: 10px;
      border-radius: 5px;
      margin-bottom: 15px;
      text-align: center;
    }}
    footer {{
      position: fixed;
      bottom: 0;
      width: 100%;
      background: white;
      padding: 10px;
      text-align: center;
      box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }}
  </style>
</head>
<body>
  <div class="compliance-banner">
    <strong>NTA COMPLIANCE NOTICE</strong><br>
    This service is compliant with Section 121 of Civil Criminal Code 2074.
  </div>
  
  <div class="container">
    <div id="hand-alert" class="alert">
      🙋 <span id="request-count">0</span> student(s) raising hand!
    </div>
    
    <canvas id="canvas" width="800" height="500"></canvas>
    
    <div class="controls">
      <button id="hand-btn" class="student-only">Raise Hand ✋</button>
      <button id="clear-btn" class="teacher-only">Clear Board</button>
      
      <div class="teacher-only">
        <button id="mute-btn" style="background:#adb5bd">
          MUTE ALL STUDENTS
        </button>
        <p style="font-size:0.85rem; color:#6c757d; margin-top:8px">
          🔒 You're the only speaker! Students must raise hands to talk.
        </p>
      </div>
    </div>
  </div>
  
  <footer>
    <p>EduClass &copy; 2023 | Professional Smartboard for Teaching</p>
  </footer>

  <script>
    Telegram.WebApp.expand();
    Telegram.WebApp.setHeaderColor('#ffffff');
    Telegram.WebApp.setBackgroundColor('#f5f5f5');
    
    // Get user data
    const user = Telegram.WebApp.initDataUnsafe.user;
    if (!user) {{
      document.body.innerHTML = `
        <div style="padding:20px; text-align:center;">
          <h2>⚠️ ERROR</h2>
          <p>This app must be opened from Telegram</p>
          <p>Please go back to Telegram and try again</p>
        </div>
      `;
      setTimeout(() => Telegram.WebApp.close(), 5000);
      throw new Error("Not opened from Telegram");
    }}
    
    // Connect to WebSocket
    const wsUrl = "{BASE_URL.replace('https', 'wss')}/ws";
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {{
      ws.send(JSON.stringify({{ 
        type: 'auth', 
        user_id: user.id 
      }}));
    }};
    
    ws.onerror = (error) => {{
      console.error("WebSocket error:", error);
      document.body.innerHTML = `
        <div style="padding:20px; text-align:center;">
          <h2>⚠️ CONNECTION ERROR</h2>
          <p>Could not connect to classroom server</p>
          <p>Please try again later</p>
        </div>
      `;
    }};

    // TEACHER VIEW
    if (user.id == {TEACHER_ID}) {{
      document.querySelectorAll('.teacher-only').forEach(el => {{
        el.style.display = 'block';
      }});
      document.querySelectorAll('.student-only').forEach(el => {{
        el.style.display = 'none';
      }});
      document.getElementById('canvas').style.display = 'block';
      
      const canvas = document.getElementById('canvas');
      const ctx = canvas.getContext('2d');
      let isDrawing = false;
      
      // Drawing setup
      const setupDrawing = () => {{
        canvas.addEventListener('touchstart', e => {{
          e.preventDefault();
          isDrawing = true;
          const rect = canvas.getBoundingClientRect();
          const x = e.touches[0].clientX - rect.left;
          const y = e.touches[0].clientY - rect.top;
          ctx.beginPath();
          ctx.moveTo(x, y);
          ws.send(JSON.stringify({{ 
            type: 'draw', 
            x, 
            y, 
            start: true 
          }}));
        }});
        
        canvas.addEventListener('touchmove', e => {{
          e.preventDefault();
          if (!isDrawing) return;
          const rect = canvas.getBoundingClientRect();
          const x = e.touches[0].clientX - rect.left;
          const y = e.touches[0].clientY - rect.top;
          ctx.lineTo(x, y);
          ctx.stroke();
          ws.send(JSON.stringify({{ 
            type: 'draw', 
            x, 
            y 
          }}));
        }});
        
        canvas.addEventListener('touchend', () => {{
          isDrawing = false;
          ctx.beginPath();
        }});
        
        canvas.addEventListener('mousedown', e => {{
          isDrawing = true;
          const rect = canvas.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          ctx.beginPath();
          ctx.moveTo(x, y);
          ws.send(JSON.stringify({{ 
            type: 'draw', 
            x, 
            y, 
            start: true 
          }}));
        }});
        
        canvas.addEventListener('mousemove', e => {{
          if (!isDrawing) return;
          const rect = canvas.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          ctx.lineTo(x, y);
          ctx.stroke();
          ws.send(JSON.stringify({{ 
            type: 'draw', 
            x, 
            y 
          }}));
        }});
        
        canvas.addEventListener('mouseup', () => {{
          isDrawing = false;
          ctx.beginPath();
        }});
      }};
      
      setupDrawing();
      
      // Clear board
      document.getElementById('clear-btn').addEventListener('click', () => {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ws.send(JSON.stringify({{ 
          type: 'clear' 
        }}));
      }});
      
      // Hand alert handling
      document.getElementById('hand-alert').addEventListener('click', () => {{
        ws.send(JSON.stringify({{ 
          type: 'clear_hand' 
        }}));
        document.getElementById('hand-alert').style.display = 'none';
      }});
    }}
    // STUDENT VIEW
    else {{
      document.getElementById('hand-btn').addEventListener('click', () => {{
        ws.send(JSON.stringify({{ 
          type: 'hand' 
        }}));
        const btn = document.getElementById('hand-btn');
        btn.innerHTML = "Hand Raised! ✅ (Wait for teacher)";
        btn.disabled = true;
        btn.style.background = "#4CAF50";
        
        setTimeout(() => {{
          btn.innerHTML = "Raise Hand ✋";
          btn.disabled = false;
          btn.style.background = "#4361ee";
        }}, 5000);
      }});
    }}

    // Handle messages from server
    ws.addEventListener('message', e => {{
      try {{
        const data = JSON.parse(e.data);
        
        if (data.type === 'hand_update') {{
          document.getElementById('request-count').textContent = data.count;
          if (data.count > 0 && user.id == {TEACHER_ID}) {{
            document.getElementById('hand-alert').style.display = 'block';
            Telegram.WebApp.HapticFeedback.notificationOccurred('success');
          }}
        }}
        else if (data.type === 'draw') {{
          if (user.id == {TEACHER_ID} || document.getElementById('canvas').style.display === 'none') return;
          
          const canvas = document.getElementById('canvas');
          const ctx = canvas.getContext('2d');
          
          if (data.start) {{
            ctx.beginPath();
            ctx.moveTo(data.x, data.y);
          }} else {{
            ctx.lineTo(data.x, data.y);
            ctx.stroke();
          }}
        }}
        else if (data.type === 'clear') {{
          if (user.id == {TEACHER_ID}) return;
          
          const canvas = document.getElementById('canvas');
          const ctx = canvas.getContext('2d');
          ctx.clearRect(0, 0, canvas.width, canvas.height);
        }}
      }} catch (err) {{
        console.error("Error processing message:", err);
      }}
    }});
  </script>
</body>
</html>
"""

@app.route('/miniapp')
def miniapp():
    """Serve the mini app"""
    return Response(MINI_APP_HTML, mimetype='text/html')

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    student_connections[request.sid] = None

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    user_id = student_connections.get(request.sid)
    if user_id and user_id != TEACHER_ID:
        hand_requests.discard(user_id)
    student_connections.pop(request.sid, None)

@socketio.on('message')
def handle_message(data):
    """Handle WebSocket messages"""
    global teacher_ws
    try:
        msg = json.loads(data)
        user_id = student_connections.get(request.sid)
        
        if msg['type'] == 'auth':
            user_id = msg['user_id']
            student_connections[request.sid] = user_id
            if user_id == TEACHER_ID:
                teacher_ws = request.sid
                socketio.emit('hand_update', {'count': len(hand_requests)}, room=request.sid)
            return

        # Hand raising (students only)
        if msg['type'] == 'hand' and user_id != TEACHER_ID:
            hand_requests.add(user_id)
            if teacher_ws:
                socketio.emit('hand_update', {'count': len(hand_requests)}, room=teacher_ws)
        
        # Teacher actions
        elif user_id == TEACHER_ID:
            if msg['type'] == 'clear_hand':
                hand_requests.clear()
                socketio.emit('hand_update', {'count': 0})
            elif msg['type'] == 'draw':
                socketio.emit('message', data, include_self=False)
            elif msg['type'] == 'clear':
                socketio.emit('message', data, include_self=False)
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")

# Required for Render.com
if __name__ == '__main__':
    # Set webhook when the app starts
    set_webhook()
    
    # Start the Flask app
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting server on port {port}")
    socketio.run(app, host='0.0.0.0', port=port)
