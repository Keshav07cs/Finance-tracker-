from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

# Path to the CSV file
csv_file = 'finance_data.csv'

# Load data from CSV file
if os.path.exists(csv_file):
    data = pd.read_csv(csv_file)
else:
    data = pd.DataFrame(columns=['Date', 'Description', 'Category', 'Amount'])

@app.route('/')
def index():
    return render_template('index.html', transactions=data.to_dict(orient='records'))

@app.route('/add', methods=['POST'])
def add_transaction():
    global data
    try:
        date = request.form['date']
        description = request.form['description']
        category = request.form['category'].capitalize()
        amount = float(request.form['amount'])

        # Convert date string to a date object
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()

        # Create a new DataFrame for the new transaction
        new_transaction = pd.DataFrame([{
            'Date': date_obj,
            'Description': description,
            'Category': category,
            'Amount': amount
        }])

        # Append new transaction to existing data
        data = pd.concat([data, new_transaction], ignore_index=True)

        # Save to CSV file
        data.to_csv(csv_file, index=False)

        flash('Transaction added successfully!', 'success')
    except Exception as e:
        flash('Error adding transaction: ' + str(e), 'danger')

    return redirect(url_for('index'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_transaction(index):
    global data
    if request.method == 'POST':
        try:
            date = request.form['date']
            description = request.form['description']
            category = request.form['category'].capitalize()
            amount = float(request.form['amount'])

            # Validate index
            if index < 0 or index >= len(data):
                flash('Invalid transaction index.', 'danger')
                return redirect(url_for('index'))

            # Convert date string to a date object
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()

            # Update the transaction
            data.loc[index] = [date_obj, description, category, amount]

            # Save to CSV file
            data.to_csv(csv_file, index=False)

            flash('Transaction updated successfully!', 'success')
        except Exception as e:
            flash('Error updating transaction: ' + str(e), 'danger')

        return redirect(url_for('index'))

    # Pre-fill the edit form
    transaction = data.iloc[index]
    return render_template('edit.html', transaction=transaction, index=index)

@app.route('/delete/<int:index>', methods=['POST'])
def delete_transaction(index):
    global data
    try:
        # Validate index
        if index < 0 or index >= len(data):
            flash('Invalid transaction index.', 'danger')
            return redirect(url_for('index'))

        # Delete the transaction
        data = data.drop(index).reset_index(drop=True)

        # Save to CSV file
        data.to_csv(csv_file, index=False)

        flash('Transaction deleted successfully!', 'success')
    except Exception as e:
        flash('Error deleting transaction: ' + str(e), 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)