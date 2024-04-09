from datetime import datetime
from db_tools.db_tools import write_volume
from exchange_tools.data_process import DataProcess
from time_measure.time_measure import measure_time


class Response:
    def __init__(self, pair, socket, percent, dp: DataProcess):
        self.pair = pair
        self.socket = socket
        self.percent = percent
        self.response = None
        self.dp = dp

    @measure_time
    async def handle_responses(self):
        """
        Asynchronous function to handle responses from the exchange socket.

        Returns:
            None

        """
        async with self.socket as tscm:
            while True:
                self.response = await tscm.recv()
                await self.process_response()

    @measure_time
    async def process_response(self):
        """
        Asynchronous function to process the response from the exchange.

        Returns:
            None

        """
        timestamp_ms = self.response['E']
        timestamp = datetime.fromtimestamp(timestamp_ms / 1000.0)

        ask_volume, bid_volume = await self.dp.calculate_volume(self.response)
        await write_volume(self.pair, timestamp, ask_volume, bid_volume)

        await self.dp.check_and_send_messages(self.pair, ask_volume, bid_volume)
        await self.dp.update_ask_volumes_history(ask_volume)
        await self.dp.update_bid_volumes_history(bid_volume)
