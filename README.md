# Sample Project for AWS Lambda with DynamoDB

## Development 

## Prerequisites

- Install [Docker](https://github.com/awslabs/aws-sam-local#prerequisites)
- Install [AWS SAM local](https://github.com/awslabs/aws-sam-local) from 
  [here](https://github.com/awslabs/aws-sam-local/releases)

### Build
For deployment we follow [the SAM documentation](https://github.com/awslabs/aws-sam-local#package-and-deploy-to-lambda)

To build the bundle.zip for lambda use the  `make bundle` target

```bash
make bundle
```

### Start an instance of DynamoDB Local
- Get it [here](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)

```bash
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
```

### Run with SAM local and environment variables
```bash
sam local start-api -n env.json
```

### Curl examples
```bash
$ curl localhost:3000/game?create=true
GameModel Created

$ curl localhost:3000/game -X POST -d '{"player_id": "mark", "opponent_id": "dave", "winner_id": "mark"}' | python -m json.tool
{
    "player_id": "mark",
    "created_time": "2018-02-21T20:04:14.309467",
    "opponent_id": "dave",
    "winner_id": "mark"
}

$ curl localhost:3000/game -X POST -d '{"player_id": "mark", "opponent_id": "dave", "winner_id": "dave"}' | python -m json.tool
{
    "player_id": "mark",
    "created_time": "2018-02-21T20:04:28.546698",
    "opponent_id": "dave",
    "winner_id": "dave"
}

$ curl localhost:3000/game -X POST -d '{"player_id": "mark", "opponent_id": "bob", "winner_id": "mark"}' | python -m json.tool
{
    "player_id": "mark",
    "created_time": "2018-02-21T20:04:48.313896",
    "opponent_id": "bob",
    "winner_id": "mark"
}

$ curl localhost:3000/game/mark?opponent_id=dave | python -m json.tool
[
    {
        "winner_id": "mark",
        "opponent_id": "dave",
        "player_id": "mark",
        "created_time": "2018-02-21T20:04:14.309467+00:00"
    },
    {
        "winner_id": "dave",
        "opponent_id": "dave",
        "player_id": "mark",
        "created_time": "2018-02-21T20:04:28.546698+00:00"
    }
]

$ curl localhost:3000/game/mark?winner_id=mark | python -m json.tool
[
    {
        "winner_id": "mark",
        "opponent_id": "dave",
        "player_id": "mark",
        "created_time": "2018-02-21T20:04:14.309467+00:00"
    },
    {
        "winner_id": "mark",
        "opponent_id": "bob",
        "player_id": "mark",
        "created_time": "2018-02-21T20:04:48.313896+00:00"
    }
]
```


### Debugging with Pycharm

- Add pycharm-debug-py3k.egg to the root directory
- Add the following lines to the lambda script
```python
import sys
sys.path.append("pycharm-debug-py3k.egg")
import pydevd
pydevd.settrace('1.2.3.4', port=5858, stdoutToServer=True, stderrToServer=True, suspend=True)
```
- Remote debug on 5858

### Debugging with Pydevd (Eclipse)

- pydevd to requirements.txt before building
- Add the following lines to the lambda script
```python
import pydevd
pydevd.settrace('1.2.3.4', port=5858, stdoutToServer=True, stderrToServer=True, suspend=True)
```
- Remote debug on 5858

