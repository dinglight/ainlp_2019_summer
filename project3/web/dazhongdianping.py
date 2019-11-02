from flask import Flask, render_template, request, redirect, url_for
from sentiment_analysis import initialize, parse_comment
app = Flask(__name__)

initialize()

@app.route('/')
def index():
    return 'Flask App!'


@app.route('/project3', methods=['GET','POST'])
def project3():
    result = None
    content = ''
    if request.method == 'POST':
        content = request.form['comment']
        df = parse_comment(content)
        result = [df.to_html(classes='data', header='true')]
    return render_template('index.html', content=content, tables=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8800)
