# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

#=========== Functions =============

def read_task_file():
    """
    The function 'read_task_file' reads tasks.txt, 
    which is needed several times during this program
    in order to be able to make changes and eventually 
    write back to the text file.  
    This function helps to avoid code repetition.
    """
    with open("tasks.txt", "r") as file:
        global tasks
        tasks = []
        for line in file:
            line_split = line.strip().split(";")
            user_dict = {"username": line_split[0],
                        "title": line_split[1],
                        "description": line_split[2],
                        "due_date": line_split[3],
                        "assigned_date": line_split[4],
                        "completed": line_split[5]
                        }
            tasks.append(user_dict)


def reg_user():
    """
    The function 'reg_user' allows the user to register a new user.
    It will check if the entered username is already in use. 
    If it is, the program will display an error message and 
    prompt the user to enter a different username.

    The function will also ask the user to confirm the password.
    If the passwords do not match, an error message will appear.

    The username and password will be written to user.txt file 
    straight away if a new user has been added successfully.
    """
    print()
    print("-" * 60)
    print("\n" + " " * 20 + " REGISTERING A USER " + " " * 20)
    end = False
    while not end:
        # Prompt for new username and check if it exists.
        new_username = input("\nNew Username: ")
        if new_username in username_password:
            print("\nThis username is already in use. "
                  "\nPlease enter a different username.")
            continue 

        # Input validation; in case user enters nothing.
        if new_username == '':
            print("Please enter a username.")
            continue

        # Prompt for password and check if they match.
        while True:
            new_password = input("New Password: ")

            # Input validation; in case user enters nothing.
            if new_password == '':
                print("\nPlease enter a password.")
                continue
            confirm_password = input("Confirm Password: ")
            
            if new_password == confirm_password:
                print(f"\nNew user '{new_username}' added.")
                username_password[new_username] = new_password
                end = True
                break
            
            else:
                    print("\nPasswords do not match.")

    with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))   



