import json
import os
import random
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
from faker import Faker
from azure.eventhub import EventHubProducerClient, EventData

# Load environment variables
load_dotenv()
CONNECTION_STR = os.getenv("AZURE_EVENT_HUB_CONNECTION_STRING")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")

fake = Faker()

# Simulation settingsC
OS_LIST = ["Windows", "MacOS", "Linux", "Android"]
BROWSERS = ["Chrome", "Safari", "Firefox", "Edge", "Opera"]
PAGES = [f"/page{i}.html" for i in range(1, 26)]
DEVICE_TYPES = ["phone", "desktop", "tablet"]

# Number of events per batch (helps Capture trigger)
EVENTS_PER_BATCH = 20
SLEEP_BETWEEN_BATCHES = 0.1  # seconds

def generate_event():
    event_id = fake.uuid4()
    return {
        "eventId": event_id,
        "timeStamp": datetime.now(timezone.utc).isoformat(),
        "userId": fake.uuid4(),
        "sessionId": fake.uuid4(),
        "ipAddress": fake.ipv4(),
        "path": random.choice(PAGES),
        "os": random.choice(OS_LIST),
        "browser": random.choice(BROWSERS),
        "deviceType": random.choice(DEVICE_TYPES),
        "isLead": random.choice([True, False]),  # 10% chance
        "diagnostics": ""
    }

def main():
    producer = EventHubProducerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        eventhub_name=EVENT_HUB_NAME
    )

    print("Simulator started. Sending events... Press Ctrl+C to stop.")

    try:
        while True:
            # Generate first event to decide partition key
            first_event = generate_event()
            partition_key = first_event["userId"]
            batch = producer.create_batch(partition_key=partition_key)
            
            # Add multiple events to batch
            batch.add(EventData(json.dumps(first_event)))
            for _ in range(EVENTS_PER_BATCH - 1):
                event = generate_event()
                if event["userId"] != partition_key:
                    # Different partition → stop adding
                    break
                batch.add(EventData(json.dumps(event)))
            
            # Send the batch
            producer.send_batch(batch)
            print(f"Sent batch with partition_key={partition_key}, {len(batch)} events at {datetime.now().strftime('%H:%M:%S')}")

            time.sleep(SLEEP_BETWEEN_BATCHES)

    except KeyboardInterrupt:
        print("Simulator stopped by user.")

if __name__ == "__main__":
    main()