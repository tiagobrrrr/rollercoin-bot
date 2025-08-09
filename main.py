import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from bot import RollerCoinBot
from bot_simulator import RollerCoinBotSimulator
from config import Config
import threading
import time

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Global bot instance
bot = None
bot_thread = None
bot_running = False

@app.route('/')
def index():
    """Main dashboard page"""
    global bot, bot_running
    
    # Get bot status
    status = {
        'running': bot_running,
        'email': Config.get_email(),
        'last_run': getattr(bot, 'last_run', None) if bot else None,
        'total_runs': getattr(bot, 'total_runs', 0) if bot else 0,
        'errors': getattr(bot, 'error_count', 0) if bot else 0
    }
    
    return render_template('index.html', status=status)

@app.route('/start', methods=['POST'])
def start_bot():
    """Start the bot"""
    global bot, bot_thread, bot_running
    
    if bot_running:
        flash('Bot is already running!', 'warning')
        return redirect(url_for('index'))
    
    try:
        # Create new bot instance - use simulator for now
        # TODO: Switch back to RollerCoinBot() when Selenium is fixed
        bot = RollerCoinBotSimulator()
        bot_running = True
        
        # Start bot in separate thread
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        
        flash('Bot started successfully!', 'success')
        logging.info('Bot started by user')
        
    except Exception as e:
        flash(f'Error starting bot: {str(e)}', 'danger')
        logging.error(f'Error starting bot: {e}')
        bot_running = False
    
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop_bot():
    """Stop the bot"""
    global bot, bot_running
    
    if not bot_running:
        flash('Bot is not running!', 'warning')
        return redirect(url_for('index'))
    
    try:
        bot_running = False
        if bot:
            bot.stop()
        flash('Bot stopped successfully!', 'success')
        logging.info('Bot stopped by user')
        
    except Exception as e:
        flash(f'Error stopping bot: {str(e)}', 'danger')
        logging.error(f'Error stopping bot: {e}')
    
    return redirect(url_for('index'))

@app.route('/config', methods=['GET', 'POST'])
def config():
    """Configuration page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email and password:
            Config.set_credentials(email, password)
            flash('Configuration updated successfully!', 'success')
        else:
            flash('Please provide both email and password!', 'danger')
        
        return redirect(url_for('index'))
    
    return render_template('config.html')

@app.route('/logs')
def logs():
    """View bot logs"""
    try:
        with open('bot.log', 'r') as f:
            log_content = f.read()
        return render_template('logs.html', logs=log_content)
    except FileNotFoundError:
        return render_template('logs.html', logs='No logs available yet.')

@app.route('/api/status')
def api_status():
    """API endpoint for real-time status"""
    global bot, bot_running
    
    status = {
        'running': bot_running,
        'last_run': getattr(bot, 'last_run', None) if bot else None,
        'total_runs': getattr(bot, 'total_runs', 0) if bot else 0,
        'errors': getattr(bot, 'error_count', 0) if bot else 0,
        'current_action': getattr(bot, 'current_action', 'Idle') if bot else 'Idle'
    }
    
    return jsonify(status)

@app.route('/download')
def download_bot():
    """Download page with bot files"""
    return render_template('download.html')

@app.route('/download/rollercoin-bot.zip')
def download_zip():
    """Download the complete bot as ZIP file"""
    import zipfile
    import tempfile
    import shutil
    
    try:
        # Create temporary zip file
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all Python files
            files_to_include = [
                'main.py',
                'bot.py', 
                'bot_simulator.py',
                'config.py',
                'README.md',
                'pyproject.toml'
            ]
            
            for file in files_to_include:
                if os.path.exists(file):
                    zipf.write(file)
            
            # Add templates
            if os.path.exists('templates'):
                for root, dirs, files in os.walk('templates'):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path)
            
            # Add static files
            if os.path.exists('static'):
                for root, dirs, files in os.walk('static'):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path)
        
        return send_file(temp_zip.name, 
                        as_attachment=True, 
                        download_name='rollercoin-bot-complete.zip',
                        mimetype='application/zip')
                        
    except Exception as e:
        logging.error(f'Error creating zip file: {e}')
        flash('Error creating download file', 'danger')
        return redirect(url_for('index'))

def run_bot():
    """Run the bot in a loop"""
    global bot, bot_running
    
    while bot_running and bot:
        try:
            bot.run_cycle()
            if bot_running:  # Check if still running after cycle
                time.sleep(Config.get_cycle_interval())
        except Exception as e:
            logging.error(f'Error in bot cycle: {e}')
            if bot:
                bot.error_count += 1
            time.sleep(60)  # Wait longer on error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
