from service.student import get_all_students
def main():
    students = get_all_students()

    print(f"✅ Tổng số sinh viên: {len(students)}\n")
    for s in students:
        print("===================================")
        for attr, val in vars(s).items():
            print(f"{attr}: {val}")

if __name__ == "__main__":
    main()