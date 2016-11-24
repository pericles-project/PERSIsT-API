"""
Copyright (C) 2016
MKLab http://mklab.iti.gr/
"""

__authors__ = 'Marina Riga (mriga@iti.gr)'

from rdflib import Graph
import Functions

def run(delta_stream):

    delta_graph = Graph()
    delta_graph.parse(data=delta_stream, format="turtle")

    SPARQL_deletion_string = "DELETE DATA {"
    SPARQL_insertion_string = "INSERT DATA {"

    if Functions.findIfChangedByExists(delta_graph):
        deletion_statements = Functions.findPredicateAndObjectCouplesFromDeltaForConversion(delta_graph, 'deletion')
    else:
        deletion_statements = Functions.findTriplesFromDeltaForConversion(delta_graph, 'deletion')

    if len(deletion_statements) == 0:
        # print "No deletion statements in delta"
        # SPARQL_deletion_string = ""
        pass
    else:
        for statement in deletion_statements:
            if Functions.findIfChangedByExists(delta_graph):
            # In this case, statement variable is in the form of <pred, obj>

                #Subject uri
                sub = Functions.findChangeSubjectFromDelta(delta_graph)

                # Predicate uri
                pred = statement[0]

                # Object uri
                obj = statement[1]
            else:
                # In this case, statement variable is in the form of <sub, pred, obj>

                #Subject uri
                sub = statement[0]

                # Predicate uri
                pred = statement[1]

                # Object uri
                obj = statement[2]

            #Compose string
            if "\"" in obj:
                # obj is already formed as "literal value"^^<datatype_URI>
                SPARQL_deletion_string = SPARQL_deletion_string + " <" + sub + ">" + " <" + pred + ">" + " " + obj + " ."
                # print " -- <" + sub + ">" + " <" + pred + ">" + " " + obj + " ."
            else:
                SPARQL_deletion_string = SPARQL_deletion_string + " <" + sub + ">" + " <" + pred + ">" + " <" + obj + "> ."
                # print " <" + sub + ">" + " <" + pred + ">" + " <" + obj + "> ."

    SPARQL_deletion_string = SPARQL_deletion_string + " }"

    # print SPARQL_deletion_string

    # Find insertions in delta
    if Functions.findIfChangedByExists(delta_graph):
        insertion_statements = Functions.findPredicateAndObjectCouplesFromDeltaForConversion(delta_graph, 'insertion')
    else:
        insertion_statements = Functions.findTriplesFromDeltaForConversion(delta_graph, 'insertion')

    if len(insertion_statements) == 0:
        # print "No insertion statements in delta"
        # SPARQL_insertion_string = ""
        pass
    else:
        for statement in insertion_statements:
            if Functions.findIfChangedByExists(delta_graph):
            # In this case, statement variable is in the form of <pred, obj>

                #Subject uri
                sub = Functions.findChangeSubjectFromDelta(delta_graph)

                # Predicate uri
                pred = statement[0]

                # Object uri
                obj = statement[1]

            else:
            # In this case, statement variable is in the form of <sub, pred, obj>

                #Subject uri
                sub = statement[0]

                # Predicate uri
                pred = statement[1]

                # Object uri
                obj = statement[2]

            #Compose string
            if "\"" in obj:
                # obj is already formed as "literal value"^^<datatype_URI>
                SPARQL_insertion_string = SPARQL_insertion_string + " <" + sub + ">" + " <" + pred + ">" + " " + obj + " ."
                # print " -- <" + sub + ">" + " <" + pred + ">" + " " + obj + " ."
            else:
                SPARQL_insertion_string = SPARQL_insertion_string + " <" + sub + ">" + " <" + pred + ">" + " <" + obj + "> ."
                # print " <" + sub + ">" + " <" + pred + ">" + " <" + obj + "> ."

    SPARQL_insertion_string = SPARQL_insertion_string + " }"

    # print SPARQL_insertion_string
    SPARQL_total = {}

    SPARQL_total['SPARQL_delete'] = SPARQL_deletion_string
    SPARQL_total['SPARQL_insert'] = SPARQL_insertion_string

    return SPARQL_total






