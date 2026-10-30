students=[]
subjects=[]
allocations=[]

def add_student():

    stu_id = input("Enter student ID : ")

    # Check duplicate student ID
    for student in students:
        if student["id"] == stu_id:
            print("Student ID already exists!")
            return

    stu_name = input("Enter student Name : ")
    stu_department = input("Enter student Department : ")
    semester = input("Enter semester : ")

    student = {
        "id": stu_id,
        "name": stu_name,
        "department": stu_department,
        "semester": semester
    }

    students.append(student)

    print("Student added successfully.")

def add_subject():

    sub_id = input("Enter subject id : ")

    # Check duplicate subject ID
    for subject in subjects:
        if subject["id"] == sub_id:
            print("Subject ID already exists!")
            return

    sub_name = input("Enter subject Name : ")
    department = input("Enter department name : ")
    semester = input("Enter semester : ")
    seats = int(input("Enter available seats : "))

    subject = {
        "id": sub_id,
        "name": sub_name,
        "department": department,
        "semester": semester,
        "seats": seats
    }

    subjects.append(subject)

    print("Subject added successfully.")

def display_students():
    if len(students)==0:
        print("No students data are available.")
        return

    print("Students lists:")

    for student in students:
        print("Student ID:", student["id"])
        print("Name:", student["name"])
        print("Department:", student["department"])
        print("Semester:", student["semester"])
        print("------------------------")

def display_subjects():
    if len(subjects)==0:
        print("No subjects data are available.")
        return

    print("Subjects lists:")

    for subject in subjects:
        print("Student ID:", subject["id"])
        print("Name:", subject["name"])
        print("Department:", subject["department"])
        print("Semester:", subject["semester"])
        print("Seats:", subject["seats"])
        print("------------------------")

#ALLOCATE SUBJECT

def allocate_subject():
    student_id = input("Enter student ID: ")
    subject_id = input("Enter subject ID: ")

    student_found = False
    subject_found = False

    # Find student
    for student in students:
        if student["id"] == student_id:
            student_found = True
            selected_student = student
            break

    # Find subject
    for subject in subjects:
        if subject["id"] == subject_id:
            subject_found = True
            selected_subject = subject
            break

    # Check student
    if student_found == False:
        print("Student not found!")
        return

    # Check subject
    if subject_found == False:
        print("Subject not found!")
        return

    # Check duplicate allocation
    for allocation in allocations:
        if allocation["student_id"] == student_id and allocation["subject_id"] == subject_id:
            print("This subject is already allocated to this student!")
            return

    # Check seats
    if selected_subject["seats"] <= 0:
        print("No seats available!")
        return

    # Check department
    if selected_student["department"] != selected_subject["department"]:
        print("Department does not match!")
        return

    # Check semester
    if selected_student["semester"] != selected_subject["semester"]:
        print("Semester does not match!")
        return

    # Create allocation
    allocation = {
        "student_id": student_id,
        "student_name": selected_student["name"],
        "subject_id": subject_id,
        "subject_name": selected_subject["name"]
    }
    allocations.append(allocation)

    # Reduce seat
    selected_subject["seats"] = selected_subject["seats"] - 1
    print("Subject allocated successfully!")


#View ALLOCATIONS---------------------------

def view_allocations():
    if len(allocations)==0:
        print("No subject allocations avaliable.")
        return
    print("\n-------SUBJECT ALLOCATION-------")

    for allocation in allocations:
        print("Student ID: ", allocation["student_id"])
        print("Student Name: ", allocation["student_name"])
        print("Subject ID: ", allocation["subject_id"])
        print("Subject Name: ", allocation["subject_name"])
        print("--------------")

#REMOVE ALLOCATION---------------
def remove_allocation():

    student_id = input("Enter student ID: ")
    subject_id = input("Enter subject ID: ")

    selected_allocation = None

    # Find allocation
    for allocation in allocations:
        if allocation["student_id"] == student_id and allocation["subject_id"] == subject_id:
            selected_allocation = allocation
            break

    # Check allocation
    if selected_allocation is None:
        print("Allocation not found!")
        return

    # Find subject
    for subject in subjects:
        if subject["id"] == subject_id:
            selected_subject = subject
            break

    # Increase available seat
    selected_subject["seats"] = selected_subject["seats"] + 1

    # Remove allocation
    allocations.remove(selected_allocation)
    print("Subject deallocated successfully!")


#MAIN MENU----------------------------------
while True:

    print("---SUBJECT ALLOCATION---")

    print("1. Add Student")
    print("2. Add Subject")
    print("3. View Students")
    print("4. View Subjects")
    print("5. Allocation Subject")
    print("6. View Allocation")
    print("7. Remove Allocation")
    print("8. Exit")

    choice=input("Enter your choice: ")

    if choice=="1":
        add_student()
    elif choice=="2":
        add_subject()
    elif choice=="3":
        display_students()
    elif choice=="4":
        display_subjects()
    elif choice=="5":
        allocate_subject()
    elif choice=="6":
        view_allocations()
    elif choice=="7":
        remove_allocation()
    elif choice=="8":
        print("Thank You for using Allocation System.")
        break
    else:
        print("Invalid choice! Please try again.")