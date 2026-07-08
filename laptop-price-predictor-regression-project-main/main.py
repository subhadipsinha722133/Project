import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor, ExtraTreesRegressor, VotingRegressor, StackingRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
import pickle
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data():
    """Load and preprocess the laptop data"""
    print("Loading data...")
    df = pd.read_csv('laptop_data.csv')
    
    # Initial preprocessing
    df.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')
    
    # Clean Ram and Weight columns
    df['Ram'] = df['Ram'].str.replace('GB', '')
    df['Weight'] = df['Weight'].str.replace('kg', '')
    df['Ram'] = df['Ram'].astype('int32')
    df['Weight'] = df['Weight'].astype('float32')
    
    return df

def feature_engineering(df):
    """Perform feature engineering on the dataset"""
    print("Performing feature engineering...")
    
    # Screen Resolution features
    df['Touchscreen'] = df['ScreenResolution'].apply(lambda x: 1 if 'Touchscreen' in x else 0)
    df['Ips'] = df['ScreenResolution'].apply(lambda x: 1 if 'IPS' in x else 0)
    
    # Extract resolution
    new = df['ScreenResolution'].str.split('x', n=1, expand=True)
    df['X_res'] = new[0]
    df['Y_res'] = new[1]
    df['X_res'] = df['X_res'].str.replace(',', '').str.findall(r'(\d+\.?\d+)').apply(lambda x: x[0])
    df['X_res'] = df['X_res'].astype('int')
    df['Y_res'] = df['Y_res'].astype('int')
    
    # Calculate PPI
    df['ppi'] = (((df['X_res']**2) + (df['Y_res']**2))**0.5/df['Inches']).astype('float')
    df.drop(columns=['ScreenResolution', 'Inches', 'X_res', 'Y_res'], inplace=True)
    
    # CPU features
    df['Cpu Name'] = df['Cpu'].apply(lambda x: " ".join(x.split()[0:3]))
    
    def fetch_processor(text):
        if text == 'Intel Core i7' or text == 'Intel Core i5' or text == 'Intel Core i3':
            return text
        else:
            if text.split()[0] == 'Intel':
                return 'Other Intel Processor'
            else:
                return 'AMD Processor'
    
    df['Cpu brand'] = df['Cpu Name'].apply(fetch_processor)
    df.drop(columns=['Cpu', 'Cpu Name'], inplace=True)
    
    # Memory features
    df['Memory'] = df['Memory'].astype(str).replace('\.0', '', regex=True)
    df["Memory"] = df["Memory"].str.replace('GB', '')
    df["Memory"] = df["Memory"].str.replace('TB', '000')
    new = df["Memory"].str.split("+", n=1, expand=True)
    
    df["first"] = new[0]
    df["first"] = df["first"].str.strip()
    df["second"] = new[1]
    df["second"].fillna("0", inplace=True)
    
    # Extract storage types
    df["Layer1HDD"] = df["first"].apply(lambda x: 1 if "HDD" in x else 0)
    df["Layer1SSD"] = df["first"].apply(lambda x: 1 if "SSD" in x else 0)
    df["Layer1Hybrid"] = df["first"].apply(lambda x: 1 if "Hybrid" in x else 0)
    df["Layer1Flash_Storage"] = df["first"].apply(lambda x: 1 if "Flash Storage" in x else 0)
    
    df["Layer2HDD"] = df["second"].apply(lambda x: 1 if "HDD" in x else 0)
    df["Layer2SSD"] = df["second"].apply(lambda x: 1 if "SSD" in x else 0)
    df["Layer2Hybrid"] = df["second"].apply(lambda x: 1 if "Hybrid" in x else 0)
    df["Layer2Flash_Storage"] = df["second"].apply(lambda x: 1 if "Flash Storage" in x else 0)
    
    # Extract numeric values
    df['first'] = df['first'].str.extract('(\d+)').fillna('0')
    df['second'] = df['second'].str.extract('(\d+)').fillna('0')
    df["first"] = df["first"].astype(int)
    df["second"] = df["second"].astype(int)
    
    # Calculate final storage values
    df["HDD"] = (df["first"] * df["Layer1HDD"] + df["second"] * df["Layer2HDD"])
    df["SSD"] = (df["first"] * df["Layer1SSD"] + df["second"] * df["Layer2SSD"])
    df["Hybrid"] = (df["first"] * df["Layer1Hybrid"] + df["second"] * df["Layer2Hybrid"])
    df["Flash_Storage"] = (df["first"] * df["Layer1Flash_Storage"] + df["second"] * df["Layer2Flash_Storage"])
    
    df.drop(columns=['first', 'second', 'Layer1HDD', 'Layer1SSD', 'Layer1Hybrid',
                     'Layer1Flash_Storage', 'Layer2HDD', 'Layer2SSD', 'Layer2Hybrid',
                     'Layer2Flash_Storage', 'Memory', 'Hybrid', 'Flash_Storage'], inplace=True)
    
    # GPU features
    df['Gpu brand'] = df['Gpu'].apply(lambda x: x.split()[0])
    df = df[df['Gpu brand'] != 'ARM']
    df.drop(columns=['Gpu'], inplace=True)
    
    # OS features
    def cat_os(inp):
        if inp == 'Windows 10' or inp == 'Windows 7' or inp == 'Windows 10 S':
            return 'Windows'
        elif inp == 'macOS' or inp == 'Mac OS X':
            return 'Mac'
        else:
            return 'Others/No OS/Linux'
    
    df['os'] = df['OpSys'].apply(cat_os)
    df.drop(columns=['OpSys'], inplace=True)
    
    return df

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple models and return the best one"""
    print("Training models...")
    
    # Define column transformer
    step1 = ColumnTransformer(transformers=[
        ('col_tnf', OneHotEncoder(drop='first'), [0, 1, 7, 10, 11])
    ], remainder='passthrough')
    
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=10),
        'Lasso Regression': Lasso(alpha=0.001),
        'KNN': KNeighborsRegressor(n_neighbors=3),
        'Decision Tree': DecisionTreeRegressor(max_depth=8),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=3, 
                                              max_features=0.75, max_depth=15,
                                              bootstrap=True, max_samples=0.5),  # Added bootstrap=True
        'Extra Trees': ExtraTreesRegressor(n_estimators=100, random_state=3,
                                          max_features=0.75, max_depth=15,
                                          bootstrap=True, max_samples=0.5),  # Added bootstrap=True
        'XGBoost': XGBRegressor(n_estimators=45, max_depth=5, learning_rate=0.5),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=500)
    }
    
    best_score = -float('inf')
    best_model = None
    best_model_name = ""
    
    for name, model in models.items():
        try:
            pipe = Pipeline([
                ('step1', step1),
                ('step2', model)
            ])
            
            pipe.fit(X_train, y_train)
            y_pred = pipe.predict(X_test)
            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            
            print(f"{name}: R2 = {r2:.4f}, MAE = {mae:.4f}")
            
            if r2 > best_score:
                best_score = r2
                best_model = pipe
                best_model_name = name
        except Exception as e:
            print(f"Error training {name}: {str(e)}")
            continue
    
    # Try ensemble methods
    print("\nTraining ensemble models...")
    
    # Voting Regressor - Fixed parameters
    rf = RandomForestRegressor(n_estimators=350, random_state=3, 
                              max_features=0.75, max_depth=15,
                              bootstrap=True, max_samples=0.5)  # Removed max_samples or added bootstrap
    gbdt = GradientBoostingRegressor(n_estimators=100, max_features=0.5)
    xgb = XGBRegressor(n_estimators=25, learning_rate=0.3, max_depth=5)
    et = ExtraTreesRegressor(n_estimators=100, random_state=3,
                            max_features=0.75, max_depth=10,
                            bootstrap=True, max_samples=0.5)  # Fixed parameters
    
    try:
        voting_pipe = Pipeline([
            ('step1', step1),
            ('step2', VotingRegressor([('rf', rf), ('gbdt', gbdt), ('xgb', xgb), ('et', et)], 
                                     weights=[5, 1, 1, 1]))
        ])
        
        voting_pipe.fit(X_train, y_train)
        y_pred_voting = voting_pipe.predict(X_test)
        r2_voting = r2_score(y_test, y_pred_voting)
        mae_voting = mean_absolute_error(y_test, y_pred_voting)
        
        print(f"Voting Regressor: R2 = {r2_voting:.4f}, MAE = {mae_voting:.4f}")
        
        if r2_voting > best_score:
            best_score = r2_voting
            best_model = voting_pipe
            best_model_name = "Voting Regressor"
    except Exception as e:
        print(f"Error training Voting Regressor: {str(e)}")
    
    # Stacking Regressor - Fixed parameters
    estimators = [
        ('rf', RandomForestRegressor(n_estimators=350, random_state=3,
                                    max_features=0.75, max_depth=15,
                                    bootstrap=True, max_samples=0.5)),
        ('gbdt', GradientBoostingRegressor(n_estimators=100, max_features=0.5)),
        ('xgb', XGBRegressor(n_estimators=25, learning_rate=0.3, max_depth=5))
    ]
    
    try:
        stacking_pipe = Pipeline([
            ('step1', step1),
            ('step2', StackingRegressor(estimators=estimators, final_estimator=Ridge(alpha=100)))
        ])
        
        stacking_pipe.fit(X_train, y_train)
        y_pred_stacking = stacking_pipe.predict(X_test)
        r2_stacking = r2_score(y_test, y_pred_stacking)
        mae_stacking = mean_absolute_error(y_test, y_pred_stacking)
        
        print(f"Stacking Regressor: R2 = {r2_stacking:.4f}, MAE = {mae_stacking:.4f}")
        
        if r2_stacking > best_score:
            best_score = r2_stacking
            best_model = stacking_pipe
            best_model_name = "Stacking Regressor"
    except Exception as e:
        print(f"Error training Stacking Regressor: {str(e)}")
    
    print(f"\nBest model: {best_model_name} with R2 score: {best_score:.4f}")
    
    return best_model

def main():
    """Main function to run the complete training pipeline"""
    print("Starting Laptop Price Prediction Training Pipeline...")
    
    # Load and preprocess data
    df = load_and_preprocess_data()
    
    # Feature engineering
    df = feature_engineering(df)
    
    print(f"Final dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Prepare features and target
    X = df.drop(columns=['Price'])
    y = np.log(df['Price'])  # Using log transformation for price
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=2)
    
    print(f"Training set shape: {X_train.shape}")
    print(f"Test set shape: {X_test.shape}")
    
    # Train models and get the best one
    best_model = train_models(X_train, X_test, y_train, y_test)
    
    # Save the model and data
    print("\nSaving model and data...")
    pickle.dump(df, open('df.pkl', 'wb'))
    pickle.dump(best_model, open('pipe.pkl', 'wb'))
    
    print("Training completed successfully!")
    print("Files saved: 'df.pkl' and 'pipe.pkl'")

if __name__ == "__main__":
    main()