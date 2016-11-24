"""
Copyright (C) 2016
MKLab http://mklab.iti.gr/
"""

__authors__ = 'Marina Riga (mriga@iti.gr)'

import ConvertDeltaToSPARQL
import ConvertMultipleDeltasToSPARQL
import CreateDependencyTreesForDelta
import Functions

from flask import Flask, jsonify
from flask import request, abort

app = Flask(__name__)

@app.route("/api")
def root():
    return 'PERSIsT API is running...'


@app.route("/api/conversion", methods = ['POST'])
# conversion from delta to SPARQL should take
# as POST parameter:
        # a delta_stream
        # an ERMR_repository
def runConversionOfDeltaToSPARQL():

    apply_to_ERMR = False

    if not request.json:
        abort(400)
    if ('delta_stream' or 'ERMR_repository') not in request.json :
        abort(400)

    SPARQL_total=''
    delta_path = ''
    ERMR_repository = ''

    if 'delta_stream' in request.get_json():
        delta_path = request.get_json()['delta_stream']

    if 'ERMR_repository' in request.get_json():
        ERMR_repository = request.get_json()['ERMR_repository']

    if delta_path != '' and ERMR_repository !='':
        SPARQL_total = ConvertDeltaToSPARQL.run(delta_path)

    if SPARQL_total == '':
        abort(400)
    elif (ERMR_repository != '' and apply_to_ERMR):
        delete_query = SPARQL_total['SPARQL_delete']
        insert_query = SPARQL_total['SPARQL_insert']
        req_del = Functions.simple_update_repository(delete_query, ERMR_repository)
        req_ins = Functions.simple_update_repository(insert_query, ERMR_repository)

    return jsonify(SPARQL_total)


@app.route("/api/conversion_multiple_deltas", methods = ['POST'])
# conversion from multiple deltas to SPARQL should take
# as POST parameter:
        # a delta_stream with multiple deltas
        # an ERMR_repository
def runConversionOfMultipleDeltasToSPARQL():

    apply_to_ERMR = False

    if not request.json:
        abort(400)
    if ('delta_stream' or 'ERMR_repository') not in request.json :
        abort(400)

    SPARQL_total=''
    delta_path = ''
    ERMR_repository = ''

    if 'delta_stream' in request.get_json():
        delta_path = request.get_json()['delta_stream']

    if 'ERMR_repository' in request.get_json():
        ERMR_repository = request.get_json()['ERMR_repository']

    if delta_path != '' and ERMR_repository !='':
        SPARQL_total = ConvertMultipleDeltasToSPARQL.run(delta_path)

    if SPARQL_total == '':
        abort(400)
    elif (ERMR_repository != '' and apply_to_ERMR):
        # call ERMR to apply delete and update queries
        delete_query = SPARQL_total['SPARQL_delete']
        insert_query = SPARQL_total['SPARQL_insert']
        req_del = Functions.simple_update_repository(delete_query, ERMR_repository)
        req_ins = Functions.simple_update_repository(insert_query, ERMR_repository)

    return jsonify(SPARQL_total)

@app.route("/api/dependency_graph", methods = ['POST'])
# in order to return the dependency graph the API should take
# as POST parameter:
        # a delta_stream and
        # an ERMR_repository
def runCreateDependencyGraph():

    delta_path = ''
    ERMR_repository = ''

    if ('delta_stream' or 'ERMR_repository') not in request.json :
        abort(400)

    if 'delta_stream' in request.get_json():
        delta_path = request.get_json()['delta_stream']
    if 'ERMR_repository' in request.get_json():
        ERMR_repository = request.get_json()['ERMR_repository']

    if delta_path != '' and ERMR_repository !='':
        dependency_graph = CreateDependencyTreesForDelta.run(ERMR_repository, delta_path)
        return jsonify(dependency_graph)
    else:
        abort(400)

if __name__ == "__main__":
    app.run()
    # app.run(host='0.0.0.0')
