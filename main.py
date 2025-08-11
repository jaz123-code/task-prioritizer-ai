import datetime
import tkinter as tk
from tkinter import messagebox
import json
import threading
import openai

class Task:
    def __init__(self, name, deadline, importance, urgency, estimated_time,status="pending", created_at=None):
        self.name = name
        self.deadline = deadline
        self.importance = importance
        self.urgency = urgency
        self.estimated_time = estimated_time
        self.status = status
        self.created_at = created_at or datetime.datetime.now()

    def to_dict(self):
        return {
            "name": self.name,
            "deadline": self.deadline,
            "importance": self.importance,
            "urgency": self.urgency,
            "estimated_time": self.estimated_time,
            "status": self.status,
            "created_at": str(self.created_at)
        }

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, task_num):
        if 0 <= task_num < len(self.tasks):
            del self.tasks[task_num]
            return True
        return False
    def task_view(self, task_num):
        if 0 <= task_num < len(self.tasks):
            task = self.tasks[task_num]
            return f"Task {task_num + 1}: {task.to_dict()}"
        return "Invalid task number"

    def save_tasks_to_json(self, filename="tasks.json"):
        with open(filename, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)
    
    def get_tasks(self):
        return self.tasks
    def load_tasks_from_json(self, filename="tasks.json"):
        try:
            with open(filename, "r") as f:
                task_dicts = json.load(f)
                self.tasks = [Task(**task_dict) for task_dict in task_dicts]
        except FileNotFoundError:
            self.tasks = []
    def status_complete(self):
        updated = False
        for task in self.tasks:
            if task.status == "pending":
                task.status = "completed"
                updated = True
        return updated
    def deadline1(self):
        res = datetime.datetime.now()
        if not self.tasks:
            print("No tasks available.")
            return
        for idx, task in enumerate(self.tasks):
            try:
                task_deadline = datetime.datetime.strptime(task.deadline, "%Y-%m-%d")
                if task_deadline < res:
                    print(f"Task {idx+1} ({task.name}): Overdue")
                else:
                    print(f"Task {idx+1} ({task.name}): Deadline is {task.deadline}")
            except Exception:
                   print(f"task {idx+1}: Invalid deadline format")
    def priority(self, task):
       
        if task.status != "pending":
            return float('-inf') 
        importance = int(task.importance)
        urgency = int(task.urgency)
        
        return importance * 2 + urgency





        
        


    def show_delete_task_gui(self):
        def on_delete():
            try:
                idx = int(entry.get()) - 1
                if self.delete_task(idx):
                    messagebox.showinfo("Success", "Task deleted successfully")
                    window.destroy()
                else:
                    messagebox.showerror("Error", "Invalid task number")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")

        window = tk.Tk()
        window.title("Delete Task")
        tk.Label(window, text="Enter task number to delete:").pack()
        entry = tk.Entry(window)
        entry.pack()
        tk.Button(window, text="Delete", command=on_delete).pack()
        window.mainloop()
    def show_task_gui(self):
        def on_display():
            try:
                idx = int(entry.get()) - 1
                task_info = self.task_view(idx)
                if "Invalid task number" not in task_info:
                    messagebox.showinfo("Task Info", task_info)
                else:
                    messagebox.showerror("Error", "Invalid task number")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")

        window = tk.Tk()
        window.title("View Task")
        tk.Label(window, text="Enter task number to view:").pack()
        entry = tk.Entry(window)
        entry.pack()
        tk.Button(window, text="Show Task", command=on_display).pack()
        window.mainloop()
    def deadline_score(self,task):
        try:
            task_deadline = datetime.datetime.strptime(task.deadline, "%Y-%m-%d")
            curr= datetime.datetime.now()
            if task_deadline<curr:
                return -1
            else:
                return task_deadline -curr
        except ValueError:
            print(f"invalid deadline format for task {task.name}")


    
