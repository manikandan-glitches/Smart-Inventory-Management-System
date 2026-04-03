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

        self.back_btn = ctk.CTkButton(self.stocks_frame, text="← Back to Dashboard", fg_color="#444444", hover_color="#333333",
                                      command=self.show_dashboard_page)

        self.back_btn.pack(pady=20, padx=20, anchor="nw")

        # Search Frame (To keep Entry and Button together)
        search_container = ctk.CTkFrame(self.stocks_frame, fg_color="transparent")
        search_container.pack(pady=20, padx=20, fill="x")

        self.search_input = ctk.CTkEntry(
            search_container, 
            placeholder_text="Search by product name...",
            width=600,
            height=40,
            corner_radius=20, # Rounded look
            border_width=2,
            border_color="#3B8ED0" # Blue border
        )
        self.search_input.pack(side="left", padx=(150, 10), expand=True, anchor="e")

        self.search_btn = ctk.CTkButton(
            search_container,
            text="🔍 Search",
            width=100,
            height=40,
            corner_radius=20,
            command=self.search_data,
            fg_color="#3B8ED0",
            hover_color="#2B6DAE"
        )
        self.search_btn.pack(side="left", padx=(0, 150), expand=True, anchor="w")

        column=('id','name','price','qty')
        self.tree=ttk.Treeview(self.stocks_frame, columns=column, show="headings", height=30)

        self.tree.heading("id", text="Item ID")
        self.tree.heading("name", text="Product Name")
        self.tree.heading("qty", text="Quantity")
        self.tree.heading("price", text="Price (₹)")

        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=250, anchor="w")
        self.tree.column("qty", width=100, anchor="center")
        self.tree.column("price", width=100, anchor="center")

        self.tree.pack(pady=20, padx=20 ,fill="both")

        self.btn_group = ctk.CTkFrame(self.stocks_frame, fg_color="transparent")
        self.btn_group.pack(pady=10)

        self.add_btn = ctk.CTkButton(self.btn_group, text="ADD ITEM", 
                                       fg_color="#FF0101", hover_color="#695957",
                                       command=self.show_Add_page
                                       )
        self.add_btn.grid(row=0,column=0,padx=10)

        self.edit_btn = ctk.CTkButton(self.btn_group, text="EDIT", 
                                       fg_color="#029115", hover_color="#695957",
                                       command=self.prepare_edit
                                       )
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Button-1>", self.handle_click)


        self.del_btn = ctk.CTkButton(self.btn_group, text="DELETE ITEM", 
                                       fg_color="#4313F0", hover_color="#695957",
                                       command=self.delete_item
                                       )
        self.del_btn.grid(row=0,column=2,padx=10)
        self.update_stock()

        # --- 3. add frame ---

        self.add_frame=ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(self.add_frame, text="Add New Product", font=("Arial", 24, "bold")).pack(pady=30)
        
        self.back_btn = ctk.CTkButton(self.add_frame, text="← Back to Dashboard", fg_color="#444444", hover_color="#333333",
                                      command=self.show_stocks_page)

        self.back_btn.pack(pady=10, padx=20, anchor="nw")


        self.name_input = ctk.CTkEntry(self.add_frame, placeholder_text="Enter Product Name", width=300)
        self.name_input.pack(pady=10)

        self.price_input = ctk.CTkEntry(self.add_frame, placeholder_text="Enter Price (₹)", width=300)
        self.price_input.pack(pady=10)

        self.qty_input = ctk.CTkEntry(self.add_frame, placeholder_text="Enter Quantity", width=300)
        self.qty_input.pack(pady=10)

        self.save_btn = ctk.CTkButton(self.add_frame, text="Submit Item", fg_color="#2ecc71",
                                      command=self.submit_data_logic)
        self.save_btn.pack(pady=20)

        self.cancel_btn = ctk.CTkButton(self.add_frame, text="Cancel", fg_color="#e74c3c", 
                                        command=self.show_stocks_page)
        self.cancel_btn.pack(pady=5)

        self.show_dashboard_page()

    def prepare_edit(self):
        id=self.tree.selection()
        self.name_input.delete(0,"end")
        self.price_input.delete(0,"end")
        self.qty_input.delete(0,"end")

        info=self.tree.item(id)
        self.current_id=info['values'][0]
        self.name_input.insert(0,info['values'][1])
        self.price_input.insert(0,info['values'][2])
        self.qty_input.insert(0,info['values'][3])
        self.show_Add_page()

    def search_data(self):

        text=self.search_input.get().strip()
        if not text:
            self.update_stock()
        else:
            for item in self.tree.get_children():
                self.tree.delete(item)

            data = db.search_items(text)
            for row in data:
                self.tree.insert("","end",values=row)




    def update_stock(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        data = db.fetch_all()
        for row in data:
            self.tree.insert("","end",values=row)

    def submit_data_logic(self):
        name = self.name_input.get()
        price_str = self.price_input.get()
        qty_str = self.qty_input.get()

        price = float(price_str)
        qty = int(qty_str)

        if self.current_id:
            db.update_items(self.current_id,name,price,qty)
            self.current_id=None
            self.update_stock()
        else:
            db.add_item(name,price,qty)
            self.update_stock()

        self.name_input.delete(0, 'end')
        self.price_input.delete(0, 'end')
        self.qty_input.delete(0, 'end')

    def on_tree_select(self,event):
        selected = self.tree.selection()
        if selected:
            self.edit_btn.grid(row=0, column=1, padx=10)
        else:
            self.edit_btn.grid_forget()

    def handle_click(self,event):
        item=self.tree.identify_row(event.y)

        if not item:
            self.tree.selection_remove(self.tree.selection())
            self.edit_btn.grid_forget()

    def delete_item(self):
        id =self.tree.selection()
        if id:
            info=self.tree.item(id)
            real_id=info['values'][0]
            db.delete_item(real_id)
            self.update_stock()
        
        


    def show_dashboard_page(self):

        self.stocks_frame.pack_forget()
        self.add_frame.pack_forget() 
        self.dashboard_frame.pack(fill="both", expand=True)

    def show_stocks_page(self):

        self.dashboard_frame.pack_forget()
        self.add_frame.pack_forget() 
        self.stocks_frame.pack(fill="both", expand=True)

    def show_Add_page(self):

        self.dashboard_frame.pack_forget()
        self.stocks_frame.pack_forget() 
        self.add_frame.pack(fill="both", expand=True)

if __name__ == "__main__" :
    app = InventoryApp()
    app.mainloop()
