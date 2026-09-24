import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

ARTIFACTS_DIR = r"C:\Users\apsar\.gemini\antigravity-ide\brain\c0616a3b-ff03-41ec-b8af-cd564e9cf092"
MODELS_DIR = "ml_models"
os.makedirs(MODELS_DIR, exist_ok=True)

# --- 1. Dataset Generation ---
class SequenceDataset(Dataset):
    def __init__(self, num_samples=2000, seq_length=10, num_modules=20):
        super().__init__()
        self.num_samples = num_samples
        self.seq_length = seq_length
        self.num_modules = num_modules
        
        # X: sequences of module IDs (0 to num_modules-1)
        self.X = np.random.randint(0, num_modules, (num_samples, seq_length))
        
        # y: mastery prediction (binary). E.g., if sum of unique modules > 5 and last module > 10, then success.
        self.y = np.zeros(num_samples)
        for i in range(num_samples):
            if len(set(self.X[i])) > 5 and self.X[i, -1] > 10:
                self.y[i] = 1
            else:
                self.y[i] = 0
                
        # To make it slightly more complex, add some noise
        noise_idx = np.random.choice(num_samples, int(0.1*num_samples), replace=False)
        self.y[noise_idx] = 1 - self.y[noise_idx]
        
    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, idx):
        return torch.tensor(self.X[idx], dtype=torch.long), torch.tensor(self.y[idx], dtype=torch.float32)

# --- 2. Model Architectures ---
class LearnerLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, output_dim, dropout=0.2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, num_layers=2, dropout=dropout)
        self.batch_norm = nn.BatchNorm1d(hidden_dim)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(dropout)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        embedded = self.embedding(x)
        output, (hidden, cell) = self.lstm(embedded)
        
        # Take the output of the last time step
        last_hidden = output[:, -1, :]
        last_hidden = self.batch_norm(last_hidden)
        last_hidden = self.dropout(last_hidden)
        
        out = self.fc(last_hidden)
        return self.sigmoid(out).squeeze(1)

class MasteryTransformer(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_heads, hidden_dim, output_dim, dropout=0.2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        
        # Using a simpler TransformerEncoder block
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, dim_feedforward=hidden_dim, dropout=dropout, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=2)
        
        self.batch_norm = nn.BatchNorm1d(embed_dim)
        self.fc = nn.Linear(embed_dim, output_dim)
        self.dropout = nn.Dropout(dropout)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        embedded = self.embedding(x)
        
        # In a real scenario, add Positional Encoding here
        
        transformer_out = self.transformer_encoder(embedded)
        
        # Global average pooling across the sequence dimension
        pooled_out = transformer_out.mean(dim=1)
        pooled_out = self.batch_norm(pooled_out)
        pooled_out = self.dropout(pooled_out)
        
        out = self.fc(pooled_out)
        return self.sigmoid(out).squeeze(1)

# --- 3. Training Loop ---
def train_model(model, train_loader, val_loader, epochs=50, lr=0.001, patience=5, name="model"):
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    best_val_loss = float('inf')
    patience_counter = 0
    
    history = {'train_loss': [], 'val_loss': [], 'val_acc': []}
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            y_pred = model(X_batch)
            loss = criterion(y_pred, y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            
        train_loss /= len(train_loader)
        
        model.eval()
        val_loss = 0
        all_preds, all_labels = [], []
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                y_pred = model(X_batch)
                loss = criterion(y_pred, y_batch)
                val_loss += loss.item()
                
                preds = (y_pred >= 0.5).float()
                all_preds.extend(preds.numpy())
                all_labels.extend(y_batch.numpy())
                
        val_loss /= len(val_loader)
        val_acc = accuracy_score(all_labels, all_preds)
        
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            torch.save(model.state_dict(), os.path.join(MODELS_DIR, f"best_{name}.pt"))
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"[{name}] Early stopping triggered at epoch {epoch+1}")
                break
                
    return history, all_labels, all_preds

# --- 4. Main Pipeline ---
def run_pipeline():
    dataset = SequenceDataset(num_samples=3000, seq_length=15, num_modules=30)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    
    vocab_size = 30
    
    # Init Models
    lstm_model = LearnerLSTM(vocab_size=vocab_size, embed_dim=32, hidden_dim=64, output_dim=1, dropout=0.3)
    transformer_model = MasteryTransformer(vocab_size=vocab_size, embed_dim=32, num_heads=4, hidden_dim=64, output_dim=1, dropout=0.3)
    
    # Train LSTM
    print("Training LSTM...")
    lstm_hist, lstm_labels, lstm_preds = train_model(lstm_model, train_loader, val_loader, epochs=20, name="lstm")
    
    # Train Transformer
    print("Training Transformer...")
    trans_hist, trans_labels, trans_preds = train_model(transformer_model, train_loader, val_loader, epochs=20, name="transformer")
    
    # Generate Curves
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(lstm_hist['train_loss'], label='LSTM Train Loss')
    plt.plot(lstm_hist['val_loss'], label='LSTM Val Loss')
    plt.plot(trans_hist['train_loss'], label='Transformer Train Loss')
    plt.plot(trans_hist['val_loss'], label='Transformer Val Loss')
    plt.title('Loss Curves')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(lstm_hist['val_acc'], label='LSTM Val Acc')
    plt.plot(trans_hist['val_acc'], label='Transformer Val Acc')
    plt.title('Accuracy Curves')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.savefig(os.path.join(ARTIFACTS_DIR, "dl_learning_curves.png"))
    plt.close()
    
    # Generate DL Evaluation Report
    report = ["# Deep Learning Evaluation Report\n"]
    report.append("## LSTM Sequence Predictor\n")
    report.append(f"- Accuracy: {accuracy_score(lstm_labels, lstm_preds):.4f}\n")
    report.append(f"- Precision: {precision_score(lstm_labels, lstm_preds):.4f}\n")
    report.append(f"- Recall: {recall_score(lstm_labels, lstm_preds):.4f}\n")
    report.append(f"- F1 Score: {f1_score(lstm_labels, lstm_preds):.4f}\n\n")
    
    report.append("## Transformer Encoder (Mastery Predictor)\n")
    report.append(f"- Accuracy: {accuracy_score(trans_labels, trans_preds):.4f}\n")
    report.append(f"- Precision: {precision_score(trans_labels, trans_preds):.4f}\n")
    report.append(f"- Recall: {recall_score(trans_labels, trans_preds):.4f}\n")
    report.append(f"- F1 Score: {f1_score(trans_labels, trans_preds):.4f}\n\n")
    
    report.append("## Comparison with Machine Learning\n")
    report.append("Deep Learning models (LSTM & Transformer) typically outperform traditional ML (Random Forest/SVM) when applied to purely sequential log data due to their ability to capture temporal dependencies and positional relevance of learning modules. The loss curves attached as `dl_learning_curves.png` show the training convergence.\n")
    
    with open(os.path.join(ARTIFACTS_DIR, "dl_evaluation_report.md"), "w") as f:
        f.writelines(report)

if __name__ == "__main__":
    run_pipeline()
