import asyncio
import discord

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

TOKEN = 'MTEyNTg4MDYwMDMzMTU1ODkxMg.Gsqbs6.84wvzEY3HfeRRKrfR1FTyQwOjqg3km5mGHMiZs'
GUILD_ID = 1125880453090513039  # Replace with your guild ID
CHANNELS_PER_BATCH = 3
DELAY_BETWEEN_BATCHES = 1  # Delay in seconds between each batch

async def create_channels(guild, batch_size):
    for i in range(1, batch_size + 1):
        tasks = []
        for j in range(1, CHANNELS_PER_BATCH + 1):
            tasks.append(guild.create_text_channel(f'Channel{j + ((i-1) * CHANNELS_PER_BATCH)}'))

        await asyncio.gather(*tasks)
        await asyncio.sleep(DELAY_BETWEEN_BATCHES)

async def main():
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name} ({bot.user.id})')
        guild = bot.get_guild(GUILD_ID)
        if guild is not None:
            print(f'Creating channels in {guild.name} ({guild.id})')

            # Calculate the number of iterations required based on CHANNELS_PER_BATCH
            iterations = 500 // CHANNELS_PER_BATCH
            for i in range(iterations):
                await create_channels(guild, CHANNELS_PER_BATCH)

            # Create any remaining channels (if not a multiple of CHANNELS_PER_BATCH)
            remaining_channels = 500 % CHANNELS_PER_BATCH
            if remaining_channels > 0:
                await create_channels(guild, remaining_channels)

        else:
            print(f'Guild with ID {GUILD_ID} not found.')

        await bot.logout()

    await bot.login(TOKEN)
    await bot.connect()

asyncio.run(main())
