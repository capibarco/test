from flask import Flask, render_template, request, make_response
from parser import parse

app = Flask(__name__)


@app.route('/')
def index():
    """
    Renders index.html page
    :return:
    """
    return render_template('index.html')


@app.route('/parse', methods=['POST'])
def parsing():
    """Handle the 'parse' route for form submission.

    Extracts the link from the form data and invokes the 'parse' function to obtain the data.
    Converts the data to a CSV string format and generates a response with the CSV file for download.

    :return: Response: Flask response object containing the CSV data as an attachment.
    """
    link = request.form['link']
    data = parse(link)

    response = make_response(data)
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    response.headers['Content-type'] = 'text/csv'

    return response


if __name__ == '__main__':
    app.run()
