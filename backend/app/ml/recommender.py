import numpy as np
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

class LearningRecommender:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        self.le = LabelEncoder()
        
        # Load the cleaned dataset
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        data_path = os.path.join(base_dir, 'xAPI_cleaned.csv')
        
        try:
            df = pd.read_csv(data_path)
            
            # Features: gender_num and raisedhands
            # (Assuming mapping: M=0, F=1 done by clean script)
            # Default to 0 for missing
            if 'gender_num' not in df.columns:
                 df['gender_num'] = df['gender'].map({'M': 0, 'F': 1}).fillna(0)
                 
            X = df[['gender_num', 'raisedhands']].fillna(0).values
            y = self.le.fit_transform(df['Topic'].astype(str))
            
            self.model.fit(X, y)
            self.is_trained = True
        except Exception as e:
            print(f"Failed to train model on dataset: {e}")
            self.is_trained = False

    def predict_next_topic(self, gender_num: int, raisedhands: int):
        if not self.is_trained:
            return {"topic": "Model untrained", "confidence_score": 0.0}
            
        prediction = self.model.predict([[gender_num, raisedhands]])[0]
        probs = self.model.predict_proba([[gender_num, raisedhands]])[0]
        confidence = float(max(probs))
        
        topic_name = self.le.inverse_transform([prediction])[0]
        
        return {
            "topic": topic_name,
            "confidence_score": confidence,
            "gender_num": gender_num,
            "raisedhands": raisedhands
        }

def generate_recommendations(user_id: int):
    import random
    
    # Since user features like 'gender_num' and 'raisedhands' are not yet stored in 
    # the database schema, we simulate fetching them by seeding with the user_id 
    # to provide consistent recommendations for a specific user.
    random.seed(user_id)
    mock_gender_num = random.choice([0, 1])
    mock_raisedhands = random.randint(0, 100)
    
    prediction = recommender_engine.predict_next_topic(mock_gender_num, mock_raisedhands)
    return [prediction]

recommender_engine = LearningRecommender()

if __name__ == "__main__":
    print("Testing ML Recommender...")
    # Test with a mock user ID
    output = generate_recommendations(user_id=1)
    print("Output:")
    print(output)
