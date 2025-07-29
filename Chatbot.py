from Database import Database

class Chatbot(Database):
    def __init__(self):
        super().__init__('student.db')
        Database.create_table(self)

    def add(self, name, age, grade, email):
        try:
            self.insert_user(name, int(age), grade, email)
            return f"Student {name} added successfully!"
        except Exception as e:
            return f"Invalid input. Error: {e}"

    def student_name(self, name):
        result = self.get_user_by_name(name)
        return f"Student found: {result}" if result else "No student found with that name."

    def student_grade(self, grade):
        result = self.get_user_by_grade(grade)
        return f"Student found: {result}" if result else "No student found with that grade."

    def student_correct_information(self, name, info, age=None, grade=None):
        result = self.get_user_by_name(name)
        if not result:
            return "No student found with that name."
        if info == "age":
            self.update_user_age(name, age)
            return f"Age updated for {name}."
        elif info == "grade":
            self.update_user_grade(name, grade)
            return f"Grade updated for {name}."
        elif info == "all information":
            self.update_user_all_info(name, age, grade)
            return f"All information updated for {name}."
        return "Invalid choice. Please choose 'age', 'grade', or 'all information'."

    def delete_students(self):
        self.delete_all_users()
        return "All students deleted."

    def handle_command(self, command, name=None, age=None, grade=None, email=None, info=None):
        command = command.strip().lower()
        if command == "add student":
            return self.add(name, age, grade, email)
        elif command == "get student with name":
            return self.student_name(name)
        elif command == "get student with grade":
            return self.student_grade(grade)
        elif command == "correct the student information":
            return self.student_correct_information(name, info, age, grade)
        elif command == "delete all students":
            return self.delete_students()
        return "Unknown command."