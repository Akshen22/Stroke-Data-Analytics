import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
import os
import numpy as np

class EDA:
    """Class for performing exploratory data analysis on the stroke dataset."""
    def __init__(self, data):
        self.data = data
        if not os.path.exists('plots'):
            os.makedirs('plots')

    def descriptive_statistics(self):
        """Compute descriptive statistics for numerical columns."""
        if self.data is None:
            print("Error: Data not loaded.")
            return None
        return self.data.describe()

    def plot_distribution(self, column, plot_type='histogram', save_path='plots/'):
        """Plot distribution of a specified column."""
        if self.data is None or column not in self.data.columns:
            print(f"Error: Data not loaded or {column} not found.")
            return

        plt.figure(figsize=(8, 6))
        if plot_type == 'histogram' and self.data[column].dtype in ['int64', 'float64']:
            sns.histplot(self.data[column], kde=True)
            plt.title(f'Distribution of {column}', fontsize=12)
            plt.xlabel(column, fontsize=10)
            plt.ylabel('Frequency', fontsize=10)
        elif plot_type == 'bar':
            sns.countplot(x=column, data=self.data)
            plt.title(f'Class Distribution of {column}', fontsize=12)
            plt.xlabel(column, fontsize=10)
            plt.ylabel('Count', fontsize=10)
        plt.savefig(f'{save_path}{column}_{plot_type}.png')
        plt.close()

    def check_class_balance(self, target_column, save_path='plots/'):
        """Check and address class imbalance for the target column."""
        if self.data is None or target_column not in self.data.columns:
            print(f"Error: Data not loaded or {target_column} not found.")
            return None

        # Ensure target is categorical
        y = self.data[target_column]
        if y.dtype in ['float64', 'float32']:
            print(f"Warning: {target_column} appears continuous. Converting to discrete labels.")
            # Assume binary classification; threshold at mean
            y = (y > y.mean()).astype(int)
            self.data[target_column] = y

        # Plot class distribution
        self.plot_distribution(target_column, plot_type='bar')

        # Check class balance
        class_counts = self.data[target_column].value_counts()
        print(f"Class distribution for {target_column} (before SMOTE):\n{class_counts}")

        # Apply SMOTE for multi-class imbalance
        if class_counts.min() / class_counts.max() < 0.5:  # Threshold for imbalance
            print(f"Applying SMOTE to balance {target_column} classes.")
            X = self.data.drop(columns=[target_column])
            y = self.data[target_column]
            try:
                smote = SMOTE(sampling_strategy='auto', random_state=42)  # Balance all classes evenly
                X_balanced, y_balanced = smote.fit_resample(X, y)
                balanced_data = pd.concat([pd.DataFrame(X_balanced, columns=X.columns), 
                                          pd.Series(y_balanced, name=target_column)], axis=1)
                print(f"Balanced class distribution for {target_column} (after SMOTE):\n{balanced_data[target_column].value_counts()}")
                return balanced_data
            except ValueError as e:
                print(f"Error applying SMOTE: {e}. Returning original data.")
                return self.data
        return self.data
    