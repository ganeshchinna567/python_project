from li import Flask, render_template, request
app = Flask(__name__)

students = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    students.append({'name': name, 'grades': []})
    return render_template('index.html', students=students)

@app.route('/assign_grade', methods=['POST'])
def assign_grade():
    student_name = request.form.get('student')
    grade = request.form.get('grade')
    for student in students:
        if student['name'] == student_name:
            student['grades'].append(grade)
            break
    return render_template('index.html', students=students)

@app.route('/view_details/<student_name>')
def view_details(student_name):
    student = next((s for s in students if s['name'] == student_name), None)
    return render_template('details.html', student=student)

@app.route('/calculate_average/<student_name>')
def calculate_average(student_name):
    student = next((s for s in students if s['name'] == student_name), None)
    if student and student['grades']:
        average = sum(map(float, student['grades'])) / len(student['grades'])
        student['average'] = average
    return render_template('details.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)
