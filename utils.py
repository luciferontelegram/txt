// ... existing code ...

async def log_to_channel(bot, message):
    """
    Logs a message to the configured log channel.
    Handles errors gracefully if the log channel isn't accessible.
    """
    try:
        log_channel = int(os.environ.get("LOG_CHANNEL", "-1002339598092"))
        await bot.send_message(chat_id=log_channel, text=message)
    except Exception as e:
        print(f"Error logging to channel: {str(e)}")
