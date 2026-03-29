import customtkinter as ctk
from tkinter import ttk
import database_management as db

class InventoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Inventory Manager')
        self.geometry("900x600")

        self.dashboard_frame = ctk.CTkFrame(self,fg_color="transparent")

        self.db_label = ctk.CTkLabel(self.dashboard_frame, text="Shop Dashboard", font=("Arial", 32, "bold"))
        self.db_label.pack(pady=(150, 20))

        self.to_stocks_btn = ctk.CTkButton(self.dashboard_frame, text="Manage Stocks", 
                                           command=self.show_stocks_page, width=200, height=50)
        self.to_stocks_btn.pack(pady=20)


        # --- 2. STOCKS PAGE
        self.stocks_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.st_label = ctk.CTkLabel(
            self.stocks_frame, 
            text="Inventory Management System", 
            font=("Arial", 26, "bold")
        )
        self.st_label.pack(pady=20)

        column=('id','name','price','qty')
        self.tree=ttk.Treeview(self.stocks_frame, columns=column, show="headings", height=15)

        self.tree.heading("id", text="Item ID")
        self.tree.heading("name", text="Product Name")
        self.tree.heading("qty", text="Quantity")
        self.tree.heading("price", text="Price (₹)")

        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=250, anchor="w")
        self.tree.column("qty", width=100, anchor="center")
        self.tree.column("price", width=100, anchor="center")

        self.tree.pack(pady=20, padx=20 ,fill="both")
    
        self.back_btn = ctk.CTkButton(
            self.stocks_frame, 
            text="← Back to Dashboard", 
            fg_color="#444444", 
            hover_color="#333333",
            command=self.show_dashboard_page
        )

        self.back_btn.pack(pady=10, padx=20, anchor="nw")

        self.update_stock()

        self.show_dashboard_page()

    def update_stock(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        data = db.fetch_all()
        for row in data:
            self.tree.insert("","end",values=row)
        


    def show_dashboard_page(self):

        self.stocks_frame.pack_forget() 
        self.dashboard_frame.pack(fill="both", expand=True)

    def show_stocks_page(self):

        self.dashboard_frame.pack_forget()
        self.stocks_frame.pack(fill="both", expand=True)

if __name__ == "__main__" :
    app = InventoryApp()
    app.mainloop()
