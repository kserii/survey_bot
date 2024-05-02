import asyncio
from logging import getLogger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from survey_bot.const import MONGO_CONNECTION_URL


logger = getLogger(__name__)

async def ping_server():
    # Replace the placeholder with your Atlas connection string
    uri = MONGO_CONNECTION_URL
    # Set the Stable API version when creating a new client
    client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        await client.admin.command('ping')
        logger.debug("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        logger.exception(e)
