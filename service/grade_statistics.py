def calculate_subject_average(regular1, regular2, regular3, midterm, final):
    """Tính điểm trung bình môn học (thang 10)"""
    # Tính trung bình điểm regular
    regulars = [r for r in [regular1, regular2, regular3] if r is not None]
    regular_avg = sum(regulars) / len(regulars) if regulars else 0
    
    # Công thức: Regular 10% + Midterm 30% + Final 60%
    average = regular_avg * 0.1 + (midterm or 0) * 0.3 + (final or 0) * 0.6
    return round(average, 2)
def convert_to_gpa_4(score_10):
    """Quy đổi điểm từ thang 10 sang thang 4"""
    if score_10 >= 8.5: return 4.0
    elif score_10 >= 7.7: return 3.5
    elif score_10 >= 7.0: return 3.0
    elif score_10 >= 6.2: return 2.5
    elif score_10 >= 5.4: return 2.0
    elif score_10 >= 4.7: return 1.5
    elif score_10 >= 4.0: return 1.0
    else: return 0.0
def get_letter_grade(score_10):
    """Xếp loại chữ từ điểm thang 10"""
    if score_10 >= 8.5: return 'A'
    elif score_10 >= 7.7: return 'B+'
    elif score_10 >= 7.0: return 'B'
    elif score_10 >= 6.2: return 'C+'
    elif score_10 >= 5.4: return 'C'
    elif score_10 >= 4.7: return 'D+'
    elif score_10 >= 4.0: return 'D'
    else: return 'F'
def get_class_statistics(class_id):
    """Lấy thống kê điểm của một lớp"""
    from service.student import get_students_by_class
    from service.score import get_scores_by_student
    
    students = get_students_by_class(class_id)
    statistics = []
    
    for student in students:
        scores = get_scores_by_student(student.sid)
        
        total_score_10 = 0
        total_gpa_4 = 0
        subject_count = 0
        
        for score in scores:
            avg = calculate_subject_average(
                score.regular1, score.regular2, score.regular3,
                score.midterm, score.final
            )
            total_score_10 += avg
            total_gpa_4 += convert_to_gpa_4(avg)
            subject_count += 1
        
        if subject_count > 0:
            avg_10 = round(total_score_10 / subject_count, 2)
            avg_4 = round(total_gpa_4 / subject_count, 2)
            letter = get_letter_grade(avg_10)
        else:
            avg_10 = 0
            avg_4 = 0
            letter = 'N/A'
        
        statistics.append({
            'student_id': student.sid,
            'student_name': f"{student.fname} {student.lname}",
            'avg_score_10': avg_10,
            'avg_gpa_4': avg_4,
            'letter_grade': letter,
            'subject_count': subject_count
        })
    
    return statistics