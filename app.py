import streamlit as st
import sqlite3

# ---------------- DATABASE ----------------

def connect_db():
    return sqlite3.connect("subject_allocation.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            semester TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            semester TEXT NOT NULL,
            seats INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS allocations (
            student_id TEXT,
            student_name TEXT,
            subject_id TEXT,
            subject_name TEXT,
            PRIMARY KEY (student_id, subject_id)
        )
    """)

    conn.commit()
    conn.close()


create_tables()


# ---------------- ADD STUDENT ----------------

def add_student(stu_id, stu_name, stu_department, semester):

    conn = connect_db()
    cursor = conn.cursor()

    # Check duplicate student ID
    cursor.execute("SELECT * FROM students WHERE id = ?", (stu_id,))

    if cursor.fetchone():
        conn.close()
        return False, "Student ID already exists!"

    cursor.execute("""
        INSERT INTO students (id, name, department, semester)
        VALUES (?, ?, ?, ?)
    """, (stu_id, stu_name, stu_department, semester))

    conn.commit()
    conn.close()

    return True, "Student added successfully."


# ---------------- ADD SUBJECT ----------------

def add_subject(sub_id, sub_name, department, semester, seats):

    conn = connect_db()
    cursor = conn.cursor()

    # Check duplicate subject ID
    cursor.execute("SELECT * FROM subjects WHERE id = ?", (sub_id,))

    if cursor.fetchone():
        conn.close()
        return False, "Subject ID already exists!"

    cursor.execute("""
        INSERT INTO subjects (id, name, department, semester, seats)
        VALUES (?, ?, ?, ?, ?)
    """, (sub_id, sub_name, department, semester, seats))

    conn.commit()
    conn.close()

    return True, "Subject added successfully."


# ---------------- DISPLAY STUDENTS ----------------

def display_students():

    conn = connect_db()

    students = conn.execute("""
        SELECT id, name, department, semester
        FROM students
    """).fetchall()

    conn.close()

    return students


# ---------------- DISPLAY SUBJECTS ----------------

def display_subjects():

    conn = connect_db()

    subjects = conn.execute("""
        SELECT id, name, department, semester, seats
        FROM subjects
    """).fetchall()

    conn.close()

    return subjects


# ---------------- ALLOCATE SUBJECT ----------------

def allocate_subject(student_id, subject_id):

    conn = connect_db()
    cursor = conn.cursor()

    # Find student
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    selected_student = cursor.fetchone()

    if selected_student is None:
        conn.close()
        return False, "Student not found!"

    # Find subject
    cursor.execute("SELECT * FROM subjects WHERE id = ?", (subject_id,))
    selected_subject = cursor.fetchone()

    if selected_subject is None:
        conn.close()
        return False, "Subject not found!"

    # Check duplicate allocation
    cursor.execute("""
        SELECT * FROM allocations
        WHERE student_id = ? AND subject_id = ?
    """, (student_id, subject_id))

    if cursor.fetchone():
        conn.close()
        return False, "This subject is already allocated to this student!"

    # Check seats
    if selected_subject[4] <= 0:
        conn.close()
        return False, "No seats available!"

    # Check department
    if selected_student[2] != selected_subject[2]:
        conn.close()
        return False, "Department does not match!"

    # Check semester
    if selected_student[3] != selected_subject[3]:
        conn.close()
        return False, "Semester does not match!"

    # Create allocation
    cursor.execute("""
        INSERT INTO allocations
        (student_id, student_name, subject_id, subject_name)
        VALUES (?, ?, ?, ?)
    """, (
        student_id,
        selected_student[1],
        subject_id,
        selected_subject[1]
    ))

    # Reduce seat
    cursor.execute("""
        UPDATE subjects
        SET seats = seats - 1
        WHERE id = ?
    """, (subject_id,))

    conn.commit()
    conn.close()

    return True, "Subject allocated successfully!"


# ---------------- VIEW ALLOCATIONS ----------------

def view_allocations():

    conn = connect_db()

    allocations = conn.execute("""
        SELECT student_id, student_name, subject_id, subject_name
        FROM allocations
    """).fetchall()

    conn.close()

    return allocations


# ---------------- REMOVE ALLOCATION ----------------

def remove_allocation(student_id, subject_id):

    conn = connect_db()
    cursor = conn.cursor()

    # Find allocation
    cursor.execute("""
        SELECT * FROM allocations
        WHERE student_id = ? AND subject_id = ?
    """, (student_id, subject_id))

    selected_allocation = cursor.fetchone()

    if selected_allocation is None:
        conn.close()
        return False, "Allocation not found!"

    # Increase available seat
    cursor.execute("""
        UPDATE subjects
        SET seats = seats + 1
        WHERE id = ?
    """, (subject_id,))

    # Remove allocation
    cursor.execute("""
        DELETE FROM allocations
        WHERE student_id = ? AND subject_id = ?
    """, (student_id, subject_id))

    conn.commit()
    conn.close()

    return True, "Subject deallocated successfully."


# =========================================================
#                     STREAMLIT UI
# =========================================================

st.set_page_config(
    page_title="Subject Allocation System",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Subject Allocation System")
st.write("Student and Subject Management System")

st.sidebar.title("MAIN MENU")

choice = st.sidebar.radio(
    "Select Option",
    [
        "Add Student",
        "Add Subject",
        "View Students",
        "View Subjects",
        "Allocate Subject",
        "View Allocation",
        "Remove Allocation"
    ]
)


# ---------------- ADD STUDENT UI ----------------

if choice == "Add Student":

    st.header("Add Student")

    stu_id = st.text_input("Enter student ID")
    stu_name = st.text_input("Enter student Name")
    stu_department = st.text_input("Enter student Department")
    semester = st.text_input("Enter semester")

    if st.button("Add Student"):

        if stu_id == "" or stu_name == "" or stu_department == "" or semester == "":
            st.warning("Please fill all fields.")

        else:
            success, message = add_student(
                stu_id,
                stu_name,
                stu_department,
                semester
            )

            if success:
                st.success(message)
            else:
                st.error(message)


# ---------------- ADD SUBJECT UI ----------------

elif choice == "Add Subject":

    st.header("Add Subject")

    sub_id = st.text_input("Enter subject ID")
    sub_name = st.text_input("Enter subject Name")
    department = st.text_input("Enter department name")
    semester = st.text_input("Enter semester")
    seats = st.number_input(
        "Enter available seats",
        min_value=0,
        step=1
    )

    if st.button("Add Subject"):

        if sub_id == "" or sub_name == "" or department == "" or semester == "":
            st.warning("Please fill all fields.")

        else:
            success, message = add_subject(
                sub_id,
                sub_name,
                department,
                semester,
                seats
            )

            if success:
                st.success(message)
            else:
                st.error(message)


# ---------------- VIEW STUDENTS UI ----------------

elif choice == "View Students":

    st.header("Students List")

    students = display_students()

    if len(students) == 0:
        st.info("No students data are available.")

    else:
        student_data = []

        for student in students:
            student_data.append({
                "Student ID": student[0],
                "Name": student[1],
                "Department": student[2],
                "Semester": student[3]
            })

        st.dataframe(
            student_data,
            use_container_width=True,
            hide_index=True
        )


# ---------------- VIEW SUBJECTS UI ----------------

elif choice == "View Subjects":

    st.header("Subjects List")

    subjects = display_subjects()

    if len(subjects) == 0:
        st.info("No subjects data are available.")

    else:
        subject_data = []

        for subject in subjects:
            subject_data.append({
                "Subject ID": subject[0],
                "Name": subject[1],
                "Department": subject[2],
                "Semester": subject[3],
                "Seats": subject[4]
            })

        st.dataframe(
            subject_data,
            use_container_width=True,
            hide_index=True
        )


# ---------------- ALLOCATE SUBJECT UI ----------------

elif choice == "Allocate Subject":

    st.header("Allocate Subject")

    students = display_students()
    subjects = display_subjects()

    if len(students) == 0:
        st.warning("First add a student.")

    elif len(subjects) == 0:
        st.warning("First add a subject.")

    else:

        student_options = {}

        for student in students:
            student_options[
                student[0] + " - " + student[1]
            ] = student[0]

        subject_options = {}

        for subject in subjects:
            subject_options[
                subject[0] + " - " + subject[1] +
                " | Seats: " + str(subject[4])
            ] = subject[0]

        selected_student = st.selectbox(
            "Select Student",
            list(student_options.keys())
        )

        selected_subject = st.selectbox(
            "Select Subject",
            list(subject_options.keys())
        )

        if st.button("Allocate Subject"):

            student_id = student_options[selected_student]
            subject_id = subject_options[selected_subject]

            success, message = allocate_subject(
                student_id,
                subject_id
            )

            if success:
                st.success(message)
            else:
                st.error(message)


# ---------------- VIEW ALLOCATION UI ----------------

elif choice == "View Allocation":

    st.header("Subject Allocation")

    allocations = view_allocations()

    if len(allocations) == 0:
        st.info("No subject allocations available.")

    else:

        allocation_data = []

        for allocation in allocations:
            allocation_data.append({
                "Student ID": allocation[0],
                "Student Name": allocation[1],
                "Subject ID": allocation[2],
                "Subject Name": allocation[3]
            })

        st.dataframe(
            allocation_data,
            use_container_width=True,
            hide_index=True
        )


# ---------------- REMOVE ALLOCATION UI ----------------

elif choice == "Remove Allocation":

    st.header("Remove Allocation")

    allocations = view_allocations()

    if len(allocations) == 0:
        st.info("No subject allocations available.")

    else:

        allocation_options = {}

        for allocation in allocations:

            display_name = (
                allocation[0] + " - " +
                allocation[1] + " | " +
                allocation[2] + " - " +
                allocation[3]
            )

            allocation_options[display_name] = (
                allocation[0],
                allocation[2]
            )

        selected_allocation = st.selectbox(
            "Select Allocation",
            list(allocation_options.keys())
        )

        if st.button("Remove Allocation"):

            student_id, subject_id = allocation_options[
                selected_allocation
            ]

            success, message = remove_allocation(
                student_id,
                subject_id
            )

            if success:
                st.success(message)
            else:
                st.error(message)
