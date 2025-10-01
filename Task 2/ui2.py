from load2 import DatasetLoader
from eda2 import EDA

class UserInterfaceCLI:
    """Class for a command-line interface for the stroke data analytics system."""
    def __init__(self, dataset_loader, eda):
        self.loader = dataset_loader
        self.eda = eda

    def display_menu(self):
        """Display the CLI menu."""
        print("\n=== Stroke Data Analytics System ===")
        print("1. Load and Clean Dataset")
        print("2. Perform Exploratory Data Analysis (EDA)")
        print("3. Exit")
        print("===================================")

    def load_and_clean(self):
        """Load and clean the dataset."""
        self.loader.load_data()
        self.loader.clean_data()
        print("Dataset loaded and cleaned successfully.")

    def perform_eda(self):
        """Perform EDA and display results."""
        if self.loader.data is not None:
            stats = self.eda.descriptive_statistics()
            self.eda.plot_distribution('Age', 'histogram')
            self.eda.plot_distribution('Stroke Occurrence', 'bar')
            self.eda.check_class_balance('Stroke Occurrence')
            print("EDA completed. Plots saved in 'plots/' folder.")
            print("\nDescriptive Statistics:")
            print(stats)
        else:
            print("Error: Please load dataset first.")

    def run(self):
        """Run the CLI."""
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-3): ").strip()
            if choice == '1':
                self.load_and_clean()
            elif choice == '2':
                self.perform_eda()
            elif choice == '3':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                