import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import time

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

DATA_FILE = "angel_accounts.json"

# --------------------------
# DATA SYSTEM
# --------------------------

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

daily_cooldown = {}

# --------------------------
# READY + STATUS
# --------------------------

@bot.event
async def on_ready():
    await tree.sync()

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="꒰ 🍵 ꒱ Ami's Angels Bank"
        )
    )

    print(f"🍵 Angel Coins is online as {bot.user}")

# --------------------------
# CREATE ACCOUNT
# --------------------------

@tree.command(name="createaccount", description="Create your Angel Account 🍵")
async def createaccount(interaction: discord.Interaction):
    data = load_data()
    user_id = str(interaction.user.id)

    if user_id in data:
        await interaction.response.send_message("꒰．𓏵． You already have an Angel Account 🍵", ephemeral=True)
        return

    data[user_id] = {
        "name": interaction.user.display_name,
        "username": interaction.user.name,
        "coins": 0
    }

    save_data(data)

    await interaction.response.send_message(
f"""꒰．𓏵． Welcome to your Angel’s Account 🍵

．𓎟𓎟． Your Angel’s account has been created!

ノ．⌢．
𓂃．´ཀ`
ᶻ 𝗓 𐰁 ．

𓏵． Name: {interaction.user.display_name}
𓏵． Username: {interaction.user.name}
𓏵． Starting Balance: 0 Angel Coins 🍵

⩇⩇:⩇⩇ ．Earn Angel Coins by chatting. 🌱

🍵． 🌱． 🍋‍🟩"""
    )

# --------------------------
# BALANCE
# --------------------------

@tree.command(name="balance", description="Check your Angel Coins 🍵")
async def balance(interaction: discord.Interaction):
    data = load_data()
    user_id = str(interaction.user.id)

    if user_id not in data:
        await interaction.response.send_message("꒰．𓏵． No Angel Account Found 🍵 Use /createaccount", ephemeral=True)
        return

    coins = data[user_id]["coins"]

    await interaction.response.send_message(
f"""꒰．𓏵． Angel Wallet 🍵

．𓎟𓎟． Current Balance

𓏵． {coins} Angel Coins 🍵

⩇⩇:⩇⩇ ．Woo hoo! Who doesn't love points? 🌱

◟．ᛝ．

⌣. 𐂯

🍵． 🌱． 🍋‍🟩"""
    )

# --------------------------
# PROFILE
# --------------------------

@tree.command(name="profile", description="View your Angel Profile 🍵")
async def profile(interaction: discord.Interaction):
    data = load_data()
    user_id = str(interaction.user.id)

    if user_id not in data:
        await interaction.response.send_message("Create an account first 🍵 /createaccount", ephemeral=True)
        return

    user = data[user_id]

    await interaction.response.send_message(
f"""꒰．𓏵． Angel Profile 🍵

𓏵． Name: {user['name']}
𓏵． Username: {user['username']}
𓏵． Balance: {user['coins']} Angel Coins 🍵

🍵． 🌱． 🍋‍🟩"""
    )

# --------------------------
# DAILY REWARD
# --------------------------

@tree.command(name="daily", description="Claim daily Angel Coins 🍵")
async def daily(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    now = time.time()

    if user_id in daily_cooldown and now - daily_cooldown[user_id] < 86400:
        await interaction.response.send_message("꒰．𓏵． You already claimed your daily reward 🍵", ephemeral=True)
        return

    data = load_data()

    if user_id not in data:
        await interaction.response.send_message("Create an account first 🍵 /createaccount", ephemeral=True)
        return

    data[user_id]["coins"] += 100
    save_data(data)

    daily_cooldown[user_id] = now

    await interaction.response.send_message(
"""꒰．𓏵． Daily Angel Coins 🍵

𓏵． +100 Angel Coins earned 🌱

⩇⩇:⩇⩇ Come back tomorrow 🍵

🍵． 🌱． 🍋‍🟩"""
    )

# --------------------------
# LEADERBOARD
# --------------------------

@tree.command(name="leaderboard", description="Top Angel Coins holders 🍵")
async def leaderboard(interaction: discord.Interaction):
    data = load_data()
    sorted_users = sorted(data.items(), key=lambda x: x[1]["coins"], reverse=True)

    text = ""
    for i, (_, info) in enumerate(sorted_users[:10], start=1):
        text += f"𓏵． {i}. {info['name']} — {info['coins']} 🍵\n"

    await interaction.response.send_message(
f"""꒰．𓏵． Angel Leaderboard 🍵

{text}

🍵． 🌱． 🍋‍🟩"""
    )

# --------------------------
# USERS LIST
# --------------------------

@tree.command(name="users", description="View all Angel Accounts 🍵")
async def users(interaction: discord.Interaction):
    data = load_data()

    if not data:
        await interaction.response.send_message("꒰．𓏵． No Angel Accounts Found 🍵", ephemeral=True)
        return

    user_list = "\n".join(
        [f"𓏵． {info['name']}" for info in data.values()]
    )

    await interaction.response.send_message(
f"""꒰．𓏵． Angel Account Directory 🍵

．𓎟𓎟． Registered Angel Accounts

{user_list}

⩇⩇:⩇⩇ ．Total Accounts: {len(data)}

🍵． 🌱． 🍋‍🟩"""
    )

# --------------------------
# ADMIN ADD COINS
# --------------------------

@tree.command(name="addcoins", description="Add Angel Coins (Admin)")
async def addcoins(interaction: discord.Interaction, user: discord.Member, amount: int):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("No permission 🍵", ephemeral=True)
        return

    data = load_data()
    uid = str(user.id)

    if uid not in data:
        await interaction.response.send_message("User has no account 🍵", ephemeral=True)
        return

    data[uid]["coins"] += amount
    save_data(data)

    await interaction.response.send_message(
f"꒰．𓏵． Added {amount} Angel Coins to {user.display_name} 🍵"
    )

# --------------------------
# ADMIN REMOVE COINS
# --------------------------

@tree.command(name="removecoins", description="Remove Angel Coins (Admin)")
async def removecoins(interaction: discord.Interaction, user: discord.Member, amount: int):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("No permission 🍵", ephemeral=True)
        return

    data = load_data()
    uid = str(user.id)

    if uid not in data:
        await interaction.response.send_message("User has no account 🍵", ephemeral=True)
        return

    data[uid]["coins"] = max(0, data[uid]["coins"] - amount)
    save_data(data)

    await interaction.response.send_message(
f"꒰．𓏵． Removed {amount} Angel Coins from {user.display_name} 🍵"
    )

# --------------------------
# ADMIN DELETE ACCOUNT
# --------------------------

@tree.command(name="delete", description="Delete Angel Account (Admin)")
async def delete(interaction: discord.Interaction, user: discord.Member):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("No permission 🍵", ephemeral=True)
        return

    data = load_data()
    uid = str(user.id)

    if uid in data:
        del data[uid]
        save_data(data)

    await interaction.response.send_message(
f"꒰．𓏵． Deleted {user.display_name}'s Angel Account 🍵"
    )

# --------------------------
# CHAT REWARDS
# --------------------------

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    data = load_data()
    user_id = str(message.author.id)

    if user_id in data:
        data[user_id]["coins"] += 1
        save_data(data)

    await bot.process_commands(message)

# --------------------------
# RUN BOT
# --------------------------

bot.run(TOKEN)