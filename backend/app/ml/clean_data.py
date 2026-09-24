import pandas as pd
import os

def clean_datasets():
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    adults_path = os.path.join(base_dir, 'Adults_15YrsAndUp (1).csv')
    xapi_path = os.path.join(base_dir, 'xAPI-Edu-Data-selected-columns.csv')
    
    out_adults_path = os.path.join(base_dir, 'Adults_cleaned.csv')
    out_xapi_path = os.path.join(base_dir, 'xAPI_cleaned.csv')
    
    # 1. Clean Adults Dataset
    try:
        print("Cleaning Adults dataset...")
        df_adults = pd.read_csv(adults_path, encoding='latin1')
        df_adults.to_csv(out_adults_path, index=False, encoding='utf-8')
        print(f"Saved cleaned Adults dataset to {out_adults_path}")
    except Exception as e:
        print(f"Error cleaning Adults dataset: {e}")

    # 2. Clean xAPI Dataset
    try:
        print("Cleaning xAPI dataset...")
        df_xapi = pd.read_csv(xapi_path)
        
        # We need to ensure we have numeric features for our simple RandomForest
        # Let's encode categorical columns if necessary, or just keep it simple.
        # Columns: 'gender', 'NationalITy', 'PlaceofBirth', 'StageID', 'GradeID', 'SectionID', 'Topic', 'Semester', 'Relation', 'raisedhands'
        
        # Let's map gender to 0/1
        if 'gender' in df_xapi.columns:
            df_xapi['gender_num'] = df_xapi['gender'].map({'M': 0, 'F': 1}).fillna(0)
            
        # We will keep 'Topic' as the string label, the recommender will encode it.
        # And we have 'raisedhands' as a numeric feature.
        
        df_xapi.to_csv(out_xapi_path, index=False, encoding='utf-8')
        print(f"Saved cleaned xAPI dataset to {out_xapi_path}")
        
    except Exception as e:
        print(f"Error cleaning xAPI dataset: {e}")

if __name__ == "__main__":
    clean_datasets()
