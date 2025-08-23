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
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # Handle corrupted file gracefully
    return []

# ---- Save tasks to file ----
def save_tasks():
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f)

# ---- Functions ----
def add_task(task, priority="Low", duedate=None):
    if not task.strip():
        console.print("[red]Task title cannot be empty![/]")
        return
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
        table.add_column("Days Left", style="yellow")
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

            # Days Left Calculation
            days_left = "N/A"
            if task["Deadline"]:
                try:
                    due_date = datetime.strptime(task["Deadline"], "%d/%m/%Y")
                    diff = (due_date - today).days
                    if diff > 0:
                        days_left = f"{diff} days"
                    elif diff == 0:
                        days_left = "[bold yellow]Today[/]"
                    else:
                        days_left = f"[red]Overdue by {abs(diff)} days[/]"
                except ValueError:
                    days_left = "Invalid Date"

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
                days_left,
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

def update_task(index):
    if 0 <= index < len(tasks):
        task = tasks[index]
        console.print("[blue]Leave input blank to keep existing value.[/]")
        
        new_task = input(f"Enter new task name (current: {task['Task']}): ") or task['Task']
        new_priority = input(f"Enter new priority (High/Medium/Low) (current: {task['Priority']}): ") or task['Priority']
        new_deadline = input(f"Enter new due date (DD/MM/YYYY) (current: {task['Deadline']}): ") or task['Deadline']

        # Validate deadline
        if new_deadline:
            try:
                datetime.strptime(new_deadline, "%d/%m/%Y")
            except ValueError:
                new_deadline = task['Deadline']  # Keep old if invalid
        
        done_input = input(f"Is the task completed? (y/n) (current: {'Yes' if task['Done'] else 'No'}): ").lower()
        if done_input == "y":
            new_done = True
        elif done_input == "n":
            new_done = False
        else:
            new_done = task['Done']

        # Update values
        task.update({"Task": new_task, "Priority": new_priority.capitalize(), "Deadline": new_deadline, "Done": new_done})
        save_tasks()
        console.print("[green]Task updated successfully![/]")
    else:
        console.print("[red]Invalid task number![/]")

def task_menu():
    console.print("\n[bold blue]Task Tracker Menu:[/]")
    console.print("[cyan]1.[/] Add Task")
    console.print("[cyan]2.[/] Complete Task")
    console.print("[cyan]3.[/] Update Task")
    console.print("[cyan]4.[/] Delete Task")
    console.print("[cyan]5.[/] Exit")

# ---- Main Program ----
tasks = load_tasks()

while True:
    show_tasks()
    task_menu()

    choice = input("Choose an option (1,2,3,4,5): ").strip()

    if choice == "1":  # Task Addition
        task = input("\nEnter task: ").strip()
        if not task:
            console.print("[red]Task cannot be empty![/]")
            continue

        priority = input("\nEnter priority (High/Medium/Low): ").lower().strip()
        deadline = input("\nEnter due date (DD/MM/YYYY): ").strip()
        try:
            datetime.strptime(deadline, "%d/%m/%Y")  # Validate date
        except ValueError:
            deadline = None

        add_task(task, priority, deadline)

    elif choice == "2":  # Task Completion
        if not tasks:
            console.print("[yellow]No tasks to complete![/]")
            continue
        num = input("Enter task number to complete: ").strip()
        if not num.isdigit():
            console.print("[red]Invalid input! Must be a number.[/]")
            continue
        complete_task(int(num) - 1)

    elif choice == "3":  # Update Task
        if not tasks:
            console.print("[yellow]No tasks to update![/]")
            continue
        num = input("Enter task number to update: ").strip()
        if not num.isdigit():
            console.print("[red]Invalid input! Must be a number.[/]")
            continue
        update_task(int(num) - 1)

    elif choice == "4":  # Delete Task
        if not tasks:
            console.print("[yellow]No tasks to delete![/]")
            continue
        num = input("Enter task number to delete: ").strip()
        if not num.isdigit():
            console.print("[red]Invalid input! Must be a number.[/]")
            continue
        delete_task(int(num) - 1)

    elif choice in ["5", "exit"]:  # Exit App
        console.print("[bold green]Goodbye! ✅[/]")
        break

    else:
        console.print("[red]Invalid choice! Try again.[/]")
