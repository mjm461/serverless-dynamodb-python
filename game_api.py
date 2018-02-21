from game import LambdaBase
from game import singleton
from game.model import GameModel
import json
import datetime

#import sys
#sys.path.append("pycharm-debug-py3k.egg")
#import pydevd
#pydevd.settrace('1.2.3.4', port=5858, stdoutToServer=True, stderrToServer=True, suspend=True)


@singleton
class ApiHandler(LambdaBase):

    def __init__(self):
        super().__init__()
        self.endpoints = {
            "GET": {
                None: self.list,
                "player": self.find
            },
            "POST": {
                None: self.create,

            }
        }

    def list(self, headers, parameters, pathParameters, body):
        return 200, ApiHandler.jsonstr([game.attribute_values for game in list(GameModel.scan())])

    def find(self, headers, parameters, pathParameters, body):
        return 200, ApiHandler.jsonstr([game.attribute_values for game in list(GameModel.query(pathParameters["player"]))])

    def create(self, headers, parameters, pathParameters, body):
        payload = json.loads(body)

        item = GameModel(payload["player_id"], datetime.datetime.utcnow())
        item.winner_id = payload["winner_id"]
        item.loser_id = payload["loser_id"]
        item.save()

        return 200, ApiHandler.jsonstr(item.attribute_values)

    @staticmethod
    def jsonstr(d):
        def converter(o):
            if isinstance(o, datetime.datetime):
                return o.isoformat()

        return json.dumps(d, default=converter)

    def handle(self, event, context):

        path = None if not event['pathParameters'] else next(iter(event['pathParameters']))

        status, body = self.endpoints[event["httpMethod"]][path](
            event["headers"],
            event["queryStringParameters"],
            event['pathParameters'],
            event["body"])

        return {
            "statusCode": status,
            "headers": {
                "x-custom-header": "my custom header value"
            },
            "body": body
        }


handler = ApiHandler.get_handler()
