def get_template(category):

    if "exam" in category:
        return "exam.png"
    elif "coding" in category or "debug" in category:
        return "coding.png"
    elif "office" in category:
        return "office.png"
    elif "cricket" in category:
        return "cricket.png"
    else:
        return "student.png"