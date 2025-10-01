import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score
import os

class MLModels:
    """Class for training and evaluating machine learning models."""
    def __init__(self, X_train, X_test, y_train, y_test):
        """Initialize with training and test data."""
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.models = {
            'Naive Bayes': GaussianNB(var_smoothing=1e-8),  # Small smoothing for stability
            'Random Forest': RandomForestClassifier(max_depth=10, min_samples_split=10, random_state=42),
            'XGBoost': XGBClassifier(max_depth=6, min_child_weight=5, eval_metric='mlogloss', random_state=42)
        }
        self.results = {}
        if not os.path.exists('plots'):
            os.makedirs('plots')

    def train_and_evaluate(self, target_name, save_path='plots/'):
        """Train and evaluate models for a given target."""
        self.results[target_name] = {}
        for model_name, model in self.models.items():
            # Train the model
            model.fit(self.X_train, self.y_train)
            # Predict
            y_pred = model.predict(self.X_test)
            # Evaluate
            self.results[target_name][model_name] = {
                'Accuracy': accuracy_score(self.y_test, y_pred),
                'Precision': precision_score(self.y_test, y_pred, average='weighted', zero_division=0),
                'Recall': recall_score(self.y_test, y_pred, average='weighted', zero_division=0),
                'Confusion Matrix': confusion_matrix(self.y_test, y_pred)
            }
            # Plot confusion matrix
            plt.figure(figsize=(6, 4))
            sns.heatmap(self.results[target_name][model_name]['Confusion Matrix'], annot=True, fmt='d', cmap='Blues')
            plt.title(f'Confusion Matrix for {model_name} - {target_name}', fontsize=12)
            plt.xlabel('Predicted', fontsize=10)
            plt.ylabel('Actual', fontsize=10)
            confusion_path = f'{save_path}{model_name}_{target_name}_confusion_matrix.png'
            plt.savefig(confusion_path)
            print(f"Confusion matrix saved at: {confusion_path}")
            plt.close()

    def plot_model_comparison(self, target_name, save_path='plots/'):
        """Plot comparison of model performance."""
        metrics = ['Accuracy', 'Precision', 'Recall']
        data = pd.DataFrame({
            metric: [self.results[target_name][model][metric] for model in self.models]
            for metric in metrics
        }, index=self.models.keys())
        
        plt.figure(figsize=(10, 6))
        data.plot(kind='bar', color=['#95a5a6', '#3498db', '#e74c3c'])  # High-contrast colors
        plt.title(f'Model Performance Comparison for {target_name}', fontsize=15)
        plt.ylabel('Score', fontsize=12)
        plt.ylim(0, 1)
        plt.xticks(rotation=45)
        plt.legend(loc='best')
        plt.tight_layout()
        comparison_path = f'{save_path}{target_name}_model_comparison.png'
        plt.savefig(comparison_path)
        print(f"Model comparison plot saved at: {comparison_path}")
        plt.close()
        return data
    