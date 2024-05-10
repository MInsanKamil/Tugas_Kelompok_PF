import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import csv
import os

class SingletonFileHandler:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.inventory_file = "inventory.csv"
        self.transactions_file = "transactions.csv"

class Observer:
    def __init__(self):
        self.observers = []
    
    def register(self, observer):
        self.observers.append(observer)
    
    def notify(self, data):
        for observer in self.observers:
            observer.update(data)
            
class InventoryObserver(Observer):
    def update(self, data):
        product = data[0]
        price = data[1]
        quantity = data[2]
        
        if not product:
            messagebox.showerror("Error", "Nama barang tidak boleh kosong.")
            return False
        if price <= 0:
            messagebox.showerror("Error", "Harga harus lebih dari 0.")
            return False
        if quantity <= 0:
            messagebox.showerror("Error", "Jumlah harus lebih dari 0.")
            return False
        
        return True

class TransactionFactory:
    @staticmethod
    def create_transaction(payment_type, transaction_data):
        if payment_type == "tunai":
            return CashTransaction(transaction_data)
        elif payment_type == "kartu kredit":
            return CreditCardTransaction(transaction_data)
        else:
            raise ValueError("Jenis pembayaran tidak valid.")

class TransactionDecorator:
    def __init__(self, transaction):
        self.transaction = transaction
    
    def calculate_total(self):
        pass

class CashTransaction(TransactionDecorator):
    def calculate_total(self):
        total = self.transaction
        return total

class CreditCardTransaction(TransactionDecorator):
    def calculate_total(self):
        total = self.transaction
        return str(int(total) - 5000)

