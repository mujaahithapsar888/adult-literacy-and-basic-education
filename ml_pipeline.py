import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve

ARTIFACTS_DIR = r"C:\Users\apsar\.gemini\antigravity-ide\brain\c0616a3b-ff03-41ec-b8af-cd564e9cf092"
MODELS_DIR = "ml_models"
os.makedirs(MODELS_DIR, exist_ok=True)

# 1. Generate Synthetic Dataset
def generate_data(n=2000):
    np.random.seed(42)
    age = np.random.randint(18, 65, n)
    hours_studied = np.random.uniform(5, 100, n)
    previous_education = np.random.choice(['None', 'Primary', 'Secondary'], n, p=[0.4, 0.4, 0.2])
    engagement_score = np.random.uniform(0, 1, n)
    
    # Introduce some noise/outliers and missing values for realism
    hours_studied[np.random.choice(n, 50, replace=False)] = np.random.uniform(200, 300, 50) # Outliers
    engagement_score[np.random.choice(n, 100, replace=False)] = np.nan # Missing values

    # Target calculation
    # Let's say older students need more hours, engagement boosts success
    success_prob = (hours_studied / 100) * 0.4 + engagement_score * 0.5 + (age < 30) * 0.1
    success = (success_prob > np.nanmedian(success_prob)).astype(int)
    
    df = pd.DataFrame({
        'age': age,
        'hours_studied': hours_studied,
        'previous_education': previous_education,
        'engagement_score': engagement_score,
        'success': success
    })
    
    # Add duplicates
    df = pd.concat([df, df.sample(50)])
    
    return df

# 2. Preprocessing & EDA
def process_and_eda(df):
    report = ["# EDA & Preprocessing Report\n"]
    report.append(f"Original shape: {df.shape}\n")
    
    # Missing values
    missing = df.isnull().sum()
    report.append(f"## Missing Values\n{missing}\n")
    df['engagement_score'].fillna(df['engagement_score'].median(), inplace=True)
    
    # Duplicates
    dups = df.duplicated().sum()
    report.append(f"## Duplicates Found: {dups}\n")
    df.drop_duplicates(inplace=True)
    
    # Outliers
    q1 = df['hours_studied'].quantile(0.25)
    q3 = df['hours_studied'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = df[(df['hours_studied'] < lower_bound) | (df['hours_studied'] > upper_bound)].shape[0]
    report.append(f"## Outliers in hours_studied: {outliers}\n")
    # Cap outliers
    df.loc[df['hours_studied'] > upper_bound, 'hours_studied'] = upper_bound
    
    report.append(f"Final shape: {df.shape}\n")
    
    with open(os.path.join(ARTIFACTS_DIR, "eda_report.md"), "w") as f:
        f.writelines(report)
        
    return df

# 3. Feature Engineering & Split
def fe_and_split(df):
    report = ["# Feature Engineering Report\n"]
    
    # Feature 1: engagement_per_hour
    df['engagement_per_hour'] = df['engagement_score'] / (df['hours_studied'] + 1)
    report.append("Added feature `engagement_per_hour`.\n")
    
    X = df.drop('success', axis=1)
    y = df['success']
    
    num_cols = ['age', 'hours_studied', 'engagement_score', 'engagement_per_hour']
    cat_cols = ['previous_education']
    
    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(drop='first'), cat_cols)
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    report.append(f"Train set: {X_train.shape}, Test set: {X_test.shape}\n")
    
    with open(os.path.join(ARTIFACTS_DIR, "feature_engineering_report.md"), "w") as f:
        f.writelines(report)
        
    return X_train, X_test, y_train, y_test, preprocessor, num_cols, cat_cols

# 4. Train and Evaluate
def train_evaluate(X_train, X_test, y_train, y_test, preprocessor, num_cols, cat_cols):
    models = {
        'Logistic Regression': LogisticRegression(random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42),
        'SVM': SVC(probability=True, random_state=42)
    }
    
    results = {}
    best_model = None
    best_auc = 0
    best_name = ""
    
    for name, model in models.items():
        clf = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)
        
        results[name] = {'Accuracy': acc, 'Precision': prec, 'Recall': rec, 'F1': f1, 'ROC-AUC': auc, 'CM': cm}
        
        if auc > best_auc:
            best_auc = auc
            best_model = clf
            best_name = name

    # Save model
    joblib.dump(best_model, os.path.join(MODELS_DIR, "best_model.pkl"))
    
    # Generate Evaluation Report
    report = ["# Model Evaluation Report\n"]
    for name, metrics in results.items():
        report.append(f"## {name}\n")
        report.append(f"- Accuracy: {metrics['Accuracy']:.4f}\n")
        report.append(f"- Precision: {metrics['Precision']:.4f}\n")
        report.append(f"- Recall: {metrics['Recall']:.4f}\n")
        report.append(f"- F1 Score: {metrics['F1']:.4f}\n")
        report.append(f"- ROC-AUC: {metrics['ROC-AUC']:.4f}\n")
        report.append(f"- Confusion Matrix:\n```\n{metrics['CM']}\n```\n\n")
        
    report.append(f"## Best Model: {best_name} (ROC-AUC: {best_auc:.4f})\n")
    report.append("Model saved as `best_model.pkl`\n")
    
    with open(os.path.join(ARTIFACTS_DIR, "model_evaluation_report.md"), "w") as f:
        f.writelines(report)

if __name__ == "__main__":
    df = generate_data()
    df = process_and_eda(df)
    X_train, X_test, y_train, y_test, preprocessor, num_cols, cat_cols = fe_and_split(df)
    train_evaluate(X_train, X_test, y_train, y_test, preprocessor, num_cols, cat_cols)
    print("Pipeline executed successfully.")
