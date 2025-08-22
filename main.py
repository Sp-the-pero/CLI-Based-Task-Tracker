import os
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import box

FILE_NAME = "tasks.txt"
console = Console()

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
def add_task(task, priority="Low", duedate=None):
    tasks.append({"Task": task, "Priority": priority.capitalize(), "Deadline": duedate, "Done": False})
    save_tasks()
    console.print(f"[green]Task added:[/] {task}")

def show_tasks():
    if not tasks:
        console.print("[yellow]No tasks yet![/]")
    else:
        table = Table(title="📋 Task Tracker", box=box.ROUNDED, show_lines=True)
        
        table.add_column("S.No", justify="center", style="cyan", no_wrap=True)
        table.add_column("Task", style="white")
        table.add_column("Priority", style="magenta")
        table.add_column("Due Date", style="blue")
        table.add_column("Status", style="green")

        today = datetime.now()

        for i, task in enumerate(tasks, start=1):
            # Priority Colors
            if task["Priority"].lower() == "high":
                priority_style = "[bold red]High[/]"
            elif task["Priority"].lower() == "medium":
                priority_style = "[yellow]Medium[/]"
            else:
                priority_style = "[green]Low[/]"

            # Status Colors
            # Determine Status
            if task["Done"]:
                status = "[green]✓ Done[/]"
            else:
                if task["Deadline"]:
                    try:
                        due_date = datetime.strptime(task["Deadline"], "%d/%m/%Y")
                        if due_date < today:
                            status = "[bold red]⚠ Due[/]"
                        else:
                            status = "[red]X Pending[/]"
                    except ValueError:
                        status = "[red]X Pending[/]"  # Invalid date
                else:
                    status = "[red]X Pending[/]"

            table.add_row(
                str(i),
                task["Task"],
                priority_style,
                task["Deadline"] if task["Deadline"] else "N/A",
                status
            )

        console.print(table)

def complete_task(index):
    if 0 <= index < len(tasks):
        tasks[index]["Done"] = True
        save_tasks()
        console.print(f"[green]Task completed:[/] {tasks[index]['Task']}")
    else:
        console.print("[red]Invalid task number![/]")

def delete_task(index):
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        save_tasks()
        console.print(f"[red]Task deleted:[/] {removed['Task']}")
    else:
        console.print("[red]Invalid task number![/]")

def task_menu():
    console.print("\n[bold blue]Task Tracker Menu:[/]")
    console.print("[cyan]1.[/] Add Task")
    console.print("[cyan]2.[/] Complete Task")
    console.print("[cyan]3.[/] Delete Task")
    console.print("[cyan]4.[/] Exit")
# ---- Main Program ----
tasks = load_tasks()

while True:
    show_tasks()
    task_menu()

    choice = input("Choose an option: ").lower()

    if choice == "1":                                                   # Task Addition
        task = input("\nEnter task: ")
        priority = input("\nEnter priority (High/Medium/Low): ").lower()
        deadline = input("\nEnter due date (DD/MM/YYYY): ")
        try:                                        
            datetime.strptime(deadline, "%d/%m/%Y") # --> Checks if date is entered in correct form
        except ValueError:
            deadline = None

        add_task(task, priority, deadline)
    elif choice == "2":                                                 # Task Completion
        show_tasks()
        num = int(input("Enter task number to complete: ")) - 1
        complete_task(num)
    elif choice == "3":                                                 # Task Deletion
        show_tasks()
        num = int(input("Enter task number to delete: ")) - 1
        delete_task(num)
    elif choice in ["4","exit"]:                                        # Exit App
        console.print("[bold green]Goodbye! ✅[/]")
        break
    else:
        console.print("[red]Invalid choice! Try again.[/]")
