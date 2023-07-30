from flask import Flask, render_template, request
import json
import os
app = Flask(__name__)
email = "null"


@app.route('/')
def Base_qstn_paper_set():
    return render_template('first.html')

@app.route('/foo', methods=['POST', 'GET'])
def foo():
    if request.method == 'POST':
        first = request.form['first']
        second = request.form['second']
        third = request.form['third']

        email = request.form['emailID']
        ans = {"a1": first, "a2": second, "a3": third, "email": email}
        json_object = json.dumps(ans, indent=4)
        if os.path.exists("data/"+email+".json")==False:
            with open("data/" + email + ".json", "w") as outfile:
                outfile.write(json_object)
            return render_template('Exam_end.html')
        else:
            return render_template('exist_student.html')


if __name__ == '__main__':
    app.run()
