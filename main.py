import tkinter as tk
from tkinter import messagebox, filedialog
import json

def merge_sort(data):
    if len(data) <= 1:
        return data

    # Split the data into two halves
    mid = len(data) // 2
    left_half = data[:mid]
    right_half = data[mid:]

    # Recursively sort both halves
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    return merge(left_half, right_half)

def merge(left, right):
    result = []
    left_idx, right_idx = 0, 0

    while left_idx < len(left) and right_idx < len(right):
        left_isbn = int(left[left_idx]["ISBN"])
        right_isbn = int(right[right_idx]["ISBN"])

        if left_isbn < right_isbn:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1

    result.extend(left[left_idx:])
    result.extend(right[right_idx:])
    return result

def load_entries_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                book_list.clear()
                book_list.extend(data)
                view_library()
                messagebox.showinfo("Book Management System", "Entries loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading entries: {str(e)}")

def save_entries_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, "w") as file:
            json.dump(book_list, file)
        messagebox.showinfo("Book Management System", "Entries saved successfully.")

def add_book():
    global book_list
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    year = year_entry.get().strip()
    isbn = isbn_entry.get().strip()

    if title and author and year and isbn:
        book_list.append({"ISBN": isbn, "Title": title, "Author": author, "Year": year})
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        isbn_entry.delete(0, tk.END)
        view_library()
        messagebox.showinfo("Book Management System", "Book added successfully.")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def delete_book():
    index = delete_entry.get().strip()
    if index.isdigit() and 1 <= int(index) <= len(book_list):
        del book_list[int(index) - 1]
        view_library()
        delete_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Invalid index.")

def view_library():
    global book_list
    library_window = tk.Toplevel(root)
    library_window.title("Current Books")
    library_window.geometry("500x500")
    books_info = tk.Text(library_window)

    if not book_list:
        books_info.insert(tk.END, "The library is empty")
    else:
        book_list = merge_sort(book_list)  # Sort the book list by ISBN
        for index, book in enumerate(book_list, start=1):
            books_info.insert(tk.END, f"{index}. ISBN: {book['ISBN']}\n    Title: {book['Title']}\n    Author: {book['Author']}\n    Year: {book['Year']}\n\n")

    books_info.pack()

def exit_library():
    root.destroy()

if __name__ == "__main__":
    book_list = []
    root = tk.Tk()
    root.title("Book Management System")
    root.configure(bg="#f0f0f0")
    root.geometry("500x500")

    custom_font = ("Arial", 12)

    isbn_label = tk.Label(root, text="ISBN:", font=custom_font, bg="#f0f0f0")
    isbn_label.pack(pady=10)

    isbn_entry = tk.Entry(root, font=custom_font)
    isbn_entry.pack(pady=5)

    title_label = tk.Label(root, text="Book Title:", font=custom_font, bg="#f0f0f0")
    title_label.pack(pady=10)

    title_entry = tk.Entry(root, font=custom_font)
    title_entry.pack(pady=5)

    author_label = tk.Label(root, text="Author Name:", font=custom_font, bg="#f0f0f0")
    author_label.pack(pady=10)

    author_entry = tk.Entry(root, font=custom_font)
    author_entry.pack(pady=5)

    year_label = tk.Label(root, text="Publication Year:", font=custom_font, bg="#f0f0f0")
    year_label.pack(pady=10)

    year_entry = tk.Entry(root, font=custom_font)
    year_entry.pack(pady=5)

    add_button = tk.Button(root, text="Add Book", font=custom_font, bg="#4CAF50", fg="white", command=add_book)
    add_button.pack(pady=10)

    view_button = tk.Button(root, text="View Library", font=custom_font, bg="#008CBA", fg="white", command=view_library)
    view_button.pack(pady=5)

    delete_label = tk.Label(root, text="Enter index to delete:", font=custom_font, bg="#f0f0f0")
    delete_label.pack(pady=10)

    delete_entry = tk.Entry(root, font=custom_font)
    delete_entry.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Book", font=custom_font, bg="#f44336", fg="white", command=delete_book)
    delete_button.pack(pady=10)

    load_button = tk.Button(root, text="Load Entries from File", font=custom_font, bg="#009688", fg="white", command=load_entries_from_file)
    load_button.pack(pady=5)

    save_button = tk.Button(root, text="Save Entries to File", font=custom_font, bg="#555", fg="white", command=save_entries_to_file)
    save_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", font=custom_font, bg="#555", fg="white", command=exit_library)
    exit_button.pack(pady=10)

    root.mainloop()
