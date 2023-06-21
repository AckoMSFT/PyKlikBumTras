from flask import Flask, request

application = Flask(__name__)


@application.route("/", methods=["GET", "POST"])
def index():
    return "Hello, world!"


@application.route("/<forename>/<surname>", methods=["GET"])
def route_parameters(forename, surname):
    return "Hello {} {}".format(forename, surname)


# address:port/pathToResource?name0=value0&name1=value1&...
@application.route("/query", methods=["GET"])
def query_string():
    result = ""
    for item in request.args.items():
        result += "{}: {}<br/>".format(str(item[0]), str(item[1]))
    return result

@application.route("/request", methods=["POST"])
def request_body():
    result = ""
    for item in request.json.items():
        result += "{}: {}<br/>".format(str(item[0]), str(item[1]))
    return result

list = []
@application.route("/append/<number>", methods=["GET"])
def append(number):
    list.append(number)
    return str(list)

@application.route("/extend", methods=["POST"])
def extend():
    numbers = request.json["numbers"]
    list.extend(numbers)
    return str(list)

@application.route("/set_value", methods=["GET"])
def set_value():
    index = int(request.args["index"])
    value = int(request.args["value"])
    list[index] = value
    return str(list)

if __name__ == "__main__":
    application.run(debug=True)
