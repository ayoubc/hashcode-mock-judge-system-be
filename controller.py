import os
import time
import logging
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

from contests.hashcode2019.qualification.score import get_score

app = Flask(__name__)
CORS(app)

_LOGS_FORMAT = '[%(asctime)s]-[%(name)s]-[%(levelname)s] %(message)s'
logging.basicConfig(level=logging.DEBUG, format=_LOGS_FORMAT, datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger(__name__)


@app.route('/files-upload', methods=['POST'])
def compute_score():
    try:
        files = request.files
        if len(files) == 0:
            logger.error('No file was uploaded')
            return make_response({
                'message': 'No file was uploaded',
                'status': 400
            })

        else:
            result = {}
            start = time.perf_counter()
            logger.info('Computing the score ...')
            # with ThreadPoolExecutor() as executor:
            #     res = list(executor.map(lambda args: (args[0], get_score(*args)), files.items()))
            #
            #     for key, score in res:
            #         files[key].stream.close()
            #         result[key] = score
            #         result['total'] = result.get('total', 0) + score
            for key, file in files.items():
                score = get_score(key, file)
                result[key] = score
                result['total'] = result.get('total', 0) + score
                file.stream.close()
            response = jsonify(result)
            response.status_code = 200
            end = time.perf_counter()
            logger.info(f'Done computing the score in {(end - start):.2f} second(s)')
            return response

    except Exception as e:
        logger.error('An error occurred when computing score', exc_info=True)
        return make_response({
            'message': 'Internal Server Error',
            'description': str(e),
            'status': 500
        })


@app.route('/version')
def get_version():
    return jsonify({
        'version': '0.0.2',
        'cpu': os.cpu_count()
    })


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