class SalesApp:
    def __init__(self):
        # self.root = tk.Tk()
        
        self.file_handler = SingletonFileHandler()
        self.observer = Observer()
        self.observer.register(InventoryObserver())
        
        self.show_inventory()
        
    def create_widgets(self):
        self.label = tk.Label(self.root, text="Selamat Datang di Aplikasi Manajemen Penjualan")
        self.label.pack(pady=10)
        
        self.manage_inventory_btn = tk.Button(self.root, text="Kelola Stok Barang", command=self.show_inventory)
        self.manage_inventory_btn.pack(pady=5)
        
    def show_inventory(self):
        self.inventory_window = tk.Tk()
        self.inventory_window.title("Kelola Stok Barang")
        
        self.inventory_tree = ttk.Treeview(self.inventory_window, columns=("Nama Barang", "Harga", "Jumlah", "Modal"))
        self.inventory_tree.heading("#0", text="No.")
        self.inventory_tree.heading("#1", text="Nama Barang")
        self.inventory_tree.heading("#2", text="Harga")
        self.inventory_tree.heading("#3", text="Jumlah")
        self.inventory_tree.heading("#4", text="Modal")
        
        inventory_data = self.load_inventory()
        for i, item in enumerate(inventory_data, start=1):
            self.inventory_tree.insert("", "end", text=str(i), values=item)
        
        self.inventory_tree.pack(pady=10)
        
        self.add_product_btn = tk.Button(self.inventory_window, text="Tambah Barang", command=self.add_product)
        self.add_product_btn.pack(pady=5)

        self.update_product_btn = tk.Button(self.inventory_window, text="Update Barang", command=self.update_product)
        self.update_product_btn.pack(pady=5)

        self.delete_product_btn = tk.Button(self.inventory_window, text="Hapus Barang", command=self.delete_product)
        self.delete_product_btn.pack(pady=5)

        self.sell_cash_product_btn = tk.Button(self.inventory_window, text="Jual Barang (Tunai)", command=lambda: self.sell_product_with_payment_type("tunai"))
        self.sell_cash_product_btn.pack(pady=5)
        
        self.sell_credit_product_btn = tk.Button(self.inventory_window, text="Jual Barang (Kartu Kredit)", command=lambda: self.sell_product_with_payment_type("kartu kredit"))
        self.sell_credit_product_btn.pack(pady=5)
        
        self.view_transactions_btn = tk.Button(self.inventory_window, text="Lihat Riwayat Transaksi", command=self.show_transactions)
        self.view_transactions_btn.pack(pady=5)


    def load_inventory(self):
        inventory_data = []
        with open(self.file_handler.inventory_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                inventory_data.append(row)
        return inventory_data

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
        # print(product, price, quantity, cost_price)
        
        product_data = (product, price, quantity, cost_price)
        
        # valid = self.observer.notify(product_data)
        # if not valid:
        #     return
        
        # Buka file inventory.csv dengan mode "a" untuk menambahkan data baru
        # with open(self.file_handler.inventory_file, "a", newline="") as file:
        #     writer = csv.writer(file)
        #     writer.writerow(product_data)
        
        # Ganti mode file ke "w" untuk menulis ulang seluruh isi file dengan data baru
        with open(self.file_handler.inventory_file, "w", newline="") as file:
            writer = csv.writer(file)
            
            # Tulis ulang data barang yang sudah ada
            for item in self.inventory_tree.get_children():
                values = self.inventory_tree.item(item, "values")
                writer.writerow(values)
            
            # Tambahkan data barang baru
            writer.writerow(product_data)
        
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
        self.product_name_entry.insert(0, selected_product_data[0])  # Mengisi entry dengan nama barang yang dipilih
        
        self.price_label = tk.Label(self.update_product_window, text="Harga:")
        self.price_label.grid(row=1, column=0, padx=5, pady=5)
        self.price_entry = tk.Entry(self.update_product_window)
        self.price_entry.grid(row=1, column=1, padx=5, pady=5)
        self.price_entry.insert(0, selected_product_data[1])  # Mengisi entry dengan harga barang yang dipilih
        
        self.quantity_label = tk.Label(self.update_product_window, text="Jumlah:")
        self.quantity_label.grid(row=2, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(self.update_product_window)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        self.quantity_entry.insert(0, selected_product_data[2])  # Mengisi entry dengan jumlah barang yang dipilih
        
        self.cost_price_label = tk.Label(self.update_product_window, text="Harga Modal:")
        self.cost_price_label.grid(row=3, column=0, padx=5, pady=5)
        self.cost_price_entry = tk.Entry(self.update_product_window)
        self.cost_price_entry.grid(row=3, column=1, padx=5, pady=5)
        self.cost_price_entry.insert(0, selected_product_data[3])  # Mengisi entry dengan harga modal barang yang dipilih
        
        self.submit_update_btn = tk.Button(self.update_product_window, text="Simpan", command=self.save_updated_product)
        self.submit_update_btn.grid(row=4, columnspan=2, padx=5, pady=5)

    def save_updated_product(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Silakan pilih barang yang ingin diperbarui.")
            return
        
        product = self.product_name_entry.get()
        price = int(self.price_entry.get())
        quantity = int(self.quantity_entry.get())
        cost_price = int(self.cost_price_entry.get())
        
        updated_product_data = (product, price, quantity, cost_price)
        
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

    def sell_product(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Silakan pilih item yang ingin dijual.")
            return
        
        index = self.inventory_tree.index(selected_item)
        product_data = self.inventory_tree.item(selected_item, "values")
        
        if int(product_data[2]) <= 0:
            messagebox.showerror("Error", "Stok barang habis.")
            return
        
        # Update data stok barang
        updated_inventory = []
        with open(self.file_handler.inventory_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if tuple(row) != tuple(product_data):
                    updated_inventory.append(row)
                else:
                    updated_inventory.append((row[0], row[1], int(row[2]) - 1, row[3]))
        
        with open(self.file_handler.inventory_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_inventory)
        
        # Tambahkan item terjual ke riwayat transaksi
        with open(self.file_handler.transactions_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow((product_data[0], product_data[1], 1, product_data[3]))  # Menambahkan transaksi dengan jumlah 1
        
        messagebox.showinfo("Info", f"Produk {product_data[0]} berhasil dijual.")
        
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
        
        if int(product_data[2]) <= 0:
            messagebox.showerror("Error", "Stok barang habis.")
            return
        
        # Create transaction based on payment type
        transaction = TransactionFactory.create_transaction(payment_type, product_data[1])
        # Calculate total payment  # Data for the transaction
        total_payment = transaction.calculate_total()
        # Update data stok barang
        updated_inventory = []
        with open(self.file_handler.inventory_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if tuple(row) != tuple(product_data):
                    updated_inventory.append(row)
                else:
                    updated_inventory.append((row[0], row[1], int(row[2]) - 1, row[3]))
        
        with open(self.file_handler.inventory_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_inventory)
        
        # Tambahkan item terjual ke riwayat transaksi
        with open(self.file_handler.transactions_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow((product_data[0], total_payment, 1, product_data[3]))  # Menambahkan transaksi dengan jumlah 1
        
        messagebox.showinfo("Info", f"Produk {product_data[0]} berhasil dijual.\nTotal Pembayaran: {total_payment}")
        
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
        
        self.transactions_tree = ttk.Treeview(self.transactions_window, columns=("Nama Barang", "Harga", "Jumlah", "Modal"))
        self.transactions_tree.heading("#0", text="No.")
        self.transactions_tree.heading("#1", text="Nama Barang")
        self.transactions_tree.heading("#2", text="Harga")
        self.transactions_tree.heading("#3", text="Jumlah")
        self.transactions_tree.heading("#4", text="Modal")
        
        transactions_data = self.load_transactions()
        for i, item in enumerate(transactions_data, start=1):
            self.transactions_tree.insert("", "end", text=str(i), values=item)
        
        self.transactions_tree.pack(pady=10)

        self.calculate_sales_summary_btn = tk.Button(self.transactions_window, text="Hitung Rekapan Penjualan", command=self.calculate_sales_summary)
        self.calculate_sales_summary_btn.pack(pady=5)

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
                total_sales += int(row[1])
                total_cost += int(row[3])
        
        total_profit = total_sales - total_cost
        
        messagebox.showinfo("Info", f"Total Penjualan: Rp {total_sales}\nTotal Laba Bersih: Rp {total_profit}")

def main():
    app = SalesApp()
    app.inventory_window.mainloop()

if __name__ == "__main__":
    main()
