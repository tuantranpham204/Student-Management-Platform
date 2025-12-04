import json
from service.student import get_students_by_class
from service.score import get_scores_by_student
from service.sectional_class import get_class_by_id as get_sec_class
from service.subject import get_subject_by_id
from service.student import get_students_by_class
import json


def calculate_subject_average(score, coff_dict):
    """
    Calculates subject average based on the specific coefficient configuration.
    formula: (r1*c1) + (r2*c2) + (r3*c3) + (mid*cm) + (fin*cf)
    """
    # Default scores to 0.0 if None
    r1 = float(score.regular1) if score.regular1 is not None else 0.0
    r2 = float(score.regular2) if score.regular2 is not None else 0.0
    r3 = float(score.regular3) if score.regular3 is not None else 0.0
    mid = float(score.midterm) if score.midterm is not None else 0.0
    fin = float(score.final) if score.final is not None else 0.0

    # Get coefficients (default to 0.0 if missing)
    c1 = float(coff_dict.get('reg1', 0))
    c2 = float(coff_dict.get('reg2', 0))
    c3 = float(coff_dict.get('reg3', 0))
    cm = float(coff_dict.get('mid', 0))
    cf = float(coff_dict.get('fin', 0))

    # Tính tổng hệ số
    total_coeff = c1 + c2 + c3 + cm + cf

    # Tránh chia cho 0
    if total_coeff == 0:
        return 0.0

    # Tính điểm trung bình có trọng số (CHIA CHO TỔNG HỆ SỐ)
    average = (r1 * c1 + r2 * c2 + r3 * c3 + mid * cm + fin * cf) / total_coeff
    return round(average, 2)


def convert_to_gpa_4(score_10):
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

def get_coefficient_name(coff_json):
    """Chuyển đổi JSON coefficient thành tên hệ số"""
    if not coff_json:
        return "Không xác định"
    
    # Parse JSON nếu là string
    if isinstance(coff_json, str):
        try:
            import json
            # Thay single quotes bằng double quotes để parse JSON đúng
            coff_str = coff_json.replace("'", '"')
            coff = json.loads(coff_str)
            print(f"✅ Parsed successfully: {coff}")
        except Exception as e:
            print(f"❌ ERROR parsing coff: {coff_json} -> {e}")
            # Fallback: trả về chuỗi rút gọn thay vì chuỗi gốc
            return "Hệ số không xác định"
    else:
        coff = coff_json
        print(f"✅ Already dict: {coff}")
    
    # Debug: in ra giá trị để kiểm tra
    print(f"🔍 Checking: reg1={coff.get('reg1')}, reg2={coff.get('reg2')}, reg3={coff.get('reg3')}, mid={coff.get('mid')}, fin={coff.get('fin')}")
    
    # Mapping các hệ số
    # Hệ số 1: Thể chất (reg1:0.2, reg2:0.2, reg3:0.1, mid:0.0, fin:0.5)
    if (coff.get('reg1') == 0.2 and coff.get('reg2') == 0.2 and 
        coff.get('reg3') == 0.1 and coff.get('mid') == 0.0 and coff.get('fin') == 0.5):
        print("✅ Matched: Hệ số 1")
        return "Hệ số 1 (Thể chất)"
    
    # Hệ số 2: Cơ sở ngành (reg1:0.1, reg2:0.1, reg3:0.1, mid:0.2, fin:0.5)
    elif (coff.get('reg1') == 0.1 and coff.get('reg2') == 0.1 and 
          coff.get('reg3') == 0.1 and coff.get('mid') == 0.2 and coff.get('fin') == 0.5):
        print("✅ Matched: Hệ số 2")
        return "Hệ số 2 (Cơ sở ngành)"
    
    # Hệ số 3: Đại cương (reg1:0.1, reg2:0.1, reg3:0.0, mid:0.3, fin:0.5)
    elif (coff.get('reg1') == 0.1 and coff.get('reg2') == 0.1 and 
          coff.get('reg3') == 0.0 and coff.get('mid') == 0.3 and coff.get('fin') == 0.5):
        print("✅ Matched: Hệ số 3")
        return "Hệ số 3 (Đại cương)"
    
    # Hệ số 4: Chuyên ngành (reg1:0.2, reg2:0.2, reg3:0.0, mid:0.0, fin:0.6)
    elif (coff.get('reg1') == 0.2 and coff.get('reg2') == 0.2 and 
          coff.get('reg3') == 0.0 and coff.get('mid') == 0.0 and coff.get('fin') == 0.6):
        print("✅ Matched: Hệ số 4")
        return "Hệ số 4 (Chuyên ngành)"
    
    # Hệ số 5: Ngoại ngữ (giống hệ số 2)
    
    else:
        print(f"⚠️ No match found, returning custom")
        return "Hệ số tùy chỉnh"
