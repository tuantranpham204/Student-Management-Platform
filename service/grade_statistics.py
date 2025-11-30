import json
from service.student import get_students_by_class
from service.score import get_scores_by_student
from service.sectional_class import get_class_by_id as get_sec_class
from service.subject import get_subject_by_id


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

    average = (r1 * c1) + (r2 * c2) + (r3 * c3) + (mid * cm) + (fin * cf)
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
    if score_10 >= 8.5: return 'A'
    elif score_10 >= 7.7: return 'B+'
    elif score_10 >= 7.0: return 'B'
    elif score_10 >= 6.2: return 'C+'
    elif score_10 >= 5.4: return 'C'
    elif score_10 >= 4.7: return 'D+'
    elif score_10 >= 4.0: return 'D'
    else: return 'F'
def get_class_statistics(class_id):
    students = get_students_by_class(class_id)
    statistics = []

    # Cache for coefficients: {sectional_class_id: coefficient_dict}
    # This prevents fetching the same subject/sectional class info repeatedly
    coeff_cache = {}

    for student in students:
        scores = get_scores_by_student(student.sid)

        total_score_10 = 0
        total_gpa_4 = 0
        subject_count = 0

        for score in scores:
            sec_id = score.sectional_class_id

            # 1. Resolve Coefficients for this score (using cache)
            if sec_id not in coeff_cache:
                # Fetch sectional class to find subject
                sec_class = get_sec_class(sec_id)
                if sec_class:
                    # Fetch subject to find coefficients
                    subject = get_subject_by_id(sec_class.subject_id)
                    if subject and subject.coff:
                        try:
                            # Parse JSON string from DB
                            if isinstance(subject.coff, str):
                                coeff_cache[sec_id] = json.loads(subject.coff)
                            else:
                                coeff_cache[sec_id] = subject.coff
                        except json.JSONDecodeError:
                            coeff_cache[sec_id] = {}  # Fail safe
                    else:
                        coeff_cache[sec_id] = {}
                else:
                    coeff_cache[sec_id] = {}

            coeffs = coeff_cache.get(sec_id, {})

            # 2. Calculate Average for this subject
            if coeffs:
                avg = calculate_subject_average(score, coeffs)
                total_score_10 += avg
                total_gpa_4 += convert_to_gpa_4(avg)
                subject_count += 1

        # 3. Calculate Overall Student Statistics
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