def main():
    gui = tk.Tk()

    logo_text = """
     ___      _    _______        _     _______        _             
    / _ \    / \  |__   __|      | |   |__   __|      | |            
   | | | |  / _ \    | | ___  ___| |_     | | ___  ___| |_ ___  _ __ 
   | |_| | / ___ \   | |/ _ \/ __| __|    | |/ _ \/ __| __/ _ \| '__|
    \___/ /_/   \_\  |_|\___/\___|\__|    |_|\___/\___|\__\___/|_|   
                                                                     
    RAT TASKS
    """

    
    rat_frames = [
        r" (\_/) ",
        r" (o.o) ",
        r" / >🐭 ",
        r" (\_/) ",
        r" (O.o) ",
        r" / >🐭 ",
    ]

    rat_canvas = tk.Canvas(gui, width=350, height=40, bg="white", highlightthickness=0)
    rat_canvas.pack(pady=(0, 10))
    rat_text = rat_canvas.create_text(10, 20, anchor="w", font=("Courier", 18), text=rat_frames[0])

    def animate_rat(frame=0, x=10):
        rat_canvas.coords(rat_text, x, 20)
        rat_canvas.itemconfig(rat_text, text=rat_frames[frame % len(rat_frames)])
        if x < 270:
            gui.after(80, animate_rat, frame+1, x+10)
        else:
            gui.after(500, animate_rat, 0, 10)

    animate_rat()
    logo_label = tk.Label(gui, text=logo_text, font=("Courier", 10, "bold"), fg="#2e86c1", justify="left")
    logo_label.pack(pady=(10, 0))
    welcome = tk.Toplevel(gui)
    welcome.title("Welcome")
    welcome.geometry("400x200")
    welcome_label = tk.Label(welcome, text="Welcome to AI Task Prioritizer!", font=("Arial", 18))
    welcome_label.pack(expand=True)

    def animate_text(text, label, idx=0):
        if idx <= len(text):
            label.config(text=text[:idx])
            welcome.after(30, animate_text, text, label, idx+1)
        else:
            
            welcome.after(1000, welcome.destroy)

    animate_text("Welcome to AI Task Prioritizer!", welcome_label)
    gui.withdraw()
    def show_main():
        gui.deiconify()
    welcome.protocol("WM_DELETE_WINDOW", show_main)
    welcome.after(1600, show_main)
    gui.title("AI Task Prioritizer by jazz")

    manager = TaskManager()
    manager.load_tasks_from_json("tasks.json")

    def refresh_task_list():
        task_list.delete(0, tk.END)
        for idx, task in enumerate(manager.get_tasks()):
            status = f"[{task.status}]"
            task_list.insert(tk.END, f"{idx+1}. {task.name} {status} (Deadline: {task.deadline})")

    def add_task_gui():
        add_win = tk.Toplevel(gui)
        add_win.title("Add Task")

        tk.Label(add_win, text="Task Name:").grid(row=0, column=0)
        name_entry = tk.Entry(add_win)
        name_entry.grid(row=0, column=1)

        tk.Label(add_win, text="Deadline (YYYY-MM-DD):").grid(row=1, column=0)
        deadline_entry = tk.Entry(add_win)
        deadline_entry.grid(row=1, column=1)

        tk.Label(add_win, text="Importance (1-10):").grid(row=2, column=0)
        importance_entry = tk.Entry(add_win)
        importance_entry.grid(row=2, column=1)

        tk.Label(add_win, text="Urgency (1-10):").grid(row=3, column=0)
        urgency_entry = tk.Entry(add_win)
        urgency_entry.grid(row=3, column=1)

        tk.Label(add_win, text="Estimated Time (min):").grid(row=4, column=0)
        time_entry = tk.Entry(add_win)
        time_entry.grid(row=4, column=1)

        def submit_task():
            name = name_entry.get()
            deadline = deadline_entry.get()
            try:
                importance = int(importance_entry.get())
                urgency = int(urgency_entry.get())
                estimated_time = int(time_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Importance, Urgency, and Estimated Time must be numbers.")
                return
            if not name.isalpha():
                messagebox.showerror("Error", "Task name must be alphabetic.")
                return
            try:
                datetime.datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Deadline must be in YYYY-MM-DD format.")
                return
            if not (1 <= importance <= 10 and 1 <= urgency <= 10):
                messagebox.showerror("Error", "Importance and Urgency must be between 1 and 10.")
                return
            task = Task(name, deadline, importance, urgency, estimated_time)
            manager.add_task(task)
            manager.save_tasks_to_json("tasks.json")
            refresh_task_list()
            add_win.destroy()

        tk.Button(add_win, text="Add", command=submit_task).grid(row=5, column=0, columnspan=2, pady=10)

    def delete_task_gui():
        del_win = tk.Toplevel(gui)
        del_win.title("Delete Task")
        tk.Label(del_win, text="Enter task number to delete:").pack()
        del_entry = tk.Entry(del_win)
        del_entry.pack()

        def delete_task():
            try:
                idx = int(del_entry.get()) - 1
                if manager.delete_task(idx):
                    manager.save_tasks_to_json("tasks.json")
                    refresh_task_list()
                    messagebox.showinfo("Success", "Task deleted successfully")
                    del_win.destroy()
                else:
                    messagebox.showerror("Error", "Invalid task number")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")

        tk.Button(del_win, text="Delete", command=delete_task).pack(pady=5)

    def mark_all_completed():
        if manager.status_complete():
            manager.save_tasks_to_json("tasks.json")
            refresh_task_list()
            messagebox.showinfo("Success", "All pending tasks marked as completed.")
        else:
            messagebox.showinfo("Info", "No pending tasks to update.")

    def show_task_details():
        try:
            idx = int(task_num_entry.get()) - 1
            task_info = manager.task_view(idx)
            if "Invalid task number" not in task_info:
                messagebox.showinfo("Task Info", task_info)
            else:
                messagebox.showerror("Error", "Invalid task number")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def show_deadlines():
        lines = []
        now = datetime.datetime.now()
        for idx, task in enumerate(manager.get_tasks()):
            try:
                task_deadline = datetime.datetime.strptime(task.deadline, "%Y-%m-%d")
                if task_deadline < now:
                    lines.append(f"Task {idx+1} ({task.name}): Overdue")
                else:
                    lines.append(f"Task {idx+1} ({task.name}): Deadline is {task.deadline}")
            except Exception:
                lines.append(f"Task {idx+1}: Invalid deadline format")
        messagebox.showinfo("Deadlines", "\n".join(lines))

    def show_deadline_scores():
        lines = []
        for task in manager.get_tasks():
            score = manager.deadline_score(task)
            lines.append(f"Task: {task.name}, Deadline Score: {score}")
        messagebox.showinfo("Deadline Scores", "\n".join(lines))

    frame = tk.Frame(gui)
    frame.pack(padx=10, pady=10)

    task_list = tk.Listbox(frame, width=60)
    task_list.pack()

    refresh_task_list()

    btn_frame = tk.Frame(gui)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add Task", command=add_task_gui).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Delete Task", command=delete_task_gui).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Mark All Completed", command=mark_all_completed).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Show Deadlines", command=show_deadlines).grid(row=0, column=3, padx=5)
    tk.Button(btn_frame, text="Show Deadline Scores", command=show_deadline_scores).grid(row=0, column=4, padx=5)

    detail_frame = tk.Frame(gui)
    detail_frame.pack(pady=10)
    tk.Label(detail_frame, text="Enter task number for details:").pack(side=tk.LEFT)
    task_num_entry = tk.Entry(detail_frame, width=5)
    task_num_entry.pack(side=tk.LEFT, padx=5)
    tk.Button(detail_frame, text="Show Details", command=show_task_details).pack(side=tk.LEFT)

    def show_ai_helper():
        ai_win = tk.Toplevel(gui)
        ai_win.title("AI Task Assistant")
        tk.Label(ai_win, text="Ask AI for help with your tasks:").pack()
        ai_entry = tk.Entry(ai_win, width=50)
        ai_entry.pack(pady=5)
        response_box = tk.Text(ai_win, width=60, height=10, wrap="word")
        response_box.pack(pady=5)

        def ask_ai():
            question = ai_entry.get()
            if not question.strip():
                messagebox.showerror("Error", "Please enter a question.")
                return

            response_box.delete("1.0", tk.END)
            response_box.insert(tk.END, "Thinking...")

            def get_ai_response():
                try:
                    import os
                    api_key = os.environ.get("OPENAI_API_KEY")
                    if not api_key:
                        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
                    openai.api_key = api_key
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant for a task management app."},
                            {"role": "user", "content": question}
                        ]
                    )
                    answer = response['choices'][0]['message']['content'].strip()
                except Exception as e:
                    answer = f"Error: {e}"
                response_box.delete("1.0", tk.END)
                response_box.insert(tk.END, answer)

            threading.Thread(target=get_ai_response).start()

        tk.Button(ai_win, text="Ask AI", command=ask_ai).pack(pady=5)

    tk.Button(btn_frame, text="AI Helper", command=show_ai_helper).grid(row=0, column=5, padx=5)

    gui.mainloop()



if __name__ == "__main__":
    main()



