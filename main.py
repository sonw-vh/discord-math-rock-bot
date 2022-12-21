import discord
import asyncio
import os
import google.auth
import google.auth.transport.requests
import google.auth.transport.grpc
import googleapiclient.discovery
import googleapiclient.errors

API_KEY = "API_KEY"

client = discord.Client(intents=discord.Intents.default())

CURRENT_SONG = None
PLAYER = None

channel_id = None

message = None


@client.event
async def on_ready():
    print("The bot is ready as {client.user}!")

@client.event
async def on_message(message):
    if message.content.startswith("g!"):
        args = message.content.split(" ")

        command = args[1]

        if command == "play":
            song_url = args[2]
            await play_song(song_url)

        elif command == "pause":
            await pause_song()

        elif command == "resume":
            await resume_song()

        elif command == "skip":
            await skip_song()

        elif command == "stop":
            await stop_song()

        elif command == "mathrock":
            await play_math_rock_songs()
            
        elif command == "queue":
            await show_queue(message)

queue = []

async def play_song(song_url):
    global CURRENT_SONG, PLAYER, queue
    queue.append(song_url)
    if not (PLAYER and PLAYER.is_playing()):
        CURRENT_SONG = song_url
        voice_client = await client.get_channel(int(channel_id)).connect()
        player = voice_client.create_ytdl_player(song_url)
        PLAYER = player
        player.start()

async def pause_song():
    global PLAYER
    if PLAYER and PLAYER.is_playing():
        PLAYER.pause()

async def resume_song():
    global PLAYER
    if PLAYER and PLAYER.is_paused():
        PLAYER.resume()

async def resume_song():
    global PLAYER
    if PLAYER and PLAYER.is_paused():
        PLAYER.resume()

async def skip_song():
    global PLAYER
    if PLAYER and PLAYER.is_playing():
        PLAYER.stop()

async def stop_song():
    global PLAYER
    if PLAYER and PLAYER.is_playing():
        PLAYER.stop()
    await client.voice_client_in(message.guild).disconnect()

async def show_queue(message):
    global queue
    embed = discord.Embed(title="Queue", description="\n".join(queue), color=0xfae)
    await message.channel.send(embed=embed)

async def play_song_by_keywords(keywords):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    request = youtube.search().list(
        part="id,snippet",
        type="video",
        q=keywords,
        videoDefinition="high",
        maxResults=1,
        fields="items(id(videoId),snippet(publishedAt,channelId,channelTitle,title,description))"
    )
    response = request.execute()

    result = response["items"][0]

    song_url = f"https://www.youtube.com/watch?v={result['id']['videoId']}"

    await play_song(song_url)

async def play_math_rock_songs():
    while client.voice_client_in(message.guild):
        await play_song_by_keywords("math rock")

client.run("BOT_KEY")