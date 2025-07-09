import time
import random
from sklearn.tree import DecisionTreeClassifier
import numpy as np

class EcoPulse:
    def __init__(self):
        X = np.array([[70, 20], [30, 35], [80, 18], [20, 40]])
        y = np.array([1, 0, 1, 0])  # 1: healthy, 0: unhealthy
        self.model = DecisionTreeClassifier()
        self.model.fit(X, y)

    def get_advice(self, moisture=None, temp=None):
        if moisture is None or temp is None:
            moisture, temp = random.randint(20, 90), random.randint(15, 40)
        prediction = self.model.predict([[moisture, temp]])
        return "Irrigate now!" if prediction[0] == 0 else "Conditions are good."

    def run(self):
        while True:
            print(f"Advice: {self.get_advice()}")
            time.sleep(3600)  # Update hourly

if __name__ == "__main__":
    ecopulse = EcoPulse()
    ecopulse.run()
