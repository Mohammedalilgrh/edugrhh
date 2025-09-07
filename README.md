# EduClass - Professional Telegram Classroom System

A complete classroom solution for Telegram that works as a Mini App. Perfect for teaching students with real-time smartboard and hand-raising features.

## Features

- 🖼️ Real-time smartboard for teachers
- ✋ Hand-raising system for students
- 🔒 Teacher-controlled voice permissions
- 📱 Works on all devices through Telegram
- 🌐 Fully compliant with Nepal Telecommunications Authority regulations

## Setup Guide

### 1. Create GitHub Repository

1. Create a new GitHub repository
2. Clone it to your local machine or Termux
3. Add the files from this project

### 2. Deploy to Render.com

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Sign up for [Render.com](https://render.com) (free)
2. Click "New +" → "Web Service" → "GitHub"
3. Select your repository
4. Configure as follows:
   - **Name**: edugrh-classroom
   - **Region**: Oregon
   - **Branch**: main
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --worker-class eventlet -w 1 edugrh:app`
   - **Port**: 5000
5. Set environment variables:
   - `TEACHER_ID`: 6968612778
   - `BOT_TOKEN`: 8388497886:AAHYfD-OJ6Ka4vh1KF4N0-0T-Aos6Gp2wfQ
   - `API_ID`: 21706160
   - `API_HASH`: 548b91f0e7cd2e44bbee05190620d9f4
6. Click "Create Web Service"

### 3. Configure Telegram Bot

1. Go to [@BotFather](https://t.me/BotFather)
2. Send `/setmenubutton` to BotFather
3. Select your bot
4. Set menu button to:
   - **Type**: `WebView`
   - **URL**: `https://edugrh-classroom.onrender.com/miniapp` (use YOUR Render URL)

### 4. Configure Group Permissions

1. Open your group `@edugrh`
2. Group Settings → Permissions
3. **DISABLE ALL** for members:
   - ❌ Send Messages
   - ❌ Send Media
   - ❌ Voice Messages
   - ❌ Add Users
4. *Students can ONLY join voice chat*

## Teaching Workflow

1. **Start voice chat** in your group → Mute All
2. **Open classroom** via menu button
3. **Draw on smartboard** - students see in real-time
4. **Students raise hands** - you get alerts
5. **Unmute students** when they need to speak

## Why This Works in Nepal

- Uses **Render.com** (NOT blocked by Nepal Telecommunications Authority)
- Fully compliant with Nepal's regulations
- No ngrok or blocked services required
- Works through Telegram's approved Mini App system
- No special permissions needed

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Mini app won't open | Verify your Render.com URL is correct in BotFather |
| Students can't see drawings | Check all devices have internet connection |
| Hand raises not showing | Verify TEACHER_ID is correct in Render environment |
| WebSocket errors | Wait a few minutes after deployment |
| Connection timeout | Restart the Render service from dashboard |
