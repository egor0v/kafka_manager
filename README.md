

# Либа для удобного использования кафки в питоне

Наброски библиотеки для удобной работы с кафкой
Используется либа kafka-python

### Класс Config
Класс Config - синглтон, то есть экземпляр продюсера будет создан один раз.
Должен быть создан до начала использования
Пока не поддерживает ничего, кроме того что нужно нам, в будущем может быть допилен :)

    from kafka_manager.config import Config

    Config(host="127.0.0.1:8090", username="login", password="pass")


### Класс Consumer
    
    from kafka_manager.consumer import Consumer

    class TestConsumer(Consumer):
        topic = "TestTopic" # Топик который слушаем
        group_id = "KafkaDebugGroup" # Идентификатор приложения

        def process_message(self, message): # Обработчик в которое поступают сообщения
            ...
    
    TestConsumer() # Запуск консьюмера

### Класс Producer
Класс Producer - синглтон, то есть экземпляр продюсера будет создан один раз.

    from kafka_manager.producer import Producer

    class TestProducer(Producer):
        topic = "TestTopic" # Топик в который отправляем сообщения
    
    TestProducer().send_message({"hello": "World"}) # Отправка сообщения

### Установка
 
    pip install -e git+https://github.com/egor0v/kafka_manager.git#egg=kafka_manager

### Пример
Примитивный пример использования

    from kafka_manager.consumer import Consumer
    from kafka_manager.producer import Producer
    from kafka_manager.config import Config
    import time
    import threading

    # Описываем конфигурацию консьюмера
    class TestConsumer(Consumer):
        topic = "TestTopic"
        group_id = "KafkaDebugGroup"

        def process_message(self, message):
            print(message)

    # Описываем конфигурацию продюсера
    class TestProducer(Producer):
        topic = "TestTopic"

    # Создаем конфиг
    Config(host="127.0.0.1:8090", username="user", password="password")


    def consume():
        TestConsumer()

    def producer_example():
        i = 0
        while 1:
            TestProducer().send_message({"index": i})
            i += 1
            time.sleep(1)

    # Запускаем два треда, один слушает, второй постоянно пишет
    t1 = threading.Thread(target=consume)
    t2 = threading.Thread(target=producer_example)
    t1.start()
    t2.start()