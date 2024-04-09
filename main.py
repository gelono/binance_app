import asyncio
from binance import AsyncClient, BinanceSocketManager

from exchange_tools.data_process import DataProcess
from exchange_tools.responses import Response
from variables import PERCENT, PAIRS


class BinanceApp:
    def __init__(self):
        self.client = None
        self.bm = None

    async def main(self):
        self.client = await AsyncClient.create()
        self.bm = BinanceSocketManager(self.client)

        pairs = PAIRS
        tasks = []

        for pair in pairs:
            socket = self.bm.depth_socket(pair)
            dp = DataProcess(PERCENT)
            r = Response(pair, socket, PERCENT, dp)
            task = asyncio.create_task(r.handle_responses())
            tasks.append(task)

        await asyncio.gather(*tasks)

        await self.client.close_connection()


if __name__ == "__main__":
    app = BinanceApp()
    asyncio.run(app.main())
