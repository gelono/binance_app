from collections import deque
from statistics import mean

from time_measure.time_measure import measure_time
from variables import PERIOD_SEC, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, KOEF
from telegram import Bot


class DataProcess:
    def __init__(self, percent):
        self.percent = percent
        self.ask_volumes_history = deque(maxlen=PERIOD_SEC)
        self.bid_volumes_history = deque(maxlen=PERIOD_SEC)

    @measure_time
    async def calculate_volume(self, data):
        """
        Asynchronous function to calculate the total ask and bid volumes based on the provided data.

        Args:
            data (dict): The data containing ask and bid information.

        Returns:
            Tuple[float, float]: The total ask volume and total bid volume.

        """

        # Obtaining asks and bids from data
        asks = tuple(data['a'])
        bids = tuple(data['b'])

        # Initial price
        start_price = (float(asks[0][0]) + float(bids[0][0])) / 2

        # Search for prices that match the ask condition
        end_ask_price = start_price * (1 + self.percent/100)
        total_ask_volume = 0
        for ask in asks:
            price = float(ask[0])
            if price >= end_ask_price:
                break
            total_ask_volume += float(ask[1])

        # Search for prices that match the bid condition
        end_bid_price = start_price * (1 - self.percent/100)
        total_bid_volume = 0
        for bid in bids:
            price = float(bid[0])
            if price <= end_bid_price:
                break
            total_bid_volume += float(bid[1])

        return total_ask_volume, total_bid_volume

    @measure_time
    async def check_and_send_messages(self, pair, ask_volume, bid_volume):
        """
        Asynchronous function to compare the latest total volume with the weighted average volume over a specified period.

        Args:
            pair (str): The trading pair for which volumes are compared.
            ask_volume (float): The latest total volume on asks.
            bid_volume (float): The latest total volume on bids.

        Returns:
            None

        """

        # Calculate the weighted average of volumes over the last established period
        avg_ask_volume = mean(self.ask_volumes_history) if len(self.ask_volumes_history) else 0
        avg_bid_volume = mean(self.bid_volumes_history) if len(self.bid_volumes_history) else 0

        # Compare the latest total volumes with weighted averages
        if ask_volume > (avg_ask_volume * KOEF) and len(self.ask_volumes_history) == PERIOD_SEC:
            msg = (f"{pair}: The latest total volume on asks ({ask_volume}) is greater than the {KOEF} * average volume"
                   f" for the last {PERIOD_SEC} seconds ({avg_ask_volume})")
            await self.send_telegram_message(msg)

        if bid_volume > (avg_bid_volume * KOEF) and len(self.bid_volumes_history) == PERIOD_SEC:
            msg = (f"{pair}: The latest total volume by bids ({bid_volume}) is greater than the {KOEF} * average volume"
                   f" for the last {PERIOD_SEC} seconds ({avg_bid_volume})")
            await self.send_telegram_message(msg)

    @measure_time
    async def send_telegram_message(self, message):
        """
        Asynchronous function to send a message to a Telegram group.

        Args:
            message (str): The message to be sent.

        Returns:
            None

        """

        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

    async def update_ask_volumes_history(self, new_data):
        self.ask_volumes_history.append(new_data)

    async def update_bid_volumes_history(self, new_data):
        self.bid_volumes_history.append(new_data)
