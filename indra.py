import logging

logging.basicConfig(level=logging.INFO)
logging.info("IndraAI initialized")

class IndraAI:
    def get_status(self):
        return "Running"
    def get_memory(self):
        return {}

if __name__ == "__main__":
    indra = IndraAI()
