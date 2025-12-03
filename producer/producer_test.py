from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')

for i in range(10):
    message = f"Message {i}"
    producer.send('test-topic', value=message.encode('utf-8'))
    print(f"Envoyé: {message}")
    time.sleep(0.5)

producer.flush()
producer.close()
print("Tous les messages ont été envoyés !")

