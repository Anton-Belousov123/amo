from flask import Flask, request

app = Flask(__name__)


@app.route('location/<scope_id>')
def hello(scope_id):
    print(f"{scope_id=}")
    if request.method == 'POST':
        print(f"{request.data=}, post")
    else:
        print(f"{request.form}, get")


app.run(debug=True, port=8000)