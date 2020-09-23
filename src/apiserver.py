from flask import Flask, request
from multiprocessing import Queue, Process
import json


class ApiServer(Process):

    def __init__(self, post_queue, link_connection):
        """init

        Args:
            post_queue (Queue): queue of posts, resoure shared with the main bot
            link_pipe(Connection): 
        """
        super(ApiServer, self).__init__()
        self.post_queue = post_queue
        self.link_connection = link_connection
        with open('src/bot_conf.json', 'r') as conf_file:
            self.USERS = (json.load(conf_file))["api_users"]
        self.api = Flask(__name__)

        @self.api.route('/server/channel/text/send_notice', methods=['POST'])
        def send_channel_post():
            """put the post (json format) on the post_queue
            """
            post = request.json
            if not self.verify_user(post["user"]):
                print("EL equipo", request.remote_addr,
                      "intento acceder con con algún dato erróneo")
                return "El usario o la contraseña no es correcto"
            self.post_queue.put(post)
            return 'OK'

        @self.api.route('/server/link_invitation', methods=['POST'])
        def get_link_invitation():
            post = request.json
            if not self.verify_user(post["user"]):
                print("EL equipo", request.remote_addr,
                      "intento acceder con con algún dato erróneo")
                return "El usario o la contraseña no es correcto"
            self.link_connection.send("get")
            return self.link_connection.recv()

    def verify_user(self, user):
        """check if username and password is correct

        Args:
            user (dict): dict wich has username and password

        Returns:
            Bool: true if correct and vice versa
        """
        return user in self.USERS

    def run(self):
        """API server process started by discord bot on the main file
        """
        self.api.run(
            debug=False, host='0.0.0.0')  # host mean the wich hosts can access this api
