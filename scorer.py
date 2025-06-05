def score_resume(parsed_json):
    if not parsed_json:
        return 0, "Error in parsing resume data."

    score = 0

    # Scoring logic
    if parsed_json.get("Skills"):
        score += len(parsed_json["Skills"]) * 2

    if parsed_json.get("Projects"):
        score += len(parsed_json["Projects"]) * 5

    if parsed_json.get("Work Experience"):
        score += len(parsed_json["Work Experience"]) * 10

    if parsed_json.get("Extra-curricular Activities"):
        score += len(parsed_json["Extra-curricular Activities"]) * 3

    score = min(score, 100)  # cap at 100

    breakdown = {
        "Skills": len(parsed_json.get("Skills", [])) * 2,
        "Projects": len(parsed_json.get("Projects", [])) * 5,
        "Work Experience": len(parsed_json.get("Work Experience", [])) * 10,
        "Extra-curricular Activities": len(parsed_json.get("Extra-curricular Activities", [])) * 3,
    }

    return score, breakdown
