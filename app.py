import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import csv
import os
from datetime import datetime
from tkcalendar import DateEntry
from design_pattern import *

class SalesApp:
    def __init__(self):
        self.file_handler = SingletonFileHandler()
        self.observer = Observer()
        self.observer.register(InventoryObserver())
        self.sort_order = {}
        self.show_inventory()
        
    def show_inventory(self):
        self.inventory_window = tk.Tk()
        self.inventory_window.title("Kelola Stok Barang")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Menggunakan tema 'clam' yang lebih modern
        self.style.configure('Treeview', background='#D3D3D3', foreground='black', rowheight=25, fieldbackground='#D3D3D3')
        self.style.map('Treeview', background=[('selected', '#347083')])
        
        self.inventory_tree = ttk.Treeview(self.inventory_window, columns=("Waktu Produk Masuk", "Nama Barang", "Harga", "Jumlah", "Modal"))
        self.inventory_tree.heading("#0", text="No.")
        self.inventory_tree.heading("#1", text="Waktu Produk Masuk")
        self.inventory_tree.heading("#2", text="Nama Barang")
        self.inventory_tree.heading("#3", text="Harga")
        self.inventory_tree.heading("#4", text="Jumlah")
        self.inventory_tree.heading("#5", text="Modal")
        
        for col in self.inventory_tree["columns"]:
            self.inventory_tree.heading(col, text=col, command=lambda _col=col: self.sort_inventory(_col))

        inventory_data = self.load_inventory()
        for i, item in enumerate(inventory_data, start=1):
            self.inventory_tree.insert("", "end", text=str(i), values=item)
        
        self.inventory_tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Menyusun tombol secara rapi dengan menggunakan frame
        button_frame = tk.Frame(self.inventory_window)
        button_frame.pack(pady=5, padx=10, fill="x")
        
        self.add_product_btn = ttk.Button(button_frame, text="Tambah Barang", command=self.add_product)
        self.add_product_btn.pack(side="left", padx=5)

        self.update_product_btn = ttk.Button(button_frame, text="Update Barang", command=self.update_product)
        self.update_product_btn.pack(side="left", padx=5)

        self.delete_product_btn = ttk.Button(button_frame, text="Hapus Barang", command=self.delete_product)
        self.delete_product_btn.pack(side="left", padx=5)

        self.sell_cash_product_btn = ttk.Button(button_frame, text="Jual Barang (Tunai)", command=lambda: self.sell_product_with_payment_type("tunai"))
        self.sell_cash_product_btn.pack(side="left", padx=5)
        
        self.sell_credit_product_btn = ttk.Button(button_frame, text="Jual Barang (Kartu Kredit)", command=lambda: self.sell_product_with_payment_type("kartu kredit"))
        self.sell_credit_product_btn.pack(side="left", padx=5)
        
        self.view_transactions_btn = ttk.Button(button_frame, text="Lihat Riwayat Transaksi", command=self.show_transactions)
        self.view_transactions_btn.pack(side="left", padx=5)

    def load_inventory(self):
        inventory_data = []
        with open(self.file_handler.inventory_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                inventory_data.append(row)
        for x in inventory_data:
            x[2] = int(x[2])
            x[3] = int(x[3])
            x[4] = int(x[4])
        inventory_data[2:] = [list(x) for x in inventory_data[2:]]
        return inventory_data
    
    def quicksort(self, arr, column_index, reverse=False):
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x[column_index] < pivot[column_index]]
        middle = [x for x in arr if x[column_index] == pivot[column_index]]
        right = [x for x in arr if x[column_index] > pivot[column_index]]

        if reverse:
            return self.quicksort(right, column_index, reverse=True) + middle + self.quicksort(left, column_index, reverse=True)
        else:
            return self.quicksort(left, column_index) + middle + self.quicksort(right, column_index)
        
    def sort_inventory(self, column):
        column_index = self.inventory_tree["columns"].index(column)
        inventory_data = self.load_inventory()
        
        if column_index not in self.sort_order or self.sort_order[column_index] == "ascending":
            sorted_data = self.quicksort(inventory_data, column_index)
            self.sort_order[column_index] = "descending"
        else:
            sorted_data = self.quicksort(inventory_data, column_index, reverse=True)
            self.sort_order[column_index] = "ascending"
        
        for i in self.inventory_tree.get_children():
            self.inventory_tree.delete(i)
        
        for i, item in enumerate(sorted_data, start=1):
            self.inventory_tree.insert("", "end", text=str(i), values=item)
    
    def add_product(self):
        self.add_product_window = tk.Toplevel(self.inventory_window)
        self.add_product_window.title("Tambah Barang")
        
        self.product_name_label = tk.Label(self.add_product_window, text="Nama Barang:")
        self.product_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.product_name_entry = tk.Entry(self.add_product_window)
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.price_label = tk.Label(self.add_product_window, text="Harga:")
        self.price_label.grid(row=1, column=0, padx=5, pady=5)
        self.price_entry = tk.Entry(self.add_product_window)
        self.price_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.quantity_label = tk.Label(self.add_product_window, text="Jumlah:")
        self.quantity_label.grid(row=2, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(self.add_product_window)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.cost_price_label = tk.Label(self.add_product_window, text="Harga Modal:")
        self.cost_price_label.grid(row=3, column=0, padx=5, pady=5)
        self.cost_price_entry = tk.Entry(self.add_product_window)
        self.cost_price_entry.grid(row=3, column=1, padx=5, pady=5)
        
        self.submit_product_btn = tk.Button(self.add_product_window, text="Tambah", command=self.save_product)
        self.submit_product_btn.grid(row=4, columnspan=2, padx=5, pady=5)

    def save_product(self):
        product = self.product_name_entry.get()
        price = int(self.price_entry.get())
        quantity = int(self.quantity_entry.get())
        cost_price = int(self.cost_price_entry.get())
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Tanggal dan waktu saat ini

        product_data = (current_datetime, product, price, quantity, cost_price)
        valid = self.observer.notify(product_data)
        print(valid)
        if not valid:
            return
        # Ganti mode file ke "w" untuk menulis ulang seluruh isi file dengan data baru
        with open(self.file_handler.inventory_file, "w", newline="") as file:
            writer = csv.writer(file)

            # Tambahkan data barang baru di awal
            writer.writerow(product_data)

            # Tulis ulang data barang yang sudah ada
            for item in self.inventory_tree.get_children():
                values = self.inventory_tree.item(item, "values")
                writer.writerow(values)

        messagebox.showinfo("Info", "Produk berhasil ditambahkan.")

        # Perbarui tampilan tabel stok barang
        self.inventory_tree.delete(*self.inventory_tree.get_children())
        self.inventory_window.destroy()
        self.show_inventory()

    def update_product(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Silakan pilih barang yang ingin diperbarui.")
            return
        
        self.update_product_window = tk.Toplevel(self.inventory_window)
        self.update_product_window.title("Perbarui Barang")
        
        selected_product_data = self.inventory_tree.item(selected_item, "values")

        self.product_name_label = tk.Label(self.update_product_window, text="Nama Barang:")
        self.product_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.product_name_entry = tk.Entry(self.update_product_window)
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.product_name_entry.insert(0, selected_product_data[1])  # Mengisi entry dengan nama barang yang dipilih
        
        self.price_label = tk.Label(self.update_product_window, text="Harga:")
        self.price_label.grid(row=1, column=0, padx=5, pady=5)
        self.price_entry = tk.Entry(self.update_product_window)
        self.price_entry.grid(row=1, column=1, padx=5, pady=5)
        self.price_entry.insert(0, selected_product_data[2])  # Mengisi entry dengan harga barang yang dipilih
        
        self.quantity_label = tk.Label(self.update_product_window, text="Jumlah:")
        self.quantity_label.grid(row=2, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(self.update_product_window)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        self.quantity_entry.insert(0, selected_product_data[3])  # Mengisi entry dengan jumlah barang yang dipilih
        
        self.cost_price_label = tk.Label(self.update_product_window, text="Harga Modal:")
        self.cost_price_label.grid(row=3, column=0, padx=5, pady=5)
        self.cost_price_entry = tk.Entry(self.update_product_window)
        self.cost_price_entry.grid(row=3, column=1, padx=5, pady=5)
        self.cost_price_entry.insert(0, selected_product_data[4])  # Mengisi entry dengan harga modal barang yang dipilih
        
        self.submit_update_btn = tk.Button(self.update_product_window, text="Simpan", command=lambda: self.save_updated_product(selected_item))
        self.submit_update_btn.grid(row=4, columnspan=2, padx=5, pady=5)

    def save_updated_product(self, selected_item):
        product = self.product_name_entry.get()
        price = int(self.price_entry.get())
        quantity = int(self.quantity_entry.get())
        cost_price = int(self.cost_price_entry.get())
        
        updated_product_data = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), product, price, quantity, cost_price)
        
        updated_inventory = []
        with open(self.file_handler.inventory_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if tuple(row) != tuple(self.inventory_tree.item(selected_item, "values")):
                    updated_inventory.append(row)
                else:
                    updated_inventory.append(updated_product_data)
        
        with open(self.file_handler.inventory_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_inventory)
        
        messagebox.showinfo("Info", "Barang berhasil diperbarui.")
        
        self.inventory_tree.delete(*self.inventory_tree.get_children())
        self.inventory_window.destroy()
        self.show_inventory()


    def sell_product_with_payment_type(self, payment_type):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Silakan pilih item yang ingin dijual.")
            return

        index = self.inventory_tree.index(selected_item)
        product_data = self.inventory_tree.item(selected_item, "values")

        if int(product_data[3]) <= 0:
            messagebox.showerror("Error", "Stok barang habis.")
            return

        transaction = TransactionFactory.create_transaction(payment_type, product_data[2])
        
        total_payment = transaction.calculate_total()

        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Tanggal dan waktu saat ini

        updated_inventory = []
        with open(self.file_handler.inventory_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if tuple(row) != tuple(product_data):
                    updated_inventory.append(row)
                else:
                    updated_inventory.append((row[0], row[1], row[2], int(row[3]) - 1, row[4]))

        with open(self.file_handler.inventory_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_inventory)

        # Tambahkan item terjual ke riwayat transaksi
        with open(self.file_handler.transactions_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow((current_datetime, product_data[1], total_payment, 1, product_data[4], current_datetime))  # Menambahkan transaksi dengan waktu penjualan

        messagebox.showinfo("Info", f"Produk {product_data[1]} berhasil dijual.\nTotal Pembayaran: {total_payment}")

        self.inventory_tree.delete(*self.inventory_tree.get_children())
        self.inventory_window.destroy()
        self.show_inventory()


    def delete_product(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Silakan pilih barang yang ingin dihapus.")
            return
        
        confirmation = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus barang ini?")
        if confirmation:
            selected_product_data = self.inventory_tree.item(selected_item, "values")
            
            updated_inventory = []
            with open(self.file_handler.inventory_file, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if tuple(row) != tuple(selected_product_data):
                        updated_inventory.append(row)
            
            with open(self.file_handler.inventory_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(updated_inventory)
            
            messagebox.showinfo("Info", "Barang berhasil dihapus.")
            
            self.inventory_tree.delete(selected_item)
            self.inventory_window.destroy()
            self.show_inventory()

    def show_transactions(self):
        self.transactions_window = tk.Tk()
        self.transactions_window.title("Riwayat Transaksi")
        
        self.transactions_tree = ttk.Treeview(self.transactions_window, columns=("Waktu Produk Masuk", "Nama Barang","Harga", "Jumlah", "Modal", "Waktu Penjualan"))
        self.transactions_tree.heading("#0", text="No.")
        self.transactions_tree.heading("#1", text="Waktu Produk Masuk")
        self.transactions_tree.heading("#2", text="Nama Barang")
        self.transactions_tree.heading("#3", text="Harga")
        self.transactions_tree.heading("#4", text="Jumlah")
        self.transactions_tree.heading("#5", text="Modal")
        self.transactions_tree.heading("#6", text="Waktu Penjualan")
        
        transactions_data = self.load_transactions()
        for i, item in enumerate(transactions_data, start=1):
            self.transactions_tree.insert("", "end", text=str(i), values=item)
        
        self.transactions_tree.pack(pady=10)

        # Menambahkan frame untuk date picker dan tombol filter
        filter_frame = tk.Frame(self.transactions_window)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Dari:").pack(side="left")
        self.start_date_entry = DateEntry(filter_frame, date_pattern="yyyy-mm-dd")
        self.start_date_entry.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Sampai:").pack(side="left")
        self.end_date_entry = DateEntry(filter_frame, date_pattern="yyyy-mm-dd")
        self.end_date_entry.pack(side="left", padx=5)

        filter_btn = ttk.Button(filter_frame, text="Filter", command=self.apply_date_filter)
        filter_btn.pack(side="left", padx=5)

        self.calculate_sales_summary_btn = tk.Button(self.transactions_window, text="Hitung Rekapan Penjualan", command=self.calculate_sales_summary)
        self.calculate_sales_summary_btn.pack(pady=5)

    def apply_date_filter(self):
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()

        filtered_transactions = []
        with open(self.file_handler.transactions_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 6:
                    transaction_date = datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S").date()
                    if start_date <= transaction_date <= end_date:
                        filtered_transactions.append(row)

        for i in self.transactions_tree.get_children():
            self.transactions_tree.delete(i)

        for i, item in enumerate(filtered_transactions, start=1):
            self.transactions_tree.insert("", "end", text=str(i), values=item)

    def load_transactions(self):
        transactions_data = []
        with open(self.file_handler.transactions_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                transactions_data.append(row)
        return transactions_data
    
    def calculate_sales_summary(self):
        total_sales = 0
        total_cost = 0
        
        if not os.path.exists(self.file_handler.transactions_file):
            messagebox.showinfo("Info", "Belum ada transaksi yang dicatat.")
            return
        
        with open(self.file_handler.transactions_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                total_sales += int(row[2])
                total_cost += int(row[4])
        
        total_profit = total_sales - total_cost
        
        messagebox.showinfo("Info", f"Total Penjualan: Rp {total_sales}\nTotal Laba Bersih: Rp {total_profit}")

def main():
    app = SalesApp()
    app.inventory_window.mainloop()

if __name__ == "__main__":
    main()
