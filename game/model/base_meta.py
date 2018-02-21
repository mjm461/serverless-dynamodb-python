import os


class BaseMeta:
    read_capacity_units = 1
    write_capacity_units = 1
    host = os.environ.get('AWS_DYNAMODB_ENDPOINT', None)
    region = os.environ.get('AWS_REGION', None)
