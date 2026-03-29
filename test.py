import database_management as db

print("connecttion check")
db.connect_db()

print("add check")
db.add_item("Milk 1L", 60.0, 20)
db.add_item("Chocolate", 20.0, 50)
db.add_item("Biscuit", 10.0, 100)

print("fetching ..")
items = db.fetch_all()
for item in items:
    print(item)

print("search check")
search_results = db.search_items("Cho")
print(search_results)

print("\n--- Testing Update (ID 1: Chocolate to 75 qty) ---")
db.update_items(1, "Chocolate", 20.0, 75)

# 6. Final check
print("\n--- Final Table View ---")
final_items = db.fetch_all()
for i in final_items:
    print(i)