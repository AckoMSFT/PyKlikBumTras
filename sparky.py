import json
import subprocess
from os import environ

from flask import Flask

application = Flask(__name__)


@application.route('/product_statistics', methods=['GET'])
def product_statistics():
    environ['SPARK_APPLICATION_PYTHON_LOCATION'] = '/app/sparky_product_statistics.py'

    result = subprocess.check_output(['/template.sh']).decode().split('SparkyIsABadBadDog!!!!!!!11111111')[1]

    return json.loads(result), 200


@application.route('/category_statistics', methods=['GET'])
def category_statistics():
    environ['SPARK_APPLICATION_PYTHON_LOCATION'] = '/app/sparky_category_statistics.py'

    result = subprocess.check_output(['/template.sh']).decode().split('SparkyIsABadBadDog!!!!!!!11111111')[1]

    return json.loads(result), 200


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5431)
