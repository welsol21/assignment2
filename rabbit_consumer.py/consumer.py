import pika


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")


def main():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Declare the queue (should match the producer)
    channel.queue_declare(queue='logs')

    # Subscribe to the queue
    channel.basic_consume(queue='logs', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Exiting...")
        channel.stop_consuming()


if __name__ == '__main__':
    main()
