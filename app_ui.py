import customtkinter as ctk

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

    
        self.back_btn = ctk.CTkButton(
            self.stocks_frame, 
            text="← Back to Dashboard", 
            fg_color="#444444", 
            hover_color="#333333",
            command=self.show_dashboard_page
        )

        self.back_btn.pack(pady=10, padx=20, anchor="nw")

        self.show_dashboard_page()


    def show_dashboard_page(self):

        self.stocks_frame.pack_forget() 
        self.dashboard_frame.pack(fill="both", expand=True)

    def show_stocks_page(self):

        self.dashboard_frame.pack_forget()
        self.stocks_frame.pack(fill="both", expand=True)

if __name__ == "__main__" :
    app = InventoryApp()
    app.mainloop()
