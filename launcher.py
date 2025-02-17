import threading
import time
import logging  # Import logging module
import os
import sys
from project.key_validation_server import app as flask_app
from project.discord_key_bot import bot
import project.spoofer_client as spoofer_client

# Set up logging
log_file = os.path.join(os.path.dirname(sys.executable), "launcher.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to run the Flask server
def run_flask():
    try:
        flask_app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        logging.error(f"Error running Flask server: {e}")

# Function to run the Discord bot
def run_discord_bot():
    try:
        bot.run("YOUR_DISCORD_BOT_TOKEN")  # Replace with your actual bot token
    except Exception as e:
        logging.error(f"Error running Discord bot: {e}")

# Main function to start all components
if __name__ == "__main__":
    try:
        # Start Flask server in a separate thread
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        time.sleep(2)  # Give the server time to start

        # Start Discord bot in a separate thread
        discord_thread = threading.Thread(target=run_discord_bot, daemon=True)
        discord_thread.start()
        time.sleep(2)

        # Run the spoofer client
        spoofer_client.main()  # Ensure spoofer_client has a `main()` function
    except Exception as e:
        logging.error(f"Error in launcher: {e}")