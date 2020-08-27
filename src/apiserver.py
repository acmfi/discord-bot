from flask import Flask, request
from multiprocessing import Queue
import signal


def run(post_queue: Queue):

    api = Flask(__name__)

    @api.route('/sendChannelPost', methods=['POST'])
    def send_channel_post():
        post = request.json
        post_queue.put(post)
        return 'ok'

    api.run(debug=False, host='0.0.0.0')
