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
        range_key_condition = None

        if "opponent_id" in parameters:
            range_key_condition = GameModel.opponent_id == parameters["opponent_id"]
        elif "winner_id" in parameters:
            range_key_condition = GameModel.winner_id == parameters["winner_id"]

        return 200, ApiHandler.jsonstr([game.attribute_values for game in list(
            GameModel.query(pathParameters["player"], range_key_condition=range_key_condition))])

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
