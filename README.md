# Sample Project for AWS Lambda with DynamoDB

## Development 

## Prerequisites

- Install [Docker](https://github.com/awslabs/aws-sam-local#prerequisites)
- Install [AWS SAM local](https://github.com/awslabs/aws-sam-local) from 
  [here](https://github.com/awslabs/aws-sam-local/releases)

## To test:
```bash
echo '{ "resources": ["arn:aws:events:eu-west-1:482174156240:rule/10MinuteTickRule"] }' | sam local invoke SampleHandlerApi
```

### Build
For deployment we follow [the SAM documentation](https://github.com/awslabs/aws-sam-local#package-and-deploy-to-lambda)

To build the bundle.zip for lambda use the  `make bundle` target

```bash
make bundle
```

### Run with SAM local and environment variables
```bash
sam local start-api -n env.json
```

### Curl commaands
```bash
# Create a new game
curl localhost:3000/game -X POST -d '{"player_id": "mark", "winner_id": "mark", "loser_id": "bob"}'

# List game for a player
curl localhost:3000/game/mark

# List all games
curl localhost:3000/game
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

