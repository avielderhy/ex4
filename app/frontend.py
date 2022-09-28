from flask import Flask, render_template
import backend
import os


app = Flask(__name__, template_folder='../template')


@app.route('/', methods=['POST', 'GET'])
def index():
    # get the data from BackEnd and show it in the FrontEnd (the site)
    data, num_of_meetings = backend.frontend_response()
    return render_template(os.environ.get('FLASK_TEMPLATE_FOLDER'), value=data, variable=num_of_meetings)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=81)