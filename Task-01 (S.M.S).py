import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class StoreManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Store Management System")

        self.sales_data = pd.DataFrame(columns=['Date', 'Item Name', 'Selling Price', 'Cost Price'])

        tk.Label(root, text="Item Name:").grid(row=0, column=0)
        tk.Label(root, text="Selling Price:").grid(row=1, column=0)
        tk.Label(root, text="Cost Price:").grid(row=2, column=0)

        self.item_name_entry = tk.Entry(root)
        self.item_name_entry.grid(row=0, column=1)
        self.selling_price_entry = tk.Entry(root)
        self.selling_price_entry.grid(row=1, column=1)
        self.cost_price_entry = tk.Entry(root)
        self.cost_price_entry.grid(row=2, column=1)

        tk.Button(root, text="Submit", command=self.submit_data).grid(row=3, columnspan=2)

        # Add a Date Entry Widget for selecting the date
        tk.Label(root, text="Select Date:").grid(row=4, column=0)
        self.selected_date_entry = tk.Entry(root)
        self.selected_date_entry.grid(row=4, column=1)

        # Add a Button for generating the daily report
        tk.Button(root, text="Generate Daily Report", command=self.generate_daily_report).grid(row=5, columnspan=2)

        # Add a Button for generating the monthly report
        tk.Button(root, text="Generate Monthly Report", command=self.generate_monthly_report).grid(row=6, columnspan=2)

    def submit_data(self):
        item_name = self.item_name_entry.get()
        selling_price = float(self.selling_price_entry.get())
        cost_price = float(self.cost_price_entry.get())
        today = date.today().strftime("%Y-%m-%d")

        new_row = pd.DataFrame({'Date': [today], 'Item Name': [item_name], 'Selling Price': [selling_price], 'Cost Price': [cost_price]})
        self.sales_data = pd.concat([self.sales_data, new_row], ignore_index=True)

        messagebox.showinfo("Success", "Data submitted successfully!")


    def generate_daily_report(self):
        # Get the selected date
        selected_date = self.selected_date_entry.get()  

        # Filter the DataFrame to get data for the selected date
        daily_sales_data = self.sales_data[self.sales_data['Date'] == selected_date]

        if daily_sales_data.empty:
            messagebox.showinfo("Error", "No data available for selected date.")
            return

        # Calculate total sales and profit for the day
        total_sales = daily_sales_data['Selling Price'].sum()
        total_cost = daily_sales_data['Cost Price'].sum()
        total_profit = total_sales - total_cost

        # Display the daily report
        report_text = f"Daily Report for {selected_date}\n\n"
        report_text += f"Total Sales: {total_sales}\n"
        report_text += f"Total Profit: {total_profit}\n"

        messagebox.showinfo("Daily Report", report_text)

    def generate_monthly_report(self):
        # Group sales data by month
        self.sales_data['Date'] = pd.to_datetime(self.sales_data['Date'])  # Convert 'Date' column to datetime
        self.sales_data['Month'] = self.sales_data['Date'].dt.strftime('%Y-%m')  # Extract month from 'Date'

        monthly_sales_data = self.sales_data.groupby('Month').agg({'Selling Price': 'sum', 'Cost Price': 'sum'}).reset_index()
        monthly_sales_data['Profit'] = monthly_sales_data['Selling Price'] - monthly_sales_data['Cost Price']

        if monthly_sales_data.empty:
            messagebox.showinfo("Error", "No sales data available for generating monthly report.")
            return

        # Plot the monthly report data
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(monthly_sales_data['Month'], monthly_sales_data['Selling Price'], label='Total Sales')
        ax.bar(monthly_sales_data['Month'], monthly_sales_data['Profit'], label='Total Profit')

        ax.set_xlabel('Month')
        ax.set_ylabel('Amount')
        ax.set_title('Monthly Sales and Profit Report')
        ax.legend()

        # Save the plot as a PDF file
        pdf_file_path = "monthly_report.pdf"
        with PdfPages(pdf_file_path) as pdf:
            pdf.savefig(fig)

        # Display a message to the user
        messagebox.showinfo("Monthly Report", f"Monthly report saved as {pdf_file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StoreManagementSystem(root)
    root.mainloop()
