import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

QUOTES_FILE = "quotes.json"
HISTORY_FILE = "history.json"


class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("650x700")

        # Загрузка данных
        self.quotes = self.load_data(QUOTES_FILE, self.get_default_quotes())
        self.history = self.load_data(HISTORY_FILE, [])

        self.setup_ui()
        self.update_history_listbox()
        self.update_filters()

    def get_default_quotes(self):
        return [
            {
                "text": "Программирование — это искусство рассказывать другому человеку то, что ты хочешь, чтобы сделал компьютер.",
                "author": "Дональд Кнут", "theme": "IT"},
            {"text": "Делай, что можешь, с тем, что имеешь, там, где ты есть.", "author": "Теодор Рузвельт",
             "theme": "Мотивация"},
            {"text": "Единственный способ делать великие дела — любить то, что вы делаете.", "author": "Стив Джобс",
             "theme": "Работа"},
            {"text": "Ошибки — это доказательство того, что вы пытаетесь.", "author": "Неизвестный",
             "theme": "Мотивация"},
            {"text": "Работает? Не трогай!", "author": "Народная мудрость", "theme": "IT"}
        ]

    def load_data(self, filename, default_data):
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return default_data
        return default_data

    def save_data(self, filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def setup_ui(self):
        # --- Блок отображения цитаты ---
        self.quote_label = tk.Label(self.root, text="Нажмите кнопку, чтобы сгенерировать цитату", wraplength=600,
                                    font=("Arial", 14, "italic"), height=4)
        self.quote_label.pack(pady=20)

        self.author_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.author_label.pack()

        # --- Фильтры ---
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0, padx=5)
        self.author_var = tk.StringVar(value="Все")
        self.author_cb = ttk.Combobox(filter_frame, textvariable=self.author_var, state="readonly")
        self.author_cb.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Фильтр по теме:").grid(row=0, column=2, padx=5)
        self.theme_var = tk.StringVar(value="Все")
        self.theme_cb = ttk.Combobox(filter_frame, textvariable=self.theme_var, state="readonly")
        self.theme_cb.grid(row=0, column=3, padx=5)

        # Кнопка генерации
        tk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote, bg="#4CAF50", fg="white",
                  font=("Arial", 12)).pack(pady=10)

        # --- История ---
        tk.Label(self.root, text="История сгенерированных цитат:", font=("Arial", 10, "bold")).pack(pady=5)
        self.history_listbox = tk.Listbox(self.root, width=90, height=10)
        self.history_listbox.pack()

        # --- Добавление новой цитаты ---
        add_frame = tk.LabelFrame(self.root, text="Добавить новую цитату", padx=10, pady=10)
        add_frame.pack(pady=20, fill="x", padx=20)

        tk.Label(add_frame, text="Текст:").grid(row=0, column=0, sticky="w")
        self.new_text_entry = tk.Entry(add_frame, width=60)
        self.new_text_entry.grid(row=0, column=1, pady=2)

        tk.Label(add_frame, text="Автор:").grid(row=1, column=0, sticky="w")
        self.new_author_entry = tk.Entry(add_frame, width=60)
        self.new_author_entry.grid(row=1, column=1, pady=2)

        tk.Label(add_frame, text="Тема:").grid(row=2, column=0, sticky="w")
        self.new_theme_entry = tk.Entry(add_frame, width=60)
        self.new_theme_entry.grid(row=2, column=1, pady=2)

        tk.Button(add_frame, text="Добавить", command=self.add_quote).grid(row=3, column=0, columnspan=2, pady=10)

    def update_filters(self):
        authors = ["Все"] + sorted(list(set(q["author"] for q in self.quotes)))
        themes = ["Все"] + sorted(list(set(q["theme"] for q in self.quotes)))

        self.author_cb['values'] = authors
        self.theme_cb['values'] = themes

    def generate_quote(self):
        selected_author = self.author_var.get()
        selected_theme = self.theme_var.get()

        filtered_quotes = [q for q in self.quotes
                           if (selected_author == "Все" or q["author"] == selected_author)
                           and (selected_theme == "Все" or q["theme"] == selected_theme)]

        if not filtered_quotes:
            messagebox.showinfo("Пусто", "По выбранным фильтрам нет цитат.")
            return

        quote = random.choice(filtered_quotes)
        self.quote_label.config(text=f'"{quote["text"]}"')
        self.author_label.config(text=f'- {quote["author"]} [{quote["theme"]}]')

        # Обновление истории
        self.history.append(quote)
        self.save_data(HISTORY_FILE, self.history)
        self.update_history_listbox()

    def update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for q in reversed(self.history):
            self.history_listbox.insert(tk.END, f'{q["text"]} — {q["author"]}')

    def add_quote(self):
        text = self.new_text_entry.get().strip()
        author = self.new_author_entry.get().strip()
        theme = self.new_theme_entry.get().strip()

        # 6. Проверка корректности ввода (пустые строки)
        if not text or not author or not theme:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        new_quote = {"text": text, "author": author, "theme": theme}
        self.quotes.append(new_quote)
        self.save_data(QUOTES_FILE, self.quotes)

        self.update_filters()
        self.new_text_entry.delete(0, tk.END)
        self.new_author_entry.delete(0, tk.END)
        self.new_theme_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Цитата успешно добавлена!")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
