import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, PhotoImage, ttk

conn = sqlite3.connect("carsharing.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS cars")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        first_name TEXT,
        last_name TEXT,
        password TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        manufacturer TEXT,
        category TEXT,
        description TEXT,
        engine_specs TEXT,
        price TEXT
    )
''')
conn.commit()

random_users = [
    ("ivanpetrov", "Иван", "Петров", "pass123"),
    ("mariasmirnova", "Мария", "Смирнова", "qwerty"),
    ("alekseiivanov", "Алексей", "Иванов", "abc123"),
    ("olgakuznetsova", "Ольга", "Кузнецова", "password"),
    ("dmitriysokolov", "Дмитрий", "Соколов", "123456"),
    ("elenorolova", "Елена", "Орлова", "letmein"),
    ("sergeymorozov", "Сергей", "Морозов", "welcome"),
    ("annavasilieva", "Анна", "Васильева", "monkey"),
    ("pavelzaytsev", "Павел", "Зайцев", "sunshine"),
    ("tatyana", "Татьяна", "Павлова", "123qwe"),
    ("nikolayvolkov", "Николай", "Волков", "iloveyou"),
    ("svetlanalebedeva", "Светлана", "Лебедева", "admin"),
    ("vladimirkozlov", "Владимир", "Козлов", "pass1"),
    ("yuliamedvedeva", "Юлия", "Медведева", "000000"),
    ("grigoriyfrolov", "Григорий", "Фролов", "123abc"),
    ("viktoria", "Виктория", "Герасимова", "superman"),
    ("maksimanisimov", "Максим", "Анисимов", "batman"),
    ("daryaegorova", "Дарья", "Егорова", "trustno1"),
    ("artemfedorov", "Артем", "Федоров", "123321"),
    ("kseniyatikhonova", "Ксения", "Тихонова", "654321")
]
for user in random_users:
    try:
        cursor.execute("INSERT INTO users (username, first_name, last_name, password) VALUES (?, ?, ?, ?)", user)
        conn.commit()
    except sqlite3.IntegrityError:
        pass


default_cars = [
    (
        "Lada Largus",
        "Lada (АвтоВАЗ)",
        "Эконом",
        "Компактный MPV, ориентированный на функциональность и надежность. Идеален для семейного использования.",
        "1.6L бензин",
        "Около $10,000"
    ),
    (
        "Renault Kaptur",
        "Renault",
        "Эконом/Кроссовер",
        "Стильный субкомпактный кроссовер, сочетающий современный дизайн с практичностью.",
        "1.0L турбо",
        "Около $15,000"
    ),
    (
        "Volkswagen Polo Sedan",
        "Volkswagen",
        "Эконом",
        "Компактный седан, предлагающий сбалансированную производительность и стиль в комфортном исполнении.",
        "1.6L двигатель",
        "Около $18,000"
    ),
    (
        "Hyundai Solaris",
        "Hyundai",
        "Эконом",
        "Современный компактный седан, известный экономичностью и доступностью, с обновленным дизайном.",
        "Опции 1.4L - 1.6L",
        "Около $12,000"
    )
]
for car in default_cars:
    try:
        cursor.execute("INSERT INTO cars (name, manufacturer, category, description, engine_specs, price) VALUES (?, ?, ?, ?, ?, ?)", car)
        conn.commit()
    except sqlite3.IntegrityError:
        pass

def open_car_selection():
    car_window = tk.Toplevel(root)
    car_window.title("Выбор автомобиля")
    car_window.geometry('900x500')
    
    exit_button = tk.Button(car_window, text="Выйти", command=car_window.destroy)
    exit_button.pack(anchor="ne", padx=10, pady=10)
    
    tab_control = ttk.Notebook(car_window)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='Эконом')
    tab_control.add(tab2, text='Медиум')
    tab_control.add(tab3, text='Бизнес')

    car_frame = tk.Frame(tab1)
    car_frame.pack(pady=20)
    
    cursor.execute("SELECT name, manufacturer, description, engine_specs, price FROM cars WHERE category = ?", ("Эконом",))
    cars = cursor.fetchall()
    if cars:
        for car in cars:
            info = f"Название: {car[0]}\nПроизводитель: {car[1]}\nОписание: {car[2]}\nДвигатель: {car[3]}\nЦена: {car[4]}"
            tk.Button(car_frame, text=car[0], font=("", 12), width=30,
                      command=lambda info=info: messagebox.showinfo("Информация об автомобиле", info)).pack(pady=5)
    else:
        tk.Label(car_frame, text="Автомобили категории 'Эконом' отсутствуют.", font=("", 12)).pack(pady=20)

    tk.Label(tab2, text="Скоро появятся автомобили категории 'Медиум'.", font=("", 12)).pack(pady=20)
    tk.Label(tab3, text="Скоро появятся автомобили категории 'Бизнес'.", font=("", 12)).pack(pady=20)
    
    tab_control.pack(expand=1, fill='both')

def open_registration_window():
    reg_window = tk.Toplevel(root)
    reg_window.title("Регистрация")
    reg_window.geometry("300x350")
    
    frame = tk.Frame(reg_window)
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    tk.Label(frame, text="Логин:").pack(anchor="w")
    entry_username_reg = tk.Entry(frame, width=25)
    entry_username_reg.pack(pady=2)
    
    tk.Label(frame, text="Имя:").pack(anchor="w")
    entry_first_name = tk.Entry(frame, width=25)
    entry_first_name.pack(pady=2)
    
    tk.Label(frame, text="Фамилия:").pack(anchor="w")
    entry_last_name = tk.Entry(frame, width=25)
    entry_last_name.pack(pady=2)
    
    tk.Label(frame, text="Пароль:").pack(anchor="w")
    entry_new_password = tk.Entry(frame, show="*", width=25)
    entry_new_password.pack(pady=2)
    
    tk.Label(frame, text="Подтвердите пароль:").pack(anchor="w")
    entry_confirm_password = tk.Entry(frame, show="*", width=25)
    entry_confirm_password.pack(pady=2)
    
    def register_user():
        username = entry_username_reg.get().strip()
        first_name = entry_first_name.get().strip()
        last_name = entry_last_name.get().strip()
        password = entry_new_password.get()
        confirm_password = entry_confirm_password.get()
        
        if not username or not first_name or not last_name:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
            return
        
        try:
            cursor.execute("INSERT INTO users (username, first_name, last_name, password) VALUES (?, ?, ?, ?)",
                           (username, first_name, last_name, password))
            conn.commit()
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            reg_window.destroy()
            open_car_selection()
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует!")
    
    tk.Button(frame, text="Зарегистрироваться", command=register_user, width=25).pack(pady=10)

def user_login():
    username = entry_username.get().strip()
    password = entry_password.get()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        messagebox.showinfo("Успех", f"Добро пожаловать, {user[2]} {user[3]}!")
        open_car_selection()
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль.")

def developer_login():
    username = entry_username.get().strip()
    password = entry_password.get()
    # Разрешенные разработчики по логину
    allowed_developers = ["Карапиря", "Усманов", "Некрылов"]
    if username in allowed_developers and password == "123":
        messagebox.showinfo("Успех", "Вход для разработчика выполнен успешно!")
        show_users_db()
    else:
        messagebox.showerror("Ошибка", "Неверные учетные данные разработчика!")

def show_users_db():
    users_window = tk.Toplevel(root)
    users_window.title("База данных пользователей")
    users_window.state('zoomed')
    
    exit_button = tk.Button(users_window, text="Выйти", command=users_window.destroy)
    exit_button.pack(anchor="ne", padx=10, pady=10)
    
    tree = ttk.Treeview(users_window, columns=("ID", "Логин", "Имя", "Фамилия", "Пароль"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Логин", text="Логин")
    tree.heading("Имя", text="Имя")
    tree.heading("Фамилия", text="Фамилия")
    tree.heading("Пароль", text="Пароль")
    tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    def refresh_tree():
        for item in tree.get_children():
            tree.delete(item)
        cursor.execute("SELECT id, username, first_name, last_name, password FROM users")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
    
    refresh_tree()
    
    deletion_frame = tk.Frame(users_window)
    deletion_frame.pack(pady=10)
    tk.Label(deletion_frame, text="Введите ID для удаления:").pack(side=tk.LEFT)
    entry_delete = tk.Entry(deletion_frame)
    entry_delete.pack(side=tk.LEFT, padx=5)
    
    def delete_user():
        id_to_delete = entry_delete.get().strip()
        if not id_to_delete:
            messagebox.showerror("Ошибка", "Введите ID пользователя для удаления!")
            return
        cursor.execute("SELECT * FROM users WHERE id = ?", (id_to_delete,))
        user = cursor.fetchone()
        if not user:
            messagebox.showerror("Ошибка", "Пользователь не найден!")
            return
        if messagebox.askyesno("Подтверждение", f"Вы действительно хотите удалить пользователя с ID {id_to_delete}?"):
            cursor.execute("DELETE FROM users WHERE id = ?", (id_to_delete,))
            conn.commit()
            messagebox.showinfo("Успех", f"Пользователь с ID {id_to_delete} удален!")
            refresh_tree()
    
    tk.Button(deletion_frame, text="Удалить", command=delete_user).pack(side=tk.LEFT, padx=5)
    
    tk.Button(users_window, text="Управление данными автомобилей", command=manage_cars, width=25).pack(pady=10)

def manage_cars():
    cars_window = tk.Toplevel(root)
    cars_window.title("Управление автомобилями")
    cars_window.state('zoomed')
    
    exit_button = tk.Button(cars_window, text="Выйти", command=cars_window.destroy)
    exit_button.pack(anchor="ne", padx=10, pady=10)
    
    tree = ttk.Treeview(cars_window, columns=("ID", "Название", "Производитель", "Категория", "Описание", "Характеристики двигателя", "Цена"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Название", text="Название")
    tree.heading("Производитель", text="Производитель")
    tree.heading("Категория", text="Категория")
    tree.heading("Описание", text="Описание")
    tree.heading("Характеристики двигателя", text="Характеристики двигателя")
    tree.heading("Цена", text="Цена")
    tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    def refresh_car_tree():
        for item in tree.get_children():
            tree.delete(item)
        cursor.execute("SELECT id, name, manufacturer, category, description, engine_specs, price FROM cars")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
    
    refresh_car_tree()
    
    add_frame = tk.Frame(cars_window)
    add_frame.pack(pady=10)
    
    tk.Label(add_frame, text="Название:").grid(row=0, column=0, padx=5, pady=2)
    entry_car_name = tk.Entry(add_frame)
    entry_car_name.grid(row=0, column=1, padx=5, pady=2)
    
    tk.Label(add_frame, text="Производитель:").grid(row=1, column=0, padx=5, pady=2)
    entry_manufacturer = tk.Entry(add_frame)
    entry_manufacturer.grid(row=1, column=1, padx=5, pady=2)
    
    tk.Label(add_frame, text="Категория:").grid(row=2, column=0, padx=5, pady=2)
    entry_category = tk.Entry(add_frame)
    entry_category.grid(row=2, column=1, padx=5, pady=2)
    
    tk.Label(add_frame, text="Описание:").grid(row=3, column=0, padx=5, pady=2)
    entry_description = tk.Entry(add_frame, width=50)
    entry_description.grid(row=3, column=1, padx=5, pady=2)
    
    tk.Label(add_frame, text="Характеристики двигателя:").grid(row=4, column=0, padx=5, pady=2)
    entry_engine = tk.Entry(add_frame)
    entry_engine.grid(row=4, column=1, padx=5, pady=2)
    
    tk.Label(add_frame, text="Цена:").grid(row=5, column=0, padx=5, pady=2)
    entry_price = tk.Entry(add_frame)
    entry_price.grid(row=5, column=1, padx=5, pady=2)
    
    def add_car():
        name = entry_car_name.get().strip()
        manufacturer = entry_manufacturer.get().strip()
        category = entry_category.get().strip()
        description = entry_description.get().strip()
        engine = entry_engine.get().strip()
        price = entry_price.get().strip()
        if not name or not manufacturer:
            messagebox.showerror("Ошибка", "Введите хотя бы название автомобиля и производителя!")
            return
        try:
            cursor.execute("INSERT INTO cars (name, manufacturer, category, description, engine_specs, price) VALUES (?, ?, ?, ?, ?, ?)",
                           (name, manufacturer, category, description, engine, price))
            conn.commit()
            messagebox.showinfo("Успех", "Автомобиль успешно добавлен!")
            refresh_car_tree()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении автомобиля: {e}")
    
    tk.Button(add_frame, text="Добавить автомобиль", command=add_car, width=20).grid(row=6, column=0, columnspan=2, pady=10)

    def delete_car():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите автомобиль для удаления!")
            return
        car_id = tree.item(selected)['values'][0]
        if messagebox.askyesno("Подтверждение", f"Вы действительно хотите удалить автомобиль с ID {car_id}?"):
            cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
            conn.commit()
            messagebox.showinfo("Успех", "Автомобиль успешно удален!")
            refresh_car_tree()
    
    tk.Button(cars_window, text="Удалить выбранный автомобиль", command=delete_car, width=25).pack(pady=10)

root = tk.Tk()
root.title("Каршеринг")
root.geometry("300x400")
root.configure(bg="white")

if os.path.exists("logo.png"):
    logo_image = PhotoImage(file="logo.png")
    logo_label = tk.Label(root, image=logo_image, bg="white")
    logo_label.pack(pady=5)

discount_label = tk.Label(root, text="Скидка на первый заказ\n550.00", fg="black", bg="yellow", font=("Arial", 10, "bold"))
discount_label.pack(pady=5)

main_frame = tk.Frame(root, bg="white")
main_frame.pack(expand=True, pady=5)

tk.Label(main_frame, text="Логин:", bg="white").pack(anchor="w")
entry_username = tk.Entry(main_frame, width=20)
entry_username.pack(pady=2)

tk.Label(main_frame, text="Пароль:", bg="white").pack(anchor="w")
entry_password = tk.Entry(main_frame, show="*", width=20)
entry_password.pack(pady=2)

tk.Button(main_frame, text="Регистрация", command=open_registration_window, width=25).pack(pady=5)
tk.Button(main_frame, text="Вход", command=user_login, width=25).pack(pady=5)
tk.Button(main_frame, text="Разработчик", command=developer_login, width=25).pack(pady=5)
tk.Button(main_frame, text="Заказ", command=lambda: messagebox.showinfo("Заказ", "В разработке......."), width=25).pack(pady=5)

root.mainloop()
conn.close()
