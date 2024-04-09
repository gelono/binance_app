This application receives price and order volume data from the Binance exchange. Volume data is written to the posrgresql database, processed, and if a surge in order volume is detected, users are notified about this event in Telegram.

The main application parameters are placed in environment variables (.env):
```shell
USERNAME: database user;
PASSWORD: database password;
HOST: database host;
DATABASE: database name;
PORT: database port;
```
```shell
PERCENT: percentage of price depth in the order book (best ask+percent, best bid - percent). The parameter is specified as an integer, for example 2;
PAIRS: list of currency pairs, for example - "BTCUSDT,ETHUSDT,SOLUSDT";
PERIOD_SEC: the period of time in seconds for which the average total volume in the order book is calculated in the specified price range;
KOEF: coefficient by which the average total volume is multiplied. This setting controls the amount of volume burst that is tracked by this application;
```
```shell
TELEGRAM_TOKEN: Telegram bot token
TELEGRAM_CHAT_ID: Telegram chat id
```
This application runs in asynchronous mode, since it involves many IO operations:
- contacting the stock exchange;
- entry into the database;
- sending messages to Telegram.

All main methods work with a decorator, which measures the running time of the method on every tenth call of this method.

```shell
When you start it for the first time, you need to run the script:
create_tables.py - it will create tables in the database;
then run the script:
fill_assets.py - it will fill the table with the installed currency pairs.
```