def get_class_statistics(class_id):
    """Lấy thống kê điểm của một lớp"""
    
    students = get_students_by_class(class_id)
    statistics = []
    
    for student in students:
        scores = get_scores_by_student(student.sid)
        
        total_score_10 = 0
        total_gpa_4 = 0
        subject_count = 0
        
        for score in scores:
            # Lấy thông tin lớp học phần
            sectional_class = get_sec_class(score.sectional_class_id)
            if not sectional_class:
                continue
            
            # Lấy thông tin môn học để có hệ số
            subject = get_subject_by_id(sectional_class.subject_id)
            if not subject or not subject.coff:
                continue
            
            # Parse hệ số từ JSON
            if isinstance(subject.coff, str):
                try:
                    coff_dict = json.loads(subject.coff.replace("'", '"'))
                except:
                    continue
            else:
                coff_dict = subject.coff
            
            # Tính điểm trung bình môn với hệ số đúng
            avg = calculate_subject_average(score, coff_dict)
            total_score_10 += avg
            total_gpa_4 += convert_to_gpa_4(avg)
            subject_count += 1
        
        if subject_count > 0:
            avg_10 = round(total_score_10 / subject_count, 2)
            avg_4 = round(total_gpa_4 / subject_count, 2)
            letter = get_letter_grade(avg_10)
        else:
            avg_10 = 0.0
            avg_4 = 0.0
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

def get_student_detailed_scores(student_id):
    """Lấy điểm chi tiết của sinh viên kèm thông tin môn học"""
    from service.student import get_all_students
    from service.score import get_scores_by_student
    from service.sectional_class import get_all_classes as get_all_sectional_classes
    from service.subject import get_all_subjects
    
    # Lấy thông tin sinh viên
    students = get_all_students()
    student = next((s for s in students if s.sid == student_id), None)
    
    if not student:
        return None
    
    # Lấy tất cả điểm của sinh viên
    scores = get_scores_by_student(student_id)
    
    # Lấy danh sách lớp học phần và môn học
    sectional_classes = get_all_sectional_classes()
    subjects = get_all_subjects()
    
    # Tạo dict để tra cứu nhanh
    sectional_class_dict = {sc.id: sc for sc in sectional_classes}
    subject_dict = {subj.id: subj for subj in subjects}
    
    detailed_scores = []
    for score in scores:
        # Lấy thông tin lớp học phần
        sectional_class = sectional_class_dict.get(score.sectional_class_id)
        if not sectional_class:
            continue
        
        # Lấy thông tin môn học
        subject = subject_dict.get(sectional_class.subject_id)
        if not subject:
            continue
        
        # Tính điểm trung bình môn
        # Lấy hệ số thực tế từ môn học
        if isinstance(subject.coff, str):
            try:
                coff_dict = json.loads(subject.coff.replace("'", '"'))
            except:
                # Nếu parse lỗi, bỏ qua môn này
                continue
        else:
            coff_dict = subject.coff

        # Tính điểm trung bình môn với hệ số đúng
        avg = calculate_subject_average(score, coff_dict)
        
        detailed_scores.append({
            'subject_id': subject.id,
            'subject_name': subject.name,
            'subject_coff': subject.coff,
            'regular1': score.regular1 if score.regular1 is not None else 0,
            'regular2': score.regular2 if score.regular2 is not None else 0,
            'regular3': score.regular3 if score.regular3 is not None else 0,
            'midterm': score.midterm if score.midterm is not None else 0,
            'final': score.final if score.final is not None else 0,
            'average': avg,
            'gpa_4': convert_to_gpa_4(avg),
            'letter_grade': get_letter_grade(avg)
        })
    
    return {
        'student_id': student.sid,
        'student_name': f"{student.fname} {student.lname}",
        'student_dob': student.dob,
        'student_gender': student.gender,
        'student_class': student.departmental_class_id,
        'scores': detailed_scores
    }
