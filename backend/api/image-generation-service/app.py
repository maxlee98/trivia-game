from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import os
import random
from PIL import Image, ImageDraw
import base64
# For Kafka
from confluent_kafka import Producer
import time
import io
import json


# Configuration for Kafka and S3
KAFKA_TOPIC = "image_stream"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"  # Update to your Kafka server
# KAFKA_BOOTSTRAP_SERVERS = "127.0.0.1:60789"  # Update to your Kafka server

# Configuration for Kafka Producer
config = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
}

def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {err}")
    else:
        # Decode the message value from bytes to a JSON object
        message_value = json.loads(msg.value().decode('utf-8'))
        print(f"Message produced: {message_value['image_id']}")


producer = Producer(**config)

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/generate_images', methods=['POST'])
def generate_and_upload_images_to_s3():
    num_images = 3
    image_folder = 'images'
    os.makedirs(image_folder, exist_ok=True)

    for i in range(num_images):
        # Create an image
        img = Image.new('RGB', (100, 100), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        draw = ImageDraw.Draw(img)
        draw.text((10, 40), f"Image-{i}", fill=(255, 255, 255))

        # Save to in-memory file
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        # Seek back to the beginning of the file.
        img_buffer.seek(0)
        # Save image in folder for backup
        img.save(os.path.join(image_folder,  f"Image-{i}.png"))
        
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        # Send image to Kafka
        metadata = {
            "image_id": f"image_{i}",
            "image_data": img_base64  # Convert image bytes to hex string for JSON compatibility
        }
        producer.produce(KAFKA_TOPIC, value=json.dumps(metadata).encode('utf-8'), callback=acked)
        producer.poll(0.1)
    producer.flush()

    return jsonify({'message': f'Streamed {num_images} images to Kafka topic - {KAFKA_TOPIC}'}), 201




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

    # Test Upload file to S3
    # print(os.getcwd())
    # generate_and_upload_images_to_s3(3)

