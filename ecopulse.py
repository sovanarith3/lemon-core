import time
import random
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EcoPulse:
    def __init__(self):
        X = np.array([[70, 20], [30, 35], [80, 18], [20, 40]])
        y = np.array([1, 0, 1, 0])
        self.model = DecisionTreeClassifier()
        self.model.fit(X, y)
        self.data = [random.randint(20, 90), random.randint(15, 40)]

    def get_advice(self):
        prediction = self.model.predict([self.data])
        self.data = [random.randint(20, 90), random.randint(15, 40)]
        return "Irrigate now!" if prediction[0] == 0 else "Conditions are good."

    def run(self):
        while True:
            try:
                advice = self.get_advice()
                logger.info(f"Advice: {advice}")
            except Exception as e:
                logger.error(f"Error: {e}")
            time.sleep(21600)  # Reduce to every 6 hours

if __name__ == "__main__":
    ecopulse = EcoPulse()
    ecopulse.run()
