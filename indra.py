import logging

logging.basicConfig(level=logging.INFO)
logging.info("IndraAI initialized")

class IndraAI:
    def __init__(self):
        self.counter = 0

    def get_status(self):
        return "Running"

    def get_memory(self):
        self.counter += 1
        return {"visits": self.counter}

if __name__ == "__main__":
    indra = IndraAI()
