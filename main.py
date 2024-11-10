import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
import datetime
import pytz
from keep_alive import keep_alive

# Botの初期設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ステータス（プレイ中）表示
@tasks.loop(seconds=20)
async def presence_loop():
    game = discord.Game("/time")
    await bot.change_presence(activity=game)

# 東京時間取得関数
def get_tokyo_time():
    tokyo_tz = pytz.timezone('Asia/Tokyo')
    tokyo_time = datetime.datetime.now(tokyo_tz)
    return tokyo_time.strftime('%Y-%m-%d %H:%M:%S')

# /time コマンド：東京の現在時刻を表示
@bot.tree.command(name="time", description="東京の現在時刻を表示します")
async def time(interaction: discord.Interaction):
    await interaction.response.defer()  # 応答を一時保留
    tokyo_time = get_tokyo_time()
    await interaction.followup.send(f"東京の現在時刻: {tokyo_time}")

# /help コマンド：使い方を表示
@bot.tree.command(name="help", description="ボットの使い方を表示します")
async def bot_help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="ボットの使い方", color=discord.Colour.blurple()
    ).add_field(name="/time", value="東京の現在時刻を表示") \
     .add_field(name="/help", value="コマンドの一覧を表示") \
     .add_field(name="/support", value="サポートサーバーのリンクを表示")
    await interaction.response.send_message(embed=embed)

# /support コマンド：サポートサーバリンクを表示
@bot.tree.command(name="support", description="サポートサーバーのリンクを表示します")
async def support(interaction: discord.Interaction):
    embed = discord.Embed(
        title="サポートサーバー",
        description="[こちらからサポートサーバーに参加できます。](https://discord.gg/r594PHeNNp)",
        color=0xFF0000,
    )
    await interaction.response.send_message(embed=embed)

# Bot起動時の処理
@bot.event
async def on_ready():
    # 重複登録を防ぐためのコマンド同期
    await bot.tree.sync()
    print(f"Logged in as {bot.user.name}")
    # ステータスのループを開始
    presence_loop.start()

# Botを実行
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
