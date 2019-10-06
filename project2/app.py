from bottle import route, run, debug, template, request, TEMPLATE_PATH
from autosumarization import extract_sumarization

TEMPLATE_PATH.insert(0,r'D:\works\NLP\kaikeba\ainlp_2019_summer\project2\views')

@route('/project2')
def input_document():
    return template('make_form')

@route('/project2', method='POST')
def parse_document():
    text = request.forms.task
    size = int(request.forms.size)

    output = extract_sumarization(text, size)
    return output


debug(True)
run(host='localhost', port=8800, reloader=True)

## visit http://localhost:8800/new
