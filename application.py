from collections import OrderedDict

from flask import Flask, request

application = Flask(__name__)

next_id = 1
messages = OrderedDict()
class_list = OrderedDict()


@application.route("/messages", methods=["GET", "POST", "DELETE"])
def messages():
    global next_id

    match request.method:
        case "GET":
            return messages, 200
        case "POST" if len(request.data) > 50:
            # 413 Request Entity Too Large
            return "Message can only be up to 50 characters", 413
        case "POST":
            messages[next_id] = request.data.decode("utf-8")
            if len(messages) > 50:
                messages.popitem(last=False)
            next_id += 1
            return str(next_id - 1), 201
        case "DELETE" if request.data in messages.keys():
            messages.pop(request.data), 204
        case "DELETE":
            return "Message ID not found", 404


# noinspection SpellCheckingInspection
tickers = {
    "AMZN": 175.00,
    "AAPL": 170.33,
    "NVDA": 864.02,
    "WMT": 59.35,
}


@application.route("/stocks", methods=["GET"])
def stocks_no_ticker():
    return list(tickers.keys()), 200


@application.route("/stocks/<ticker>", methods=["GET"])
def stocks(ticker):
    if ticker.upper() in tickers.keys():
        return str(tickers[ticker.upper()]), 200
    else:
        return 404


@application.route("/")
def index():
    return "Welcome to my API!", 200


if __name__ == "__main__":
    application.run(port=80)
