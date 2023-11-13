import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Класс для представления сотрудника
class Employee:
    def __init__(self, name, phone, email, salary):
        self.name = name
        self.phone = phone
        self.email = email
        self.salary = salary

    def get_name(self):
        return self.name

    def get_phone(self):
        return self.phone

    def get_email(self):
        return self.email

    def get_salary(self):
        return self.salary

    def set_name(self, name):
        self.name = name

    def set_phone(self, phone):
        self.phone = phone

    def set_email(self, email):
        self.email = email

    def set_salary(self, salary):
        self.salary = salary

# Функция для создания таблицы сотрудников в БД
def create_employee_table():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (name TEXT, phone TEXT, email TEXT, salary REAL)''')
    conn.commit()
    conn.close()

# Функция для добавления нового сотрудника в БД
def add_employee(employee):
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute("INSERT INTO employees VALUES (?, ?, ?, ?)",
              (employee.get_name(), employee.get_phone(), employee.get_email(), employee.get_salary()))
    conn.commit()
    conn.close()

# Функция для изменения существующего сотрудника в БД
def update_employee(employee):
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute("UPDATE employees SET phone = ?, email = ?, salary = ? WHERE name = ?",
              (employee.get_phone(), employee.get_email(), employee.get_salary(), employee.get_name()))
    conn.commit()
    conn.close()

# Функция для удаления сотрудника из БД
def delete_employee(name):
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute("DELETE FROM employees WHERE name = ?", (name,))
    conn.commit()
    conn.close()

# Функция для поиска сотрудника по ФИО в БД
def search_employee(name):
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees WHERE name LIKE ?", ('%' + name + '%',))
    result = c.fetchall()
    conn.close()
    return result

# Функция для обновления данных в виджете Treeview
def update_treeview(tree, employees):
    tree.delete(*tree.get_children())
    for employee in employees:
        tree.insert('', 'end', values=(employee[0], employee[1], employee[2], employee[3]))

# Функция для обработки события добавления сотрудника
def add_employee_handler():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()

    if name and phone and email and salary:
        employee = Employee(name, phone, email, salary)
        add_employee(employee)
        employees = search_employee('')
        update_treeview(treeview, employees)
        clear_entries()
        messagebox.showinfo('Success', 'Employee added successfully.')
    else:
        messagebox.showerror('Error', 'Please enter all details.')

# Функция для обработки события изменения сотрудника
def update_employee_handler():
    selected_item = treeview.focus()
    if selected_item:
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        salary = salary_entry.get()

        if name and phone and email and salary:
            employee = Employee(name, phone, email, salary)
            update_employee(employee)
            employees = search_employee('')
            update_treeview(treeview, employees)
            clear_entries()
            messagebox.showinfo('Success', 'Employee updated successfully.')
        else:
            messagebox.showerror('Error', 'Please enter all details.')
    else:
        messagebox.showerror('Error', 'No employee selected.')

# Функция для обработки события удаления сотрудника
def delete_employee_handler():
    selected_item = treeview.focus()
    if selected_item:
        name = treeview.item(selected_item)['values'][0]
        delete_employee(name)
        employees = search_employee('')
        update_treeview(treeview, employees)
        clear_entries()
        messagebox.showinfo('Success', 'Employee deleted successfully.')
    else:
        messagebox.showerror('Error', 'No employee selected.')

# Функция для обработки события поиска сотрудника
def search_employee_handler():
    name = search_entry.get()
    employees = search_employee(name)
    update_treeview(treeview, employees)

# Функция для очистки полей ввода
def clear_entries():
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)
    salary_entry.delete(0, END)

# Создание окна приложения
root = Tk()

# Создание виджета Treeview для отображения данных
treeview = ttk.Treeview(root)
treeview['columns'] = ('Name', 'Phone', 'Email', 'Salary')
treeview.heading('#0', text='ID')
treeview.column('#0', width=50)
treeview.heading('Name', text='Name')
treeview.column('Name', width=150)
treeview.heading('Phone', text='Phone')
treeview.column('Phone', width=100)
treeview.heading('Email', text='Email')
treeview.column('Email', width=200)
treeview.heading('Salary', text='Salary')
treeview.column('Salary', width=100)
treeview.pack()

# Создание полей ввода
name_label = Label(root, text='Name:')
name_label.pack()
name_entry = Entry(root)
name_entry.pack()

phone_label = Label(root, text='Phone:')
phone_label.pack()
phone_entry = Entry(root)
phone_entry.pack()

email_label = Label(root, text='Email:')
email_label.pack()
email_entry = Entry(root)
email_entry.pack()

salary_label = Label(root, text='Salary:')
salary_label.pack()
salary_entry = Entry(root)
salary_entry.pack()

# Создание кнопок для выполнения операций
add_button = Button(root, text='Add', command=add_employee_handler)
add_button.pack()

# Функция для обновления информации о сотруднике в полях ввода
def refresh_employee_info():
    selected_item = treeview.focus()
    if selected_item:
        name = treeview.item(selected_item)['values'][0]
        phone = treeview.item(selected_item)['values'][1]
        email = treeview.item(selected_item)['values'][2]
        salary = treeview.item(selected_item)['values'][3]

        name_entry.delete(0, END)
        name_entry.insert(0, name)

        phone_entry.delete(0, END)
        phone_entry.insert(0, phone)

        email_entry.delete(0, END)
        email_entry.insert(0, email)

        salary_entry.delete(0, END)
        salary_entry.insert(0, salary)

# Создание кнопки для обновления информации
refresh_button = Button(root, text='Refresh Info', command=refresh_employee_info)
refresh_button.pack()

update_button = Button(root, text='Update', command=update_employee_handler)
update_button.pack()

delete_button = Button(root, text='Delete', command=delete_employee_handler)
delete_button.pack()

search_label = Label(root, text='Search:')
search_label.pack()
search_entry = Entry(root)
search_entry.pack()

search_button = Button(root, text='Search', command=search_employee_handler)
search_button.pack()

# Создание таблицы сотрудников в БД (если она еще не создана)
create_employee_table()

# Получение всех сотрудников из БД и отображение их в виджете Treeview
employees = search_employee('')
update_treeview(treeview, employees)

# Запуск главного цикла приложения
root.mainloop()