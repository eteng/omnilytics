import flask
from flask_cors import CORS, cross_origin
from flask import request, jsonify
import json
import uuid

import rand_gen


app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Backend API Service</h1><p>This site is running.</p>"


@app.route('/api/v1/random/generate', methods=['GET'])
@cross_origin()
def api_random_generate():
    uniq = str(uuid.uuid4())
    file_name = f"tmp/{uniq}.txt"
    stats = {
        'alpha_str': 0,
        'real_num': 0,
        'ints': 0,
        'alpha_num': 0,
    }

    with open(file_name, "w") as fp:
       max_mb = 2 * 10 ** 6
       is_first = True
       
       while fp.tell() < max_mb:
           rand_obj = str(rand_gen.gen_all_rand())
           
           if rand_obj.isalpha():
               stats['alpha_str'] = stats['alpha_str'] + 1
           elif rand_obj.isdigit():
               stats['ints'] = stats['ints'] + 1
           elif rand_obj.isalnum():
               stats['alpha_num'] = stats['alpha_num'] + 1
           else:
               stats['real_num'] = stats['real_num'] + 1

           if is_first:
               fp.write(rand_obj)
               is_first = False
           else:
                fp.write(',' + rand_obj)

    with open(f"tmp/{uniq}.json", "w") as fp:
        fp.write(json.dumps(stats))

    link = "/dl-report/" + uniq + ".txt"

    return jsonify({
        'id': uniq,
        'path': link
    })

@app.route('/api/v1/report/<id>', methods=['GET'])
@cross_origin()
def generate_stats(id):

    file_name = f"tmp/{id}.json"
    with open(file_name, "r") as fp:
        stats = json.load(fp)

    
    info ={
        'alpha_str': "Alphabetical string",
        'real_num': "Real numbers",
        'ints': "Integers",
        'alpha_num': "Alphanumerics",
    }
    
    stats_info = [{'label': info[x], 'amt': v} for x, v in stats.items()]

    
    return jsonify({
        'id': id,
        'items': stats_info,
    })


@app.route('/dl-report/<path:filename>', methods=['GET'])
def download(filename):
    return flask.send_from_directory(directory='tmp', \
                filename=filename, as_attachment=True)

app.run(host='0.0.0.0')