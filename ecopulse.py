def run(self):
    while True:
        try:
            print(f"Advice: {self.get_advice()}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(10800)  # Reduce to every 3 hours to save CPU
