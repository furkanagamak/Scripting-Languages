## 
## MESSAGE FOR GRADING TAs:
## As my bonus task for Part 4, I implemented the "Task Editing" functionality for my To-Do List App. If you select an incomplete task
## from the list and click on the "Edit Task" button, it will allow you to modify the properties of the selected task. Once you are done
## editing, you can click on "Update Task" and finalize the edit. You will be able to see the task change in the task list.
##

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

class MyToDoListApplication:
    def __init__(self, todolist_app_main_window):
        self.todolist_app_main_window = todolist_app_main_window
        self.todolist_app_main_window.title("To-Do List App")
        
        self.tasks = []
        self.completed_tasks = []
        
        self.todolist_app_create_widgets()
        
    def todolist_app_create_widgets(self):
        app_widgets_style = ttk.Style()
        app_widgets_style.configure('TFrame', background='white')
        app_widgets_style.configure('TLabel', background='white', font=('Helvetica', 10))
        app_widgets_style.configure('TEntry', font=('Helvetica', 10))
        app_widgets_style.configure('TButton', font=('Helvetica', 10))
        app_widgets_style.configure('TCheckbutton', background='white')
        app_widgets_style.configure('TRadiobutton', background='white')

        todolist_app_main_header = tk.Label(self.todolist_app_main_window, text="To-Do List App", font=('Helvetica', 16))
        todolist_app_main_header.pack(pady=20)

        todolist_app_main_input_frame = tk.Frame(self.todolist_app_main_window, pady=5)
        todolist_app_main_input_frame.pack(pady=10, fill='x', expand=True)
        todolist_app_main_input_frame.columnconfigure(1, weight=1)

        tk.Label(todolist_app_main_input_frame, text="Task:").grid(row=0, column=0, sticky='w', padx=10)
        self.task_entry = tk.Entry(todolist_app_main_input_frame, font=('Helvetica', 10))
        self.task_entry.grid(row=0, column=1, sticky='we', padx=10)

        tk.Label(todolist_app_main_input_frame, text="Priority:").grid(row=1, column=0, sticky='w', padx=10)
        self.todolist_app_priority_variable = tk.StringVar()
        self.todolist_app_priority_dropdown = ttk.Combobox(todolist_app_main_input_frame, textvariable=self.todolist_app_priority_variable, state="readonly", font=('Helvetica', 10))
        self.todolist_app_priority_dropdown['values'] = ('Low', 'Medium', 'High')
        self.todolist_app_priority_dropdown.grid(row=1, column=1, sticky='we', padx=10)
        self.todolist_app_priority_dropdown.current(0)

        tk.Label(todolist_app_main_input_frame, text="Due Date:").grid(row=2, column=0, sticky='w', padx=10)
        self.calendar = Calendar(todolist_app_main_input_frame, selectmode='day', date_pattern='dd/mm/yyyy', font=('Helvetica', 10))
        self.calendar.grid(row=2, column=1, sticky='we', padx=10)

        todolist_app_main_add_button = tk.Button(todolist_app_main_input_frame, text="Add Task", font=('Helvetica', 10), command=self.todolist_app_add_task)
        todolist_app_main_add_button.grid(row=3, column=0, columnspan=2, sticky='we', padx=10, pady=10)
        
        todolist_app_list_frame = tk.Frame(self.todolist_app_main_window)
        todolist_app_list_frame.pack(pady=10, fill='both', expand=True)
        
        self.task_listbox = tk.Listbox(todolist_app_list_frame, height=8, width = 50, activestyle = "none")
        self.task_listbox.pack(side='left', fill='both', expand=True)
        
        self.completed_listbox = tk.Listbox(todolist_app_list_frame, height=8, width = 50, activestyle = "none")
        self.completed_listbox.pack(side='right', fill='both', expand=True)
        
        todolist_app_main_button_frame = tk.Frame(self.todolist_app_main_window)
        todolist_app_main_button_frame.pack(pady=10, fill='x', expand=True)
        
        todolist_app_main_mark_complete_button = tk.Button(todolist_app_main_button_frame, text="Mark Complete", command=self.todolist_app_mark_complete, width = 50)
        todolist_app_main_mark_complete_button.pack(side='left', fill='x', expand=True)
        
        todolist_app_main_remove_completed_button = tk.Button(todolist_app_main_button_frame, text="Remove Completed", command=self.todolist_app_remove_completed, width = 50)
        todolist_app_main_remove_completed_button.pack(side='right', fill='x', expand=True)

        todolist_app_main_edit_button = tk.Button(todolist_app_main_button_frame, text="Edit Task", command=self.todolist_app_edit_task, width=50)
        todolist_app_main_edit_button.pack(side='left', fill='x', expand=True, padx=5)

    ## For Part 4 Bonus Task:
    def todolist_app_edit_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            return
        self.todolist_app_new_edit_window = tk.Toplevel(self.todolist_app_main_window)
        self.todolist_app_new_edit_window.title("Edit Task")
        self.todolist_app_new_edit_window.geometry("400x300")

        current_task_to_be_edited = self.tasks[selected_index[0]].split(" - ")
        task_name, priority, due_date = current_task_to_be_edited[0], current_task_to_be_edited[1].split(": ")[1], current_task_to_be_edited[2].split(": ")[1]

        due_date_day, due_date_month, due_date_year = map(int, due_date.split("/"))

        tk.Label(self.todolist_app_new_edit_window, text="Task:").grid(row=0, column=0)
        self.edit_task_entry = tk.Entry(self.todolist_app_new_edit_window)
        self.edit_task_entry.grid(row=0, column=1)
        self.edit_task_entry.insert(0, task_name)

        tk.Label(self.todolist_app_new_edit_window, text="Priority:").grid(row=1, column=0)
        self.todolist_app_edit_priority_variable = tk.StringVar(value=priority)
        self.todolist_app_edit_priority_dropdown = ttk.Combobox(self.todolist_app_new_edit_window, textvariable=self.todolist_app_edit_priority_variable, state="readonly")
        self.todolist_app_edit_priority_dropdown['values'] = ('Low', 'Medium', 'High')
        self.todolist_app_edit_priority_dropdown.grid(row=1, column=1)

        tk.Label(self.todolist_app_new_edit_window, text="Due Date:").grid(row=2, column=0)
        self.edit_calendar = Calendar(self.todolist_app_new_edit_window, selectmode='day', year=due_date_year, month=due_date_month, day=due_date_day, date_pattern='dd/mm/yyyy')
        self.edit_calendar.grid(row=2, column=1)

        update_button = tk.Button(self.todolist_app_new_edit_window, text="Update Task", command=lambda: self.todolist_app_update_task(selected_index[0]))
        update_button.grid(row=3, column=0, columnspan=2, sticky='ew')

    ## For Part 4 Bonus Task:
    def todolist_app_update_task(self, index):
        updated_list_task_name = self.edit_task_entry.get()
        updated_list_task_priority = self.todolist_app_edit_priority_variable.get()
        updated_list_task_date = self.edit_calendar.get_date()

        updated_task_info = f"{updated_list_task_name} - Priority: {updated_list_task_priority} - Due Date: {updated_list_task_date}"
        self.tasks[index] = updated_task_info
        self.task_listbox.delete(index)
        self.task_listbox.insert(index, updated_task_info)

        self.todolist_app_new_edit_window.destroy()

    def todolist_app_add_task(self):
        list_task_name = self.task_entry.get().strip()
        if not list_task_name:
            return
        list_task_name = self.task_entry.get()
        list_task_priority = self.todolist_app_priority_variable.get()
        list_task_date = self.calendar.get_date()
        
        list_task_info = f"{list_task_name} - Priority: {list_task_priority} - Due Date: {list_task_date}"
        self.tasks.append(list_task_info)
        
        self.task_listbox.insert('end', list_task_info)
        
        self.task_entry.delete(0, 'end')
        
    def todolist_app_mark_complete(self):
        selected_indices = self.task_listbox.curselection()
        for i in selected_indices:
            task = self.task_listbox.get(i)
            self.completed_tasks.append(task)
            self.completed_listbox.insert('end', task)
            
        for i in reversed(selected_indices):
            del self.tasks[i]
            self.task_listbox.delete(i)
        
    def todolist_app_remove_completed(self):
        selected_indices = self.completed_listbox.curselection()
        for i in reversed(selected_indices):
            self.completed_listbox.delete(i)

todolist_app_main_window = tk.Tk()
app = MyToDoListApplication(todolist_app_main_window)

todolist_app_main_window.mainloop()
