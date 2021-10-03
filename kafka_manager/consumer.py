from .config import Config
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

class Consumer():
    host = None
    username = None
    password = None
    auto_commit = True
    group_id = None
    topic = None
    is_stopped = False

    def __init__(self):
        if not Config._instance:
            raise Exception("Config is not found")

        if self.__class__ == Consumer:
            raise Exception("Base class can't start")

        if self.topic == None:
            raise Exception("Can't start without topic")
        
        if self.group_id == None:
            raise Exception("Can't start without group_id")

        self.consumer = KafkaConsumer(
            bootstrap_servers=Config._instance.host,
            sasl_plain_username=Config._instance.username,
            sasl_plain_password=Config._instance.password,
            sasl_mechanism='PLAIN',
            security_protocol='SASL_PLAINTEXT',
            consumer_timeout_ms=1000,
            enable_auto_commit=self.auto_commit,
            group_id=self.group_id
        )
        self.consumer.subscribe(self.topic)

        if not self.is_stopped:
            self.run()

    def process_message(self, message : ConsumerRecord):
        pass

    def start(self):
        self.is_stopped = False
        self.run()
    
    def stop(self):
        self.is_stopped = True

    def run(self):
        print(f"Consuming {self.topic}")
        while not self.is_stopped:
            msg_pack = self.consumer.poll(0.1)
            if not msg_pack:
                continue
            for tp, messages in msg_pack.items():
                for message in messages:
                    self.process_message(message)
        self.consumer.close()