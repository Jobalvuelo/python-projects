# TODO List Manager

import json
import os
from datetime import datetime

# File where tasks will be saved
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return[]

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(TASKS_FILE, "w", encoding="utf8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def show_menu():
    """Display the main menu"""
    print("\n" + "="*40)
    print("       TODO LIST MANAGER")
    print("="*40)
    print("1. Add task")
    print("2. Show all tasks")
    print("3. Complete task")
    print("4. Edit task")
    print("5. Delete task")
    print("6. Statistics")
    print("7. Search tasks")
    print("8. Exit")
    print("="*40)

def add_task(tasks):
    """Add a new task"""
    print("\n--- ADD NEW TASK ---")
    task_name = input("Task name: ").strip()
    
    if task_name:
        new_task = {
            "id": len(tasks) + 1,
            "name": task_name,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        tasks.append(new_task)
        save_tasks(tasks)
        print(f"\n✅ Task '{task_name}' added successfully!")
    else:
        print("\n❌ Task name cannot be empty.")

def show_tasks(tasks):
    """Show all tasks"""
    print("\n" + "="*40)
    print("       ALL TASKS")
    print("="*40)
    
    if not tasks:
        print("\n📝 No tasks yet. Add your first task!")
    else:
        for task in tasks:
            status = "✅" if task["completed"] else "⬜"
            created = task.get("created_at", "No date")
            print(f"{task['id']}. {status} {task['name']}")
            print(f"   📅 Created: {created}")
    
    print("="*50)

def show_statistics(tasks):
    """Show task statistics"""
    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    pending = total - completed
    
    print("\n" + "="*40)
    print("       STATISTICS")
    print("="*40)
    print(f"📊 Total tasks: {total}")
    print(f"✅ Completed: {completed}")
    print(f"⬜ Pending: {pending}")
    
    if total > 0:
        percentage = (completed / total) * 100
        print(f"📈 Progress: {percentage:.1f}%")
    
    print("="*40)

def search_tasks(tasks):
    """Search tasks by keyword"""
    if not tasks:
        print("\n📝 No tasks yet. Add your first task!")
        return
    keyword = input("\nEnter keyword to search: ").strip().lower()
    
    if not keyword:
        print("\n❌ Please enter a keyword.")
        return
    # Find tasks that contain the keyword
    found_tasks = [task for task in tasks if keyword in task["name"].lower()]
    
    print("\n" + "="*50)
    print(f"      SEARCH RESULTS FOR: '{keyword}'")
    print("="*50)
    
    if not found_tasks:
        print(f"\n❌ No tasks found with keyword '{keyword}'")
    else:
        for task in found_tasks:
            status = "✅" if task["completed"] else "⬜"
            created = task.get("created_at", "No date")
            print(f"{task['id']}. {status} {task['name']}")
            print(f"   📅 Created: {created}")
        
        print("="*50)

def complete_task(tasks):
    "Mark a task as completed"
    show_tasks(tasks)
    
    if not tasks:
        return
    
    try:
        task_id = int(input("\nEnter task ID to complete: "))
        
        # Find task by ID
        for task in tasks:
            if task['id'] == task_id:
                task["completed"] = True
                save_tasks(tasks)
                print(f"\n✅ Task '{task['name']}' marked as completed!")
                return
        print(f"\n❌ Task with ID {task_id} not found.")
    except ValueError:
        print("\n❌ Please enter a valid number.")
def edit_task(tasks):
    """Edit a task name"""
    show_tasks(tasks)
    
    if not tasks:
        return
    
    try:
        task_id = int(input("\nEnter task ID to edit: "))
        
        # Find task by ID
        for task in tasks:
            if task["id"] == task_id:
                print(f"\nCurrent name: {task['name']}")
                new_name = input("New name: ").strip()
                
                if new_name:
                    old_name = task['name']
                    task['name'] = new_name
                    save_tasks(tasks)
                    print(f"\n✏️ Task updated from '{old_name}' to '{new_name}'!")
                else:
                    print("\n❌ Task name cannot be empty.")
                return
            
            print(f"\n❌ Task with ID {task_id} not found.")
            
    except ValueError:
        print("\n❌ Please enter a valid number.")
                
def delete_task(tasks):
    """Delete a task"""
    show_tasks(tasks)
    
    if not tasks:
        return
    
    try:
        task_id = int(input("\nEnter task ID to delete: "))
        
        # Find and remove task
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                deleted_task = tasks.pop(i)
                save_tasks(tasks)
                print(f"\n🗑️ Task '{deleted_task['name']}' deleted successfully!")
                return
        
        print(f"\n❌ Task with ID {task_id} not found.")
    except ValueError:
        print("\n❌ Please enter a valid number.")

def main():
    """Main function"""
    tasks = load_tasks()
   
    while True:
        show_menu()
        option = input("\nSelect an option (1-8): ")
        
        if option == "1":
           add_task(tasks)
        elif option == "2":
            show_tasks(tasks)
        elif option == "3":
            complete_task(tasks)
        elif option == "4":
            edit_task(tasks)
        elif option == "5":
            delete_task(tasks)
        elif option == "6":
            show_statistics(tasks)
        elif option == "7":
            search_tasks(tasks)
        elif option == "8":
            print("\nGoodbye! 👋")
            break
        else:
            print("\n❌ Invalid option. Please try again.")

# Run the program
if __name__ == "__main__":
    main()