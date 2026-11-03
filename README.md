# Subject Allocation System

A simple Subject Allocation System built with Python. It provides two versions:

- **Streamlit web application** (`app.py`) — uses SQLite to store students, subjects, and allocations.
- **Command-line application** (`main.py`) — runs in the terminal and stores data in memory while the program is running.

## Features

- Add and manage student records.
- Add and manage subject records, including available seats.
- View the list of students and subjects.
- Allocate subjects to students.
- Check that the student's department and semester match the subject.
- Prevent duplicate student IDs, subject IDs, and duplicate allocations.
- Check seat availability before allocating a subject.
- Remove an allocation and return the seat to the subject.

## Technologies Used

- Python
- Streamlit (web interface)
- SQLite (database for the Streamlit application)

## Project Structure

```text
subject-allocation-system/
│
├── app.py                 # Streamlit web application
├── main.py                # Command-line application
├── subject_allocation.db  # SQLite database (created automatically if absent)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

> Keep the filenames consistent with the commands below. If your files have different names, either rename them or update the commands.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the repository URL with your own GitHub repository URL.

### 2. Create a virtual environment (recommended)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Streamlit Web Application

```bash
streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to use the application.

The web application creates the required SQLite tables when it starts. The database file is named `subject_allocation.db` and is stored in the application's working directory.

## Run the Command-Line Application

```bash
python main.py
```

Follow the menu displayed in the terminal and enter the number for the operation you want.

**Note:** The command-line version stores records in Python lists, so its data is cleared when the program exits. The Streamlit version uses SQLite for persistent storage.

## Allocation Rules

A subject can be allocated only when:

1. The student ID exists.
2. The subject ID exists.
3. The same subject has not already been allocated to that student.
4. The subject has at least one available seat.
5. The student's department matches the subject's department.
6. The student's semester matches the subject's semester.

When an allocation is removed, the available seat count is increased by one.

## Database

The Streamlit version uses SQLite with three tables:

- `students` — student ID, name, department, and semester.
- `subjects` — subject ID, name, department, semester, and available seats.
- `allocations` — student and subject allocation details.

SQLite is included with Python, so no separate database server is required.

## Future Improvements

- Add student and subject update/delete options.
- Add search and filtering.
- Add authentication for administrators.
- Add input validation and clearer error handling.
- Add export options for allocation reports.
