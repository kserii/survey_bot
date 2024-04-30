import os
import time

import asyncio

from survey_bot.utils.mongodb import ping_server


if __name__ == '__main__':
    print(*[f'{k}={v}' for k, v in os.environ.items()], sep='\n')

    asyncio.run(ping_server())
    while True:
        time.sleep(5)
        print(time.time())
