# from django.shortcuts import render, redirect

# # MCQ Data (Simulated Database)
# mcq_data = [
#     {
#         "id": 1,
#         "question": "What is the capital of France?",
#         "options": ["Paris", "Berlin", "Madrid", "Rome"],
#         "correct": "Paris",
#     },
#     {
#         "id": 2,
#         "question": "Which planet is known as the Red Planet?",
#         "options": ["Earth", "Mars", "Venus", "Jupiter"],
#         "correct": "Mars",
#     },
#     {
#         "id": 3,
#         "question": "What is the chemical symbol for water?",
#         "options": ["H2O", "CO2", "O2", "N2"],
#         "correct": "H2O",
#     },
# ]

# def enter_name(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         if name:
#             # Reset session data
#             request.session.flush()
#             request.session['name'] = name
#             request.session['score'] = 0
#             request.session['current_question'] = 0
#             return redirect("index")
#     return render(request, "qna/enter_name.html")

# def index(request):
#     # Ensure the user is logged in
#     name = request.session.get('name')
#     if not name:
#         return redirect("enter_name")

#     # Get the current question index
#     current_question_index = request.session.get('current_question', 0)

#     # If all questions are completed, redirect to results
#     if current_question_index >= len(mcq_data):
#         return redirect("results")

#     # Get the current question and options
#     current_question = mcq_data[current_question_index]
#     options = [
#         {"value": opt, "is_correct": opt == current_question["correct"]}
#         for opt in current_question["options"]
#     ]

#     user_answer = None
#     feedback = None

#     if request.method == "POST":
#         # Get the user's answer
#         user_answer = request.POST.get("answer")
#         if user_answer:
#             # Update the score if the answer is correct
#             if user_answer == current_question["correct"]:
#                 request.session['score'] += 1
#                 feedback = "correct"
#             else:
#                 feedback = "incorrect"

#             # Move to the next question
#             request.session['current_question'] += 1
#             request.session.modified = True  # Save session changes

#         # Redirect to refresh the page with the next question
#         return redirect("index")

#     return render(request, "qna/index.html", {
#         'name': name,
#         'question': current_question,
#         'options': options,
#         'user_answer': user_answer,
#         'feedback': feedback,
#     })

# # The results view function
# def results(request):
#     # Ensure the user is logged in
#     name = request.session.get('name')
#     if not name:
#         return redirect("enter_name")

#     # Get the final score
#     score = request.session.get('score', 0)
#     total_questions = len(mcq_data)

#     # Clear session after results
#     request.session.flush()

#     return render(request, "qna/results.html", {
#         'name': name,
#         'score': score,
#         'total': total_questions,
#     })
from django.shortcuts import render, redirect

# MCQ Data (Simulated Database)
mcq_data = [
    {
        "id": 1,
        "question": "What is the capital of France?",
        "options": ["Paris", "Berlin", "Madrid", "Rome"],
        "correct": "Paris",
    },
    {
        "id": 2,
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Venus", "Jupiter"],
        "correct": "Mars",
    },
    {
        "id": 3,
        "question": "What is the chemical symbol for water?",
        "options": ["H2O", "CO2", "O2", "N2"],
        "correct": "H2O",
    },
]

def enter_name(request):
    """Initial view to capture the user's name."""
    # Clear any existing session data
    request.session.flush()
    
    if request.method == "POST":
        name = request.POST.get("name", "").strip()  # Strip whitespace
        if name:  # Check if name is not empty after stripping
            # Initialize session data
            request.session['name'] = name
            request.session['score'] = 0
            request.session['current_question'] = 0
            request.session.modified = True  # Ensure session is saved
            return redirect("index")
            
    return render(request, "qna/enter_name.html")

def index(request):
    """Main view for displaying and processing MCQs."""
    # Ensure the user is logged in
    name = request.session.get('name')
    if not name:
        return redirect("enter_name")

    # Get the current question index
    current_question_index = request.session.get('current_question', 0)

    # If all questions are completed, redirect to results
    if current_question_index >= len(mcq_data):
        return redirect("results")

    # Get the current question and options
    current_question = mcq_data[current_question_index]
    options = [
        {"value": opt, "is_correct": opt == current_question["correct"]}
        for opt in current_question["options"]
    ]

    if request.method == "POST":
        # Check if this is a "next question" request
        if request.POST.get("action") == "next":
            # Move to next question
            request.session['current_question'] = current_question_index + 1
            request.session.modified = True
            return redirect('index')
        
        # Get the user's answer
        user_answer = request.POST.get("answer")
        if user_answer:
            # Update the score if the answer is correct
            if user_answer == current_question["correct"]:
                request.session['score'] = request.session.get('score', 0) + 1
                feedback = "correct"
            else:
                feedback = "incorrect"

            # Render the same page with feedback
            return render(request, "qna/index.html", {
                'name': name,
                'question': current_question,
                'options': options,
                'user_answer': user_answer,
                'feedback': feedback,
            })

    # For GET requests or after processing POST
    return render(request, "qna/index.html", {
        'name': name,
        'question': current_question,
        'options': options,
        'user_answer': None,  # Reset user_answer for new questions
        'feedback': None,     # Reset feedback for new questions
    })

def results(request):
    """Final results view."""
    # Ensure the user is logged in
    name = request.session.get('name')
    if not name:
        return redirect("enter_name")

    # Get the final score
    score = request.session.get('score', 0)
    total_questions = len(mcq_data)

    # Clear session after results
    request.session.flush()

    return render(request, "qna/results.html", {
        'name': name,
        'score': score,
        'total': total_questions,
    })


