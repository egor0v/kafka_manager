from .config import Config
from kafka import KafkaProducer
import json

class Producer():
    _instance = None
    
    host = None
    username = None
    password = None
    topic = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Producer, cls).__new__(
                cls, *args, **kwargs
            )
        return cls._instance

    def __init__(self):
        if not Config._instance:
            raise Exception("Config is not found")

        if self.__class__ == Producer:
            raise Exception("Base class can't produce")

        if self.topic == None:
            raise Exception("Can't produce without topic")
        
        self.producer = KafkaProducer(
            bootstrap_servers=Config._instance.host,
            sasl_plain_username=Config._instance.username,
            sasl_plain_password=Config._instance.password,
            sasl_mechanism="PLAIN",
            security_protocol="SASL_PLAINTEXT",
        )

    def send_message(self, data):
        self.producer.send(topic=self.topic, value=json.dumps(data).encode("utf-8"))
        self.producer.flush()
