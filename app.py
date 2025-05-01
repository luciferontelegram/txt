import os
import sys
import subprocess
from threading import Thread

def run_bot():
    """Run the main bot process."""
    try:
        # Print for debugging
        print("Starting bot...")
        
        # Run the main.py file
        subprocess.run([sys.executable, "main.py"])
    except Exception as e:
        print(f"Error running bot: {e}")

if __name__ == "__main__":
    # Start the bot in a separate thread
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True  # Allow the thread to exit when the main process exits
    bot_thread.start()
    
    # Keep the main thread alive (Koyeb requires the process to stay alive)
    print("Bot started in background. Keeping main process alive...")
    try:
        # This keeps the main process alive
        bot_thread.join()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
