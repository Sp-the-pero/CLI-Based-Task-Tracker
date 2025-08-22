import os
import json

FILE_NAME = "tasks.txt"

# ---- Load tasks from file if it exists ----
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

# ---- Save tasks to file ----
def save_tasks():
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f)

# ---- Functions ----
def add_task(task):
    tasks.append({"task": task, "done": False})
    save_tasks()
    print(f"Task added: {task}")

def show_tasks():
    if not tasks:
        print("No tasks yet!")
    else:
        for i, task in enumerate(tasks, start=1):
            status = "✓" if task["done"] else "✗"
            print(f"{i}. {task['task']} [{status}]")

def complete_task(index):
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks()
        print(f"Task completed: {tasks[index]['task']}")
    else:
        print("Invalid task number!")

def delete_task(index):
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        save_tasks()
        print(f"Task deleted: {removed['task']}")
    else:
        print("Invalid task number!")

# ---- Main Program ----
tasks = load_tasks()

while True:
    print("\nTask Tracker Menu:")
    print("1. Add Task")
    print("2. Show Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        task = input("Enter task: ")
        add_task(task)
    elif choice == "2":
        show_tasks()
    elif choice == "3":
        show_tasks()
        num = int(input("Enter task number to complete: ")) - 1
        complete_task(num)
    elif choice == "4":
        show_tasks()
        num = int(input("Enter task number to delete: ")) - 1
        delete_task(num)
    elif choice == "5":
        print("Goodbye! ✅")
        break
    else:
        print("Invalid choice! Try again.")
