from flask import Flask, request, make_response, jsonify
from multiprocessing import Queue, Process
import json
import jwt
import datetime
from functools import wraps
import string
import random


class ApiServer(Process):

    def __init__(self, post_queue, link_task_queue):
        """init

        Args:
            post_queue (Queue): queue of posts, resoure shared with the main bot
            link_pipe(Connection): 
        """
        super(ApiServer, self).__init__()
        self.post_queue = post_queue
        self.link_task_queue = link_task_queue
        self.config = {}
        with open('src/bot_conf.json', 'r') as conf_file:
            self.config['USERS'] = (json.load(conf_file))["api_users"]
        self.api = Flask(__name__)
        self.config['SECRET_KEY'] = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))

        @self.api.route('/login', methods=['GET'])
        def login():
            """login users and return token via http get

            Returns:
                [Response]: http content
            """
            auth = request.authorization
            if auth and self.verify_user({'username': auth.username, 'password': auth.password}):
                exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                token = jwt.encode(
                    {'user': auth.username, 'exp': exp}, self.config['SECRET_KEY'])
                return jsonify({'token': token.decode('UTF-8'), 'exp': exp.timestamp()})

            return make_response('Could not verify', 401, {'WWW-Aurthenticate': 'Basic realm="Login Required"'})

        @self.api.route('/server/channel/text/send_notice', methods=['POST'])
        @self.token_required
        def send_channel_post():
            """put the post (json format) in the post_queue
            """
            post = request.json
            self.post_queue.put(post)
            return 'OK'

        @self.api.route('/server/link_invitation', methods=['GET'])
        @self.token_required
        def get_link_invitation():
            self.link_task_queue[0].put("get_link")
            link = self.link_task_queue[1].get()
            return jsonify({'link': link})

    def verify_user(self, user):
        """check if username and password is correct

        Args:
            user (dict): dict which has username and password

        Returns:
            Bool: True if correct and vice versa
        """
        return user in self.config['USERS']

    def token_required(self, f):
        """decorator to check if the token is correct

        Args:
            f (function): a function to decorate
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.args.get('token')
            if not token:
                return jsonify({'message': 'Token is missing'}), 403

            try:
                date = jwt.decode(token, self.config['SECRET_KEY'])
            except:
                return jsonify({'message': 'Token is invalid'}), 403

            return f(*args, **kwargs)
        return decorated

    def run(self):
        """API server process started by discord bot in the main file
        """
        self.api.run(
            debug=False, host='0.0.0.0')  # host means which hosts can be access this API, 0.0.0.0 means all
