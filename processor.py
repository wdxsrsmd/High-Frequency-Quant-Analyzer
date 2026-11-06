import time
import random
import threading
import queue
from collections import deque

class RealTimeStreamProcessor:
    """
    A highly scalable, multithreaded data streaming engine.
    Simulates processing high-velocity real-time events and 
    aggregating statistics using a sliding window approach.
    """
    def __init__(self, window_size=100):
        self.event_queue = queue.Queue()
        self.window_size = window_size
        self.processed_count = 0
        self.is_running = False
        # Memory-efficient sliding window using deque
        self.sliding_window = deque(maxlen=window_size)

    def ingest_data(self):
        """Simulates an external data source (e.g., Kafka/WebSocket)."""
        while self.is_running:
            # Simulate high-frequency tick data (e.g., financial or IoT data)
            event = {"timestamp": time.time(), "value": random.uniform(100, 200)}
            self.event_queue.put(event)
            time.sleep(0.01) # 100 events per second

    def process_stream(self):
        """Worker thread to process and aggregate data."""
        while self.is_running or not self.event_queue.empty():
            try:
                event = self.event_queue.get(timeout=1)
                self.sliding_window.append(event["value"])
                self.processed_count += 1
                
                # Perform real-time analytics every 50 events
                if self.processed_count % 50 == 0:
                    self.calculate_analytics()
                    
                self.event_queue.task_done()
            except queue.Empty:
                continue

    def calculate_analytics(self):
        """Calculates real-time moving averages and anomalies."""
        if not self.sliding_window:
            return
        current_avg = sum(self.sliding_window) / len(self.sliding_window)
        max_val = max(self.sliding_window)
        
        print(f"[Stream Analytics] Processed: {self.processed_count} | "
              f"Moving Avg: {current_avg:.2f} | Peak: {max_val:.2f}")

    def start(self):
        self.is_running = True
        print("[*] Booting Real-Time Stream Processor...")
        
        # Start background threads
        producer = threading.Thread(target=self.ingest_data)
        consumer = threading.Thread(target=self.process_stream)
        
        producer.start()
        consumer.start()
        
        try:
            time.sleep(3) # Run demo for 3 seconds
            print("\n[*] Initiating graceful shutdown...")
        finally:
            self.is_running = False
            producer.join()
            consumer.join()
            print(f"[*] Shutdown complete. Total events processed: {self.processed_count}")

if __name__ == "__main__":
    engine = RealTimeStreamProcessor()
    engine.start()
