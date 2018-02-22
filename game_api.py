from game import LambdaBase
from game import singleton
from game.model import GameModel
import json
import datetime
import os

if 'DEBUG' in os.environ:
    import sys
    sys.path.append("pycharm-debug-py3k.egg")
    import pydevd
    pydevd.settrace(os.environ['DEBUG'], port=5858, stdoutToServer=True, stderrToServer=True, suspend=True)


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
        if "create" in parameters:
            ## Quick and dirty way to create the table
            if not GameModel.exists():
                GameModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
            if not GameModel.exists():
                GameModel.create_table(wait=True)
            return 200, "GameModel Created"
        else:
            ## This is just an example - don't scan the whole table
            return 200, ApiHandler.jsonstr([game.attribute_values for game in list(GameModel.scan())])

    def find(self, headers, parameters, pathParameters, body):

        opponent_id = parameters.get("opponent_id", None)
        winner = parameters.get("winner", None)

        if opponent_id:
            ## Use LSI to find the times you played an opponent
            results = GameModel.player_opponent_index.query(pathParameters["player"], GameModel.opponent_id == opponent_id)
        elif winner:
            ## Use GSI to order your wins by time
            results = GameModel.winner_time_index.query(pathParameters["player"])
        else:
            ## Get your wins/losses
            results = GameModel.query(pathParameters["player"])

        return 200, ApiHandler.jsonstr([game.attribute_values for game in list(results)])

    def create(self, headers, parameters, pathParameters, body):
        payload = json.loads(body)

        item = GameModel(payload["player_id"], datetime.datetime.utcnow())
        item.opponent_id = payload["opponent_id"]
        item.winner_id = payload["winner_id"]
        if "notes" in payload:
            item.notes = payload["notes"]
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
