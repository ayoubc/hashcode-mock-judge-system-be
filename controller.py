import traceback

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

from contests.hashcode2019.qualification.score import get_score

app = Flask(__name__)
CORS(app)


@app.route('/files-upload', methods=['POST'])
def compute_score():
    try:
        files = request.files
        if len(files) == 0:
            return make_response({
                'message': 'No file part in the request',
                'status': 400
            })

        else:
            result = {}
            for key in files:
                file = files[key]
                score = get_score(file, key)
                result[key] = score
                result['total'] = result.get('total', 0) + score
                file.stream.close()

            response = jsonify(result)
            response.status_code = 200
            return response

    except:
        print(traceback.format_exc())
        return make_response({
            'message': 'Internal Server Error',
            'status': 500
        })


@app.route('/version')
def get_version():
    return jsonify({'version': '0.0.1'})


if __name__ == '__main__':
    app.run(debug=True)
