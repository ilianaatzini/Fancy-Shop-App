import os
import pandas as pd
from datetime import datetime
import subprocess
import platform
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class SalesManager:
    def __init__(self, excel_filename='sales_records.xlsx'):
        self.excel_filename = excel_filename
        self.invoice_counter = 1
        self.next_invoice_number = 1  # Initial invoice number
        self.product_counters = {}
        self.product_codes = {
            'φορεμα': 'A',
            'φανελα': 'B',
            'μπλουζα': 'C',
            'σορτσακι': 'D',
            'παντελονι': 'E',
            'σετακι': 'F',
            'φουστα': 'G',
            'πουκαμισο': 'H',
            'μπουφαν': 'I',
            'ζωνη': 'J'
        }

        if not os.path.exists(self.excel_filename):
            self.create_excel_file()
        self.load_existing_data()

    def create_excel_file(self):
        with pd.ExcelWriter(self.excel_filename) as writer:
            df_sales = pd.DataFrame(columns=[
                'Invoice Number', 'Date & Time', 'Product Code', 'Product Type', 'Amount'
            ])
            df_sales.to_excel(writer, sheet_name='Sales', index=False)
            
            df_daily = pd.DataFrame(columns=['Date', 'Total Sales'])
            df_daily.to_excel(writer, sheet_name='Daily Totals', index=False)

            df_monthly = pd.DataFrame(columns=['Month', 'Total Sales'])
            df_monthly.to_excel(writer, sheet_name='Monthly Totals', index=False)

            df_yearly = pd.DataFrame(columns=['Year', 'Total Sales'])
            df_yearly.to_excel(writer, sheet_name='Yearly Totals', index=False)

    def load_existing_data(self):
        if not os.path.exists(self.excel_filename):
            self.create_excel_file()

        with pd.ExcelFile(self.excel_filename) as reader:
            df_sales = pd.read_excel(reader, sheet_name='Sales')

            if not df_sales.empty:
                last_invoice_number = df_sales['Invoice Number'].str.extract('(\d+)').astype(int).max()
                self.invoice_counter = int(last_invoice_number + 1)
            else:
                self.invoice_counter = 1
            
            for _, row in df_sales.iterrows():
                product_type = row['Product Type']
                product_code = row['Product Code']
                date_str = product_code[1:7]  # Assuming the date part is at positions 1 to 6
                serial_num = int(product_code[7:])

                if product_type not in self.product_counters:
                    self.product_counters[product_type] = {}

                if date_str not in self.product_counters[product_type]:
                    self.product_counters[product_type][date_str] = serial_num
                else:
                    self.product_counters[product_type][date_str] = max(self.product_counters[product_type][date_str], serial_num)

    def get_next_invoice_number(self):
        current_invoice_number = f"INV{self.invoice_counter:06d}"
        self.invoice_counter += 1  # Increment for the next sale
        return current_invoice_number

    def get_next_product_code(self, product_type):
        date_str = datetime.now().strftime('%y%m%d')
        if product_type not in self.product_counters:
            self.product_counters[product_type] = {}
        
        if date_str not in self.product_counters[product_type]:
            self.product_counters[product_type][date_str] = 1
        else:
            self.product_counters[product_type][date_str] += 1

        count = self.product_counters[product_type][date_str]
        return f"{self.product_codes[product_type]}{date_str}{count:05d}"

    def update_totals(self, date, amount, quantity):
        daily_date = date.strftime('%Y-%m-%d')
        monthly_date = date.strftime('%Y-%m')
        yearly_date = date.strftime('%Y')

        with pd.ExcelFile(self.excel_filename) as reader:
            df_daily = pd.read_excel(reader, sheet_name='Daily Totals')
            df_monthly = pd.read_excel(reader, sheet_name='Monthly Totals')
            df_yearly = pd.read_excel(reader, sheet_name='Yearly Totals')

        def update_or_append(df, date_column, date_value):
            total_amount = amount * quantity
            if date_value in df[date_column].values:
                df.loc[df[date_column] == date_value, 'Total Sales'] += total_amount
            else:
                # Check if the year already exists in the dataframe
                if any(df[date_column].astype(str).str.endswith(date_value[-4:])):
                    # Update the existing row for that year
                    df.loc[df[date_column].astype(str).str.endswith(date_value[-4:]), 'Total Sales'] += total_amount
                else:
                    # Append a new row for the new year
                    new_row = pd.DataFrame([[date_value, total_amount]], columns=[date_column, 'Total Sales'])
                    df = pd.concat([df, new_row], ignore_index=True)
            return df

        df_daily = update_or_append(df_daily, 'Date', daily_date)
        df_monthly = update_or_append(df_monthly, 'Month', monthly_date)
        df_yearly = update_or_append(df_yearly, 'Year', yearly_date)

        with pd.ExcelWriter(self.excel_filename, mode='a', if_sheet_exists='replace') as writer:
            df_daily.to_excel(writer, sheet_name='Daily Totals', index=False)
            df_monthly.to_excel(writer, sheet_name='Monthly Totals', index=False)
            df_yearly.to_excel(writer, sheet_name='Yearly Totals', index=False)


    def record_sale(self, invoice_number, product_name, quantity, amount):
        product_type = product_name.lower()
        if product_type not in self.product_codes:
            raise ValueError(f"Product type '{product_type}' not recognized.")

        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        product_codes = []
        for _ in range(quantity):
            product_code = self.get_next_product_code(product_type)
            product_codes.append(product_code)
            new_record = {
                'Invoice Number': invoice_number,
                'Date & Time': date_str,
                'Product Code': product_code,
                'Product Type': product_type,
                'Amount': amount
            }

            if os.path.exists(self.excel_filename):
                with pd.ExcelFile(self.excel_filename) as reader:
                    df_sales = pd.read_excel(reader, sheet_name='Sales')
                df_sales = pd.concat([df_sales, pd.DataFrame([new_record])], ignore_index=True)
                with pd.ExcelWriter(self.excel_filename, mode='a', if_sheet_exists='replace') as writer:
                    df_sales.to_excel(writer, sheet_name='Sales', index=False)
            else:
                df_sales = pd.DataFrame([new_record])
                with pd.ExcelWriter(self.excel_filename) as writer:
                    df_sales.to_excel(writer, sheet_name='Sales', index=False)

        self.update_totals(now, amount, quantity)
        print(f"Recorded sale: {new_record}")
        return product_codes