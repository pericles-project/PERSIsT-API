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

    deletion_statements = []
    if Functions.findIfChangedByExists(delta_graph):
        # For one or more deltas produce deletion statements
        deltasAndResources = Functions.findDeltasAndChangedResourcesFromDeltaGraph(delta_graph)

        for pairDeltaResource in deltasAndResources:
            deletion_statements.append(Functions.findPredicateAndObjectCouplesFromSPECIFICDeltaForConversion(delta_graph, pairDeltaResource[1], 'deletion'))


    if len(deletion_statements) == 0:
        # print "No deletion statements in delta"
        # SPARQL_deletion_string = ""
        pass
    else:
        for statement_row in deletion_statements:
            statement = statement_row[0]
            if Functions.findIfChangedByExists(delta_graph):

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

    insertion_statements = []
    # Find insertions in delta
    if Functions.findIfChangedByExists(delta_graph):
        # For one or more deltas produce insertion statements
        deltasAndResources = Functions.findDeltasAndChangedResourcesFromDeltaGraph(delta_graph)

        # insertion_statements = []
        for pairDeltaResource in deltasAndResources:
            insertion_statements.append(Functions.findPredicateAndObjectCouplesFromSPECIFICDeltaForConversion(delta_graph, pairDeltaResource[1], 'insertion'))

    if len(insertion_statements) == 0:
        # print "No insertion statements in delta"
        # SPARQL_insertion_string = ""
        pass
    else:
        for statement_row in insertion_statements:
            statement = statement_row[0]
            if Functions.findIfChangedByExists(delta_graph):
            # In this case, statement variable is in the form of <pred, obj>

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






