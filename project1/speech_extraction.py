from bottle import route, run, debug, template, request, TEMPLATE_PATH
from myalgorithm import extract_opinion

TEMPLATE_PATH.insert(0,r'D:\works\NLP\kaikeba\ainlp_2019_summer\project1\views')

@route('/new')
def input_document():
    return template('make_form')

@route('/new', method='POST')
def parse_document():
    new = request.forms.task

    result = extract_opinion(new)
    output = template('make_table', rows=result)

    return output


debug(True)
run(host='localhost', port=8800, reloader=True)

## visit http://localhost:8800/new
