import time
import random
from sklearn.tree import DecisionTreeClassifier
import numpy as np

class EcoPulse:
    def __init__(self):
        # Mock training data: [moisture, temp] -> healthy/unhealthy
        X = np.array([[70, 20], [30, 35], [80, 18], [20, 40]])
        y = np.array([1, 0, 1, 0])  # 1: healthy, 0: unhealthy
        self.model = DecisionTreeClassifier()
        self.model.fit(X, y)
        self.data = [random.randint(20, 90), random.randint(15, 40)]  # [moisture, temp]

    def update_data(self):
        self.data = [random.randint(20, 90), random.randint(15, 40)]

    def get_advice(self):
        prediction = self.model.predict([self.data])
        self.update_data()
        return "Irrigate now!" if prediction[0] == 0 else "Conditions are good."

    def run(self):
        while True:
            print(f"Advice: {self.get_advice()}")
            time.sleep(3600)  # Update hourly

if __name__ == "__main__":
    ecopulse = EcoPulse()
    ecopulse.run()
