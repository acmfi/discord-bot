from flask import Flask, request
from multiprocessing import Queue
import json


def run(post_queue: Queue):
    """API server process started by discord bot on the main file

    Args:
        post_queue (Queue): queue of the posts, resoure used for the model consumer/producer

    """
    USERS = (json.load(open('src/bot_conf.json', 'r')))["api_users"]

    api = Flask(__name__)

    def verify_user(user):
        """check if username and password is correct

        Args:
            user (dict): dict wich has username and password

        Returns:
            Bool: true if correct and vice versa
        """
        return user in USERS

    @api.route('/sendChannelPost', methods=['POST'])
    def send_channel_post():
        """put the post (json format) on the post_queue

        """
        post = request.json
        if not verify_user(post["user"]):
            print("EL equipo", request.remote_addr,
                  "intento acceder con con algún dato erróneo")
            return "El usario o la contraseña no es correcto"
        post_queue.put(post)
        return 'OK'

    api.run(debug=False, host='0.0.0.0')
