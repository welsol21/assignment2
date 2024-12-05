import pika
import os
import time
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Лог в консоль (stdout)
)


def callback(ch, method, properties, body):
    # Логирование сообщения с метаданными
    logging.info(f"""
    Received Message:
    -----------------
    Exchange: {method.exchange or "(AMQP default)"}
    Routing Key: {method.routing_key}
    Redelivered: {method.redelivered}
    Properties: {properties.headers if properties.headers else "(No properties)"}
    Payload: {body.decode()}
    """)


def connect_to_rabbitmq():
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    rabbitmq_port = int(os.getenv("RABBITMQ_PORT", 5672))

    for attempt in range(10):  # Try to connect 10 times
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port)
            )
            return connection
        except pika.exceptions.AMQPConnectionError:
            logging.warning(f"Connection attempt {attempt + 1} failed. Retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("Failed to connect to RabbitMQ after 10 attempts.")


def main():
    connection = connect_to_rabbitmq()
    channel = connection.channel()

    # Убедитесь, что очередь `logs` существует
    channel.queue_declare(queue='logs')  # Работает с прямой очередью

    logging.info('Waiting for messages in queue "logs". To exit press CTRL+C')
    try:
        channel.basic_consume(queue='logs', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except KeyboardInterrupt:
        logging.info("Consumer stopped by user.")
        channel.stop_consuming()
        connection.close()


if __name__ == '__main__':
    main()
