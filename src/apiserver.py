from flask import Flask, request
from multiprocessing import Queue

def run(post_queue: Queue):
    api = Flask(__name__)

    @api.route('/sendChannelPost', methods=['POST'])
    def send_channel_post():
        post = request.json
        post_queue.put(post)
        print(post['text'])
        return 'ok'
        
    api.run(debug=False)



    



