from tkinter import messagebox
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
            result = observer.update(data)
        return result
class InventoryObserver(Observer):
    def update(self, data):
        product = data[1]
        price = data[2]
        quantity = data[3]
        
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
            return CashTransaction(TransactionDecorator(transaction_data))
        elif payment_type == "kartu kredit":
            return CreditCardTransaction(TransactionDecorator(transaction_data))
        else:
            raise ValueError("Jenis pembayaran tidak valid.")

class TransactionDecorator:
    def __init__(self, transaction):
        self._transaction = transaction
    
    def calculate_total(self):
        return int(self._transaction)

class CashTransaction(TransactionDecorator):
    def __init__(self, cash):
        self._cash = cash
    def calculate_total(self):
        return str(self._cash.calculate_total())
     

class CreditCardTransaction(TransactionDecorator):
    def __init__(self, credit):
        self._credit = credit
    def calculate_total(self):
        return str(self._credit.calculate_total() - 5000)
