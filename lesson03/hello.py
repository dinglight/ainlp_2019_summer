from bottle import route, run

@route('/hello')
def hello():
    return "My first Python Web App!"

run(host='localhost', port=8080, debug=True)

## visit http://localhost:8080/hello 
