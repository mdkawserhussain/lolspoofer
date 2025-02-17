import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta
import logging  # Import logging module

# Set up logging
log_file = os.path.join(os.path.dirname(__file__), "discord_key_bot.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Path to store activation keys
KEYS_FILE = "activation_keys.json"

# Load keys from file or initialize an empty dictionary
def load_keys():
    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.error("Invalid JSON in keys file. Initializing empty keys database.")
            return {}
    return {}

# Save keys to file
def save_keys(keys):
    with open(KEYS_FILE, "w") as f:
        json.dump(keys, f, indent=4)

# Initialize keys database
KEYS_DB = load_keys()

TOKEN = "MTM0MTA0MDY0NzE0NjE3NjU5Mw.Gl7k_l.2q2MXu9gCwQI5Mo60qTpHkrym33AafSORKs0iU"  # Replace with your actual bot token
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}")

@bot.command()
async def genkey(ctx, key_type: str):
    """Generates an activation key of the specified type."""
    new_key = f"{key_type.upper()}-{int(datetime.now().timestamp())}"
    
    if key_type.lower() == "single":
        KEYS_DB[new_key] = {"type": "single", "used": False}
    elif key_type.lower() == "unlimited":
        KEYS_DB[new_key] = {"type": "unlimited"}
    elif key_type.lower() == "time-limited":
        expiry_date = datetime.now() + timedelta(days=7)
        KEYS_DB[new_key] = {"type": "time-limited", "expires": expiry_date.strftime("%Y-%m-%d")}
    else:
        await ctx.send("Invalid key type. Use `single`, `unlimited`, or `time-limited`.")
        return
    
    save_keys(KEYS_DB)
    await ctx.send(f"Generated key: {new_key}")

@bot.command()
async def listkeys(ctx):
    """Lists all available activation keys."""
    if not KEYS_DB:
        await ctx.send("No keys available.")
        return
    message = "Available keys:\n"
    for key, data in KEYS_DB.items():
        status = "Used" if data.get("used", False) else "Active"
        expiry = f" (Expires: {data['expires']})" if "expires" in data else ""
        message += f"{key} - {data['type'].capitalize()} - {status}{expiry}\n"
    await ctx.send(f"```{message}```")

@bot.command()
async def revoke(ctx, key: str):
    """Revokes an existing activation key."""
    if key in KEYS_DB:
        del KEYS_DB[key]
        save_keys(KEYS_DB)
        await ctx.send(f"Key {key} has been revoked.")
    else:
        await ctx.send("Invalid key.")

bot.run(TOKEN)
