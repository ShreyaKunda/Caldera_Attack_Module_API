import pandas as pd

class AbilityLoader:

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def load(self):
        df = pd.read_csv(self.csv_path)
        return df.to_dict(orient="records")
