student_grades = {}

while True:
	print("\n1. Add student")
	print("2. Update grade")
	print("3. Print all grades")
	print("4. Exit")

	choice = input("Choose an option: ")

	if choice == "1":
		name = input("Enter student name: ")
		grade = input("Enter student grade: ")

		if name in student_grades:
			print("Student already exists.")
		else:
			student_grades[name] = grade
			print("Student added.")

	elif choice == "2":
		name = input("Enter student name: ")

		if name in student_grades:
			student_grades[name] = input("Enter new grade: ")
			print("Grade updated.")
		else:
			print("Student not found.")

	elif choice == "3":
		if student_grades:
			for name, grade in student_grades.items():
				print(f"{name}: {grade}")
		else:
			print("No student grades available.")

	elif choice == "4":
		print("Goodbye!")
		break

	else:
		print("Invalid option.")
