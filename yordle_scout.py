import os
from time import sleep
from dotenv import load_dotenv
import tweepy
from tweepy.asynchronous.streaming import AsyncStreamingClient
import discord 


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

twitter_client = tweepy.Client(bearer_token=os.getenv("BEARER_TOKEN"))

@client.event
async def on_ready():
    stream = AsyncStreamingClient(bearer_token=os.getenv("BEARER_TOKEN"))
    # stream rule add to follow LoLDev
    await stream.add_rules(tweepy.StreamRule("from:LoLDev OR from:LeagueOfLegends"))
    stream.filter()
    print('Logged on as {0}!'.format(client.user))
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Running away from Teemo")
    )

class AsyncStreamingClient(tweepy.asynchronous.AsyncStreamingClient):
    async def on_tweet(self, tweet):
        tweet_include = twitter_client.get_tweet(id=tweet.id, expansions=["author_id", "attachments.media_keys"], media_fields=["url"]).includes

        link = "https://www.twitter.com/" + str(tweet_include["users"][-1]) + "/status/" + str(tweet.id)
        channel = client.get_channel(int(os.getenv("GENERAL_CHANNEL")))
        await channel.send(link)
        if "media" in tweet_include:
            for media in tweet_include["media"]:
                if media.type == "photo":
                    await channel.send(media.url)
                if media.type == "video":
                    await channel.send("Tweet has video attachment")

    async def on_connect(self):
        print("Stream has connected")

    async def on_disconnect(self):
        print("Stream has disconnected")

    async def on_connection_error(self):
        print("Stream could not connect")
    

client.run(os.getenv("DISCORD_TOKEN"))