def add_task():
    """
    The function 'add_task' allows the user to add a task and assign it
    to a registered user.
    Every task includes a user, title, description, due date,
    current date and if it is completed.
    This will be written to the tasks.txt file straight away.
    """
    print()
    print("-" * 60)
    print("\n" + " " * 22 + " ADDING A TASK " + " " * 22)
    end = False
    while not end:

        # Prompt for username to assign task to.
        task_username = input("\nName of person assigned to task: ")
        if task_username not in username_password.keys():
            print("\nUser does not exist. Please enter a valid username")
            break

        while True:
            task_title = input("Title of Task: ")
            # Input validation; in case user enters nothing.
            if task_title == '':
                print("\nPlease enter a title.")
                continue
            else:
                break

        while True:
            task_description = input("Description of Task: ")
            # Input validation; in case user enters nothing.
            if task_description == '':
                print("\nPlease enter a description.")
                continue
            else:
                break

        while True:
            # Prompt for due date and check if format is correct.
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime\
                    (task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("\nInvalid datetime format. "
                      "Please use the format specified")

        curr_date = date.today()

        # Add the data to the file task.txt and
        # include 'No' to indicate if the task is complete.
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        
        # Write task to tasks.txt.
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        
        print("\nTask successfully added.")
        break


def view_all():
    """
    The function 'view_all' allows the user to view all tasks,
    including the title, username, assigned date, due date, description.
    """
    print()
    print("-" * 60)
    print("\n" + " " * 24 + " ALL TASKS " + " " * 24)

    # If task_list is empty, advising user that there are no tasks.
    if task_list == []:
        print("\nThere are no tasks.")
    
    for t in task_list:
            disp_str = f"-" * 60 + "\n"
            disp_str += f"\nTask: \t\t\t {t['title']}\n"
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Date Assigned: \t\t \
{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t \
{t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description:\n {t['description']}\n"
            print(disp_str)


def view_mine():
    """
    The function 'view_mine' allows the user to view 
    the current user's tasks.
    The tasks are displayed with a corresponding number that can be
    used to identify the task.
    """
    print()
    print("-" * 60)
    print("\n" + " " * 25 + " MY TASKS " + " " * 24)
    global counter
    counter = []
    
    for i, t in enumerate(task_list, 1):
        if t['username'] == curr_user:
            disp_str = f"\n{i}. Task: \t\t {t['title']}\n"
            disp_str += f"   Assigned to: \t {t['username']}\n"
            disp_str += f"   Date Assigned: \t \
{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"   Due Date: \t\t \
{t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"   Task Description: \n    {t['description']}\n\n"
            disp_str += f"-" * 60
            print(disp_str)
            counter.append(i)
        
        elif task_list != [] and curr_user == t['username']:
            print("\nYou do not have any assigned tasks.\n")
            break
        elif task_list == []:
            print("\nThere are no tasks.\n")
            break
            


def mark_task():
    """
    The function 'mark_task' allows the user to mark the selected task
    as completed by entering the corresponding number.
    This will be written to the tasks.txt file straight away.
    """
    read_task_file()
    
    # Change 'completed' to 'Yes'/True in dict.
    user_task = tasks[selected_task]
    user_task["completed"] = "Yes"
    task_list[selected_task]["completed"] = True
    
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(f"{task['username']};{task['title']};"
                       f"{task['description']};{task['due_date']};"
                       f"{task['assigned_date']};{task['completed']}\n")

    print("\nWe have marked the task as completed.")
    


def edit_task():
    """
    The function 'edit_task' allows the user to reassign a task or
    to change the due date. 

    The user can only reassign the task to a registered user.
    If the task has been reassigned or the due date has been changed,
    this will be written to the tasks.txt file straight away.
    """
    end = False
    while not end:
        # Request a selection from the user.
        edit_option = input('''\nSelect one of the following Options below:
r - Reassign a task
d - Change the due date
: ''').lower()
            
        if edit_option == "r":

            while True:
                # Prompt user for username and check if it exists.
                task_username = input("\nName of person assigned to task: ")
                if task_username not in username_password.keys():
                    print("\nUser does not exist. "
                          "Please enter a valid username")
                    
                
                else:
                    read_task_file()
                    # Change username in dict.
                    user_task = tasks[selected_task]
                    user_task["username"] = task_username
                    task_list[selected_task]["username"] = task_username
                    

                    with open("tasks.txt", "w") as file:
                        for task in tasks:
                            file.write(f"{task['username']};{task['title']};"
                                       f"{task['description']};"
                                       f"{task['due_date']};"
                                       f"{task['assigned_date']};"
                                       f"{task['completed']}\n")
                    
                    print(f"\nTask successfully reassigned "
                          f"to {task_username}.")
                    end = True
                    break
            
        elif edit_option == "d":    

            while True:
                # Prompt user to enter due date and check the format.
                try:
                    task_due_date = input("\nDue date of task (YYYY-MM-DD): ")
                    due_date_time = datetime.strptime\
                        (task_due_date, DATETIME_STRING_FORMAT).date()
                    break

                except ValueError:
                    print("\nInvalid datetime format. "
                          "Please use the format specified.")
            
            read_task_file()
            
            # Change due date in dict.
            user_task = tasks[selected_task]
            user_task["due_date"] = due_date_time
            task_list[selected_task]["due_date"] = due_date_time
            

            with open("tasks.txt", "w") as file:
                for task in tasks:
                    file.write(f"{task['username']};{task['title']};"
                               f"{task['description']};{task['due_date']};"
                               f"{task['assigned_date']};"
                               f"{task['completed']}\n")
            
            print("\nDue date successfully edited.")
            break

        else:
            print("\nInvalid entry.")



def task_overview_report():
    """
    The function 'task_overview_report' allows the admin to generate a
    report to have an overview of the tasks.
    This includes the total number of tasks, number and percentage of 
    completed, incompleted and overdue tasks in a separate text file 
    called task_overview.txt.
    """
    # Set variables
    completed_tasks = 0 
    uncompleted_tasks = 0
    overdue_tasks = 0

    # Update variables for each task
    for task in task_list:
        if task["completed"]:
            completed_tasks += 1
        elif datetime.today() > task["due_date"]:
            uncompleted_tasks += 1
            overdue_tasks += 1
        else:
            uncompleted_tasks += 1

    # Total number of tasks
    total_tasks = len(task_list)

    # Calculate percentage of tasks that are incomplete and overdue
    try:
        perc_complete = round((completed_tasks/total_tasks) * 100, 2)
        perc_incomplete = round((uncompleted_tasks/total_tasks) * 100, 2)
        perc_overdue = round((overdue_tasks/total_tasks) * 100, 2)

    # If there are no tasks -> percentage will be zero
    except ZeroDivisionError:
        perc_incomplete = perc_overdue = 0

    # Write information to task_overview.txt
    date_time = datetime.today().strftime(DATETIME_STRING_FORMAT + "  %H:%M")
    with open("task_overview.txt", "w") as task_re_file:
        task_re_file.write(f"-" * 23 + " TASK OVERVIEW " + \
                           f"-" * 22 + F"\nDate: {date_time}\n")
        task_re_file.write(f"-" * 60 + "\n")
        task_re_file.write(f"\nTotal number of tasks: {total_tasks}\n")
        task_re_file.write(f"Total number of completed tasks: "
                           f"{completed_tasks}\n")
        task_re_file.write(f"Total number of uncompleted tasks: "
                           f"{uncompleted_tasks}\n")
        task_re_file.write(f"Total number of tasks that are overdue: "
                           f"{overdue_tasks}\n")
        task_re_file.write(f"\n")
        task_re_file.write(f"Percentage of completed tasks: "
                           f"{perc_complete}%\n")
        task_re_file.write(f"Percentage of incompleted tasks: "
                           f"{perc_incomplete}%\n")
        task_re_file.write(f"Percentage of tasks that are overdue: "
                           f"{perc_overdue}%")



def user_overview_report():
    """
    The function 'user_overview_report' allows the admin to generate
    a report to have an overview of the users, 
    to who tasks may have been assigned. This report shows: how many tasks 
    are assigned to each user and the number and percentage of 
    complete, incomplete and overdue tasks for each user.
    This will be generated in a separate text file called user_overview.txt.
    """
    # Total number of users.
    total_user = len(username_password)

    # Total number of tasks.
    total_tasks = len(task_list)

    # Set and update variables for each user and store in dict.
    data = {}
    for user in username_password:
        data[user] = user
        user_total_assigned_tasks = 0
        user_completed_task = 0
        user_uncompleted_task = 0
        user_overdue_task = 0

        for task in task_list:
            if task['username'] == user:
                
                if task["completed"]:
                    user_completed_task += 1
                    user_total_assigned_tasks += 1
                elif datetime.today() > task["due_date"]:
                    user_uncompleted_task += 1
                    user_overdue_task += 1
                    user_total_assigned_tasks += 1
                else:
                    user_uncompleted_task += 1
                    user_total_assigned_tasks += 1
        
        data[user] = [user_total_assigned_tasks, user_completed_task, 
                      user_uncompleted_task, user_overdue_task]

    
    # Calculate percentage of total tasks, tasks that 
    # are complete, incomplete and overdue.
    try:
        for user in data:
            if data[user][0] != 0:
                perc_user_total_assigned = \
                    round((data[user][0]/total_tasks) * 100, 2)
                perc_user_complete = \
                    round((data[user][1]/data[user][0]) * 100, 2)
                perc_user_incomplete = \
                    round((data[user][2]/data[user][0]) * 100, 2)
                perc_user_overdue = \
                    round((data[user][3]/data[user][0]) * 100, 2)

                data[user].append(perc_user_total_assigned) 
                data[user].append(perc_user_complete)
                data[user].append(perc_user_incomplete)
                data[user].append(perc_user_overdue)


            # If user does not have any tasks assigned, 
            # the percentages will be 0 and will be stored in dict.
            elif data[user][0] == 0:
                perc_user_total_assigned = perc_user_complete \
                = perc_user_incomplete = perc_user_overdue = 0
                data[user].append(perc_user_total_assigned) 
                data[user].append(perc_user_complete)
                data[user].append(perc_user_incomplete)
                data[user].append(perc_user_overdue)


    # If there are no tasks -> percentage will be zero
    except ZeroDivisionError:
        perc_user_total_assigned = perc_user_complete \
        = perc_user_incomplete = perc_user_overdue = 0


    # Write information to user_overview.txt
    date_time = datetime.today().strftime(DATETIME_STRING_FORMAT + "  %H:%M")
    with open("user_overview.txt", "w") as user_re_file:
        user_re_file.write(f"-" * 23 + " USER OVERVIEW " + 
                           f"-" * 22 + F"\nDate: {date_time}\n")
        user_re_file.write(f"-" * 60 + "\n")
        user_re_file.write(f"\nTotal number of users registered: "
                           f"{total_user}\n")
        user_re_file.write(f"Total number of tasks: {total_tasks}")
        
        # Loop to generate report for each user.
        for user in username_password:
            user_re_file.write(f"\n\n" + "-" * 23 + f" User: {user} " + \
                               f"-" * 23 + "\n\n")
            user_re_file.write(f"Number (Percentage) of total number " 
                               f"of tasks: {data[user][0]} "
                               f"({data[user][4]}%)\n")
            user_re_file.write(f"\n")
            user_re_file.write(f"Number (Percentage) of "
                               f"completed tasks: {data[user][1]} "
                               f"({data[user][5]}%)\n")
            user_re_file.write(f"Number (Percentage) of "
                               f"incompleted tasks: {data[user][2]} "
                               f"({data[user][6]}%)\n")
            user_re_file.write(f"Number (Percentage) of "
                               f"tasks that are overdue: {data[user][3]} "
                               f"({data[user][7]}%)")



def display_statistics():
    """
    The function 'disply_statistcis' allows the admin to display
    the generated reports to the terminal. 

    This function will read the information from task_overview.txt
    and user_overview.txt and display it in a user-friendly manner.

    If the admin has not generated the reports yet, then the code 
    to generate the text files will be called in order to 
    display the information.
    """
    # Create task_overview.txt if it does not exist.
    if not os.path.exists("task_overview.txt"):
        task_overview_report()  
    
    # Create user_overview.txt if it does not exist.
    if not os.path.exists("user_overview.txt"):
        user_overview_report()

    print()
    print("=" * 24 + " STATISTICS " + "=" * 24 + "\n")
    with open("task_overview.txt", 'r') as task_overview_file:
        task_ov_content = task_overview_file.read()
        print(task_ov_content)
    
    print("\n")
    with open("user_overview.txt", 'r') as user_overview_file:
        user_ov_content = user_overview_file.read()
        print(user_ov_content)



# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime\
        (task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime\
        (task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password


logged_in = False
while not logged_in:

    print()
    print("-" * 23 + " TASK MANAGER " + "-" * 23 + "\n")

    # Prompt user to login.
    print("LOGIN\n")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("\nUser does not exist. Please try again.")
        continue

    elif username_password[curr_user] != curr_pass:
        print("\nWrong password. Please try again.")
        continue

    else:
        print("\nLogin Successful!")
        logged_in = True


while True:
    # Presenting different menu to the user and to the admin. 
    # Making sure that the user input is converted to lower case.
    if curr_user == "admin":
        print()
        print("-" * 60)
        menu = input('''\nSelect one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()
        
    else:
        print()
        print("-" * 60)
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()


    elif menu == 'a':
        add_task()


    elif menu == 'va':
        view_all()            


    elif menu == 'vm':
        view_mine()

        while True:
            # Prompt user to select a task or to return to the main menu.
            task_selection = input("\nPlease select a specific task by "
                                "entering \nthe corresponding "
                                "number shown.\n\nIf you want to return "
                                "to the main menu, please enter '-1'\n: ")
            
            # Check if input is numeric and if it is corresponding 
            # to the user's tasks displayed. 
            if task_selection.isnumeric():
                selected_task = int(task_selection)

                if selected_task in counter:
                    # Index correction.
                    selected_task = int(task_selection) - 1
                    break

                else:
                    print("\nThe number selected is not matching "
                        "to any of your tasks.")
            
            elif task_selection == "-1":
                break
            else:
                print("\nInvalid entry.")
                                
        # Return to main menu.
        if task_selection == "-1":
            continue
        
        while True:
            # Prompt user to select to mark or edit the selected task.
            mark_or_edit = input("\nWould you like to mark the task "
                                 "as complete or edit the task. "
                                 "\nChoose by entering 'Mark' or 'Edit': ")

            if mark_or_edit.lower() == "mark":
                mark_task()
                break

            elif mark_or_edit.lower() == "edit":
                # Check if task is incomplete.
                if task_list[selected_task]["completed"] == False:
                    edit_task()
                    break

                else:
                    print("\nYou can no longer edit this task "
                          "as this has been completed.")
                    break

            else:
                print("\nInvalid entry.")


    elif menu == 'gr' and curr_user == 'admin':
        task_overview_report()  
        user_overview_report()       

                
    
    elif menu == 'ds' and curr_user == 'admin': 
        display_statistics()  


    elif menu == 'e':
        print('\nGoodbye!!!')
        exit()


    else:
        print("\nYou have made a wrong choice. Please try again.")