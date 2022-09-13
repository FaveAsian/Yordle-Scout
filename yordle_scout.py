import os
from dotenv import load_dotenv
import tweepy
from tweepy.asynchronous.streaming import AsyncStream
import discord 

client = discord.Client()
load_dotenv()


@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Running away from Teemo")
    )


class AsyncStream(tweepy.asynchronous.AsyncStream):
    async def on_status(self, status):
        # Checks to make sure the user is actually @LoLDev
        if status.user.id == 1405644969675681794:
            # creates the url to be posted to discord
            link = "https://www.twitter.com/" + status.user.screen_name + "/status/" + status.id_str
            channel = client.get_channel(int(os.getenv("CHANNEL")))
            await channel.send(link)

    async def on_disconnect_message(self, message):
        print("Stream has disconnected: " + message)

    async def on_connection_error(self):
        print("Stream could not connect")

# Start the stream
stream = AsyncStream(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_KEY_SECRET"),
                     os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
# Follows the @LoLDev (follow=["1405644969675681794"])
stream.filter(follow=["1405644969675681794"])
client.run(os.getenv("DISCORD_TOKEN"))