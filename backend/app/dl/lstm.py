import torch
import torch.nn as nn
import os

class StudentScoreLSTM(nn.Module):
    def __init__(self, input_size=4, hidden_size=16, num_layers=1, output_size=1):
        super(StudentScoreLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # LSTM layer
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        # Fully connected layer to predict the score (0-100)
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        # Initialize hidden state and cell state with zeros
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        # Forward propagate LSTM
        out, _ = self.lstm(x, (h0, c0))
        
        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        
        # Ensure output is a bounded score using Sigmoid and scaling (0 to 100)
        return torch.sigmoid(out) * 100.0


# Instantiate a singleton model (with random weights for now)
model = StudentScoreLSTM(input_size=4, hidden_size=16)
model.eval()

def predict_score(features: list) -> float:
    """
    Predicts a student's score given a list of features.
    Args:
        features: A list of 4 numerical features, e.g.,
                  [raisedhands, VisITedResources, AnnouncementsView, Discussion]
    Returns:
        float: Predicted score from 0 to 100
    """
    try:
        # Features should be shaped (batch_size, sequence_length, input_size)
        # We treat the single feature set as a sequence of length 1
        tensor_features = torch.tensor([[features]], dtype=torch.float32)
        
        with torch.no_grad():
            prediction = model(tensor_features)
            
        return round(float(prediction.item()), 2)
    except Exception as e:
        print(f"LSTM Prediction Error: {e}")
        # Fallback in case of error
        return 50.0
