# consumer.py
from confluent_kafka import Consumer, KafkaError, KafkaException
import base64
import boto3
import json

# Kafka configuration
KAFKA_TOPIC = 'image_stream'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# S3 Configuration
s3 = boto3.client('s3')
BUCKET_NAME = "trivia-image-bucket"

# Adjusted consumer configuration
config = {
    'bootstrap.servers':  KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'trivia-image-test-group',  # Consider using a new group ID for a fresh start
    'auto.offset.reset': 'earliest'  # Ensure we start from the beginning of the topic
}

# Initialize Kafka consumer
consumer = Consumer(**config)
consumer.subscribe([KAFKA_TOPIC]) # Reference to producer


def save_image_to_s3(image_data, image_name):
    """Uploads the image to S3."""
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=image_name,
            Body=image_data,
            ContentType='image/png'
        )
        print(f"Uploaded {image_name} to S3 bucket {BUCKET_NAME}.")
    except Exception as e:
        print(f"Failed to upload {image_name} to S3: {str(e)}")

def consume_messages():
    """Consumes images from Kafka and uploads them to S3."""
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Increase poll timeout if needed

            if msg is None:
                continue  # No message, normal behavior

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event, normal behavior but can adjust if not desired
                    print(f'End of partition reached {msg.topic()}/{msg.partition()}')
                else:
                    print(f'Error: {msg.error()}')
            else:
                # Message is successfully received
                message_value = json.loads(msg.value().decode('utf-8'))
                image_data_base64, image_name = message_value['image_data'], message_value['image_id']
                print(f"Received message: {image_name}")

                # Decode base64 image data
                image_data = base64.b64decode(image_data_base64)

                # Upload to S3
                save_image_to_s3(image_data, image_name)
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()


if __name__ == "__main__":
    print("Starting image consumer service...")
    consume_messages()
