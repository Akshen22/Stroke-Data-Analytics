import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

class DatasetLoader:
    """Class to load, clean, and preprocess the stroke dataset."""
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.scaler = StandardScaler()

    def load_data(self):
        """Load the dataset from a CSV file."""
        try:
            self.data = pd.read_csv(self.file_path)
            print("Dataset loaded successfully.")
            return self.data
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found.")
            return None

    def clean_data(self):
        """Clean the dataset by handling missing values, encoding, and scaling."""
        if self.data is None:
            print("Error: Data not loaded.")
            return None

        # Handle missing numerical values with median
        numerical_cols = self.data.select_dtypes(include=['float64', 'int64']).columns
        for col in numerical_cols:
            self.data[col] = self.data[col].fillna(self.data[col].median())

        # Handle missing categorical values with mode
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            self.data[col] = self.data[col].fillna(self.data[col].mode()[0])

        # Encode categorical variables
        le = LabelEncoder()
        for col in categorical_cols:
            self.data[col] = le.fit_transform(self.data[col])

        # Feature engineering
        self.compute_features()

        # Define categorical columns to exclude from scaling
        categorical_cols = ['Chronic Stress', 'Physical Activity', 'Income Level', 'Stroke Occurrence', 
                           'Hypertension', 'Heart Disease', 'Ever Married', 'Work Type', 
                           'Residence Type', 'Smoking Status', 'Dietary Habits', 
                           'Alcohol Consumption', 'Family History of Stroke', 
                           'Education Level', 'Region', 'Cardiovascular_Condition', 
                           'BMI_Category', 'High_Glucose_Risk']

        # Ensure categorical columns are integers
        for col in categorical_cols:
            if col in self.data.columns:
                self.data[col] = self.data[col].astype('int64')

        # Scale only non-categorical numerical columns
        numerical_cols = [col for col in self.data.select_dtypes(include=['float64', 'int64']).columns 
                         if col not in categorical_cols]
        if numerical_cols:
            self.data[numerical_cols] = self.scaler.fit_transform(self.data[numerical_cols])

        print("Data cleaned, features computed, and scaled (excluding categorical columns).")
        return self.data

    def compute_features(self):
        """Compute additional statistical features for the dataset."""
        if self.data is None:
            print("Error: Data not loaded.")
            return None

        # Create a binary feature for cardiovascular conditions
        if 'Hypertension' in self.data.columns and 'Heart Disease' in self.data.columns:
            self.data['Cardiovascular_Condition'] = (self.data['Hypertension'] | self.data['Heart Disease']).astype(int)

        # Categorize BMI into standard ranges
        if 'BMI' in self.data.columns:
            self.data['BMI_Category'] = pd.cut(self.data['BMI'], 
                                              bins=[0, 18.5, 25, 30, float('inf')], 
                                              labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
            le = LabelEncoder()
            self.data['BMI_Category'] = le.fit_transform(self.data['BMI_Category'])

        # Threshold for high glucose risk
        if 'Average Glucose Level' in self.data.columns:
            self.data['High_Glucose_Risk'] = (self.data['Average Glucose Level'] > 200).astype(int)

        # Interaction feature: Age * Physical Activity
        if 'Age' in self.data.columns and 'Physical Activity' in self.data.columns:
            self.data['Activity_Age_Interaction'] = self.data['Age'] * self.data['Physical Activity']

        # Ratio feature: Sleep Hours / Physical Activity
        if 'Sleep Hours' in self.data.columns and 'Physical Activity' in self.data.columns:
            self.data['Sleep_Activity_Ratio'] = self.data['Sleep Hours'] / (self.data['Physical Activity'] + 1)  # Avoid division by zero

    def split_data(self, target_column, test_size=0.2, random_state=42):
        """Split the dataset into training and test sets, avoiding data leakage."""
        if self.data is None or target_column not in self.data.columns:
            print(f"Error: Data not loaded or {target_column} not found.")
            return None, None, None, None

        # Exclude features that include the target to prevent leakage
        exclude_cols = [target_column]
        if target_column == 'Physical Activity':
            exclude_cols.extend(['Activity_Age_Interaction', 'Sleep_Activity_Ratio'])

        X = self.data.drop(columns=exclude_cols)
        y = self.data[target_column]
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    