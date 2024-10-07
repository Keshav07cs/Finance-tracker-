import os
import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle  # Import for background color
from datetime import datetime

class FinanceTrackerApp(App):
    def build(self):
        # Path to the CSV file
        self.csv_file = 'finance_data.csv'

        # Check if the CSV file exists, and load it if it does
        if os.path.exists(self.csv_file):
            self.data = pd.read_csv(self.csv_file)
            print("Loaded data:")
            print(self.data)
        else:
            # Initialize an empty DataFrame if the file doesn't exist
            self.data = pd.DataFrame(columns=['Date', 'Description', 'Category', 'Amount'])

        # Create the layout and UI elements
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Set background color for layout
        with layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light grey background
            self.rect = Rectangle(size=(800, 600), pos=layout.pos)

        self.date_input = TextInput(hint_text='Date (YYYY-MM-DD)', multiline=False,
                                    background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.description_input = TextInput(hint_text='Description', multiline=False,
                                           background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.category_input = TextInput(hint_text='Category (Income/Expense)', multiline=False,
                                        background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.amount_input = TextInput(hint_text='Amount', multiline=False,
                                      background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

        add_button = Button(text="Add Transaction", on_press=self.add_transaction,
                            background_color=(0.3, 0.5, 1, 1), color=(1, 1, 1, 1))
        view_button = Button(text="View All Transactions", on_press=self.view_transactions,
                             background_color=(0.3, 0.5, 1, 1), color=(1, 1, 1, 1))
        
        self.result_label = Label(text="Summary will be shown here.", size_hint_y=None, height=600, color=(0, 0, 0, 1))
        
        self.scroll_view = ScrollView(size_hint=(1, None), size=(600, 400))
        self.scroll_view.add_widget(self.result_label)

        # New input and button for editing transaction
        self.edit_index_input = TextInput(hint_text='Transaction Index to Edit', multiline=False,
                                          background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        edit_button = Button(text="Edit Transaction", on_press=self.edit_transaction,
                             background_color=(0.3, 0.5, 1, 1), color=(1, 1, 1, 1))
        
        # New input and button for deleting transaction
        self.delete_index_input = TextInput(hint_text='Transaction Index to Delete', multiline=False,
                                            background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        delete_button = Button(text="Delete Transaction", on_press=self.delete_transaction,
                               background_color=(0.3, 0.5, 1, 1), color=(1, 1, 1, 1))

        # Add widgets to the layout with spacing
        layout.add_widget(self.date_input)
        layout.add_widget(self.description_input)
        layout.add_widget(self.category_input)
        layout.add_widget(self.amount_input)
        layout.add_widget(Widget(size_hint_y=None, height=10))  # Add spacing
        layout.add_widget(add_button)
        layout.add_widget(view_button)
        layout.add_widget(Widget(size_hint_y=None, height=10))  # Add spacing
        layout.add_widget(self.edit_index_input)
        layout.add_widget(edit_button)
        layout.add_widget(self.delete_index_input)
        layout.add_widget(delete_button)
        layout.add_widget(self.scroll_view)

        return layout

    def add_transaction(self, instance):
        try:
            # Retrieve input data
            date_str = self.date_input.text
            description = self.description_input.text
            category = self.category_input.text.capitalize()
            amount = float(self.amount_input.text)

            # Convert date string to a date object
            date = datetime.strptime(date_str, '%Y-%m-%d').date()

            # Add the new transaction to the DataFrame using pd.concat
            new_transaction = pd.DataFrame([{'Date': date, 'Description': description, 'Category': category, 'Amount': amount}])
            self.data = pd.concat([self.data, new_transaction], ignore_index=True)

            # Save the updated DataFrame to the CSV file
            self.data.to_csv(self.csv_file, index=False)

            # Update the result label to confirm the transaction was added
            self.result_label.text = f"Transaction added: {description} for {amount:.2f}"

            print("Data saved:")
            print(self.data)

            # Clear inputs after adding transaction
            self.date_input.text = ''
            self.description_input.text = ''
            self.category_input.text = ''
            self.amount_input.text = ''

        except ValueError:
            # Handle potential errors in input data
            self.result_label.text = "Please enter valid data."

    def view_transactions(self, instance):
        # Function to handle the viewing of all transactions
        if not self.data.empty:
            formatted_data = self.data.to_string(index=False, header=True)
        else:
            formatted_data = "No transactions to display."

        self.result_label.text = f"All Transactions:\n{formatted_data}"

        # Update the scroll view to fit the new content
        self.scroll_view.scroll_y = 1

    def edit_transaction(self, instance):
        try:
            # Retrieve the index of the transaction to edit
            index = int(self.edit_index_input.text)
            print(f"Editing transaction at index: {index}")

            # Check if the index is valid
            if index < 0 or index >= len(self.data):
                self.result_label.text = "Invalid index. Please enter a valid transaction index."
                return

            # Retrieve input data
            date_str = self.date_input.text
            description = self.description_input.text
            category = self.category_input.text.capitalize()
            amount = float(self.amount_input.text)

            print(f"Input data - Date: {date_str}, Description: {description}, Category: {category}, Amount: {amount}")

            # Validate and parse the date
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                self.result_label.text = "Invalid date format. Please use YYYY-MM-DD."
                return

            # Update the transaction at the specified index
            self.data.loc[index] = [date, description, category, amount]

            # Save the updated DataFrame to the CSV file
            self.data.to_csv(self.csv_file, index=False)

            # Update the result label to confirm the transaction was updated
            self.result_label.text = f"Transaction at index {index} updated."

            print("Data updated:")
            print(self.data)

            # Clear inputs after editing transaction
            self.date_input.text = ''
            self.description_input.text = ''
            self.category_input.text = ''
            self.amount_input.text = ''
            self.edit_index_input.text = ''

        except (ValueError, IndexError):
            # Handle potential errors in input data
            self.result_label.text = "Please enter valid index and data."

    def delete_transaction(self, instance):
        try:
            # Retrieve the index of the transaction to delete
            index = int(self.delete_index_input.text)
            print(f"Deleting transaction at index: {index}")

            # Check if the index is valid
            if index < 0 or index >= len(self.data):
                self.result_label.text = "Invalid index. Please enter a valid transaction index."
                return

            # Delete the transaction at the specified index
            self.data = self.data.drop(index).reset_index(drop=True)

            # Save the updated DataFrame to the CSV file
            self.data.to_csv(self.csv_file, index=False)

            # Update the result label to confirm the transaction was deleted
            self.result_label.text = f"Transaction at index {index} deleted."

            print("Data updated after deletion:")
            print(self.data)

            # Clear the delete index input
            self.delete_index_input.text = ''

        except (ValueError, IndexError):
            # Handle potential errors in input data
            self.result_label.text = "Please enter a valid index."

if __name__ == '__main__':
    FinanceTrackerApp().run()