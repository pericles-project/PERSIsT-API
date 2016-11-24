"""
Copyright (C) 2016
MKLab http://mklab.iti.gr/
"""

__authors__ = 'Marina Riga (mriga@iti.gr), Panagiotis Mitzias (pmitzias@iti.gr)'


import Functions
from Functions import Tree
from rdflib import Graph, URIRef

def run(repository, delta_stream):

    ERMR_URL_for_repository = "https://141.5.100.67/api/triple/" + repository + "/statements"
    my_graph = Functions.loadOntologyFromERMRToGraph(ERMR_URL_for_repository)

    delta_graph = Graph()
    delta_graph.parse(data=delta_stream, format="turtle")

    main_dictionary = {}
    main_dictionary['action'] = 'update'

    # Find deletions in delta
    if Functions.findIfChangedByExists(delta_graph):
        deletion_statements = Functions.findPredicateAndObjectCouplesFromDelta(delta_graph, 'deletion')
    else:
        deletion_statements = Functions.findTriplesFromDelta(delta_graph, 'deletion')

    if len(deletion_statements) == 0:
        main_dictionary['action'] = 'insertion'
        main_dictionary['deletions'] = []
    else:
        deletion_dictionary_list = []

        # For each deletion, produce a Tree
        for statement in deletion_statements:

            if Functions.findIfChangedByExists(delta_graph):
                # In this case, statement variable is in the form of <pred, obj>

                # Object uri
                obj = statement[1]

                # Predicate uri
                pred = statement[0]

                # Get dictionary of tree
                obj_dictionary = (Tree(my_graph, URIRef(obj))).dictionary

                obj_dictionary['action'] = 'deletion'
                obj_dictionary['subject'] = Functions.findChangeSubjectFromDelta(delta_graph)
                obj_dictionary['predicate'] = pred
                obj_dictionary['object'] = obj

                deletion_dictionary_list.append(obj_dictionary)
            else:
                # In this case, statement variable is in the form of <sub, pred, obj>

                # Object uri
                obj = statement[2]

                # Predicate uri
                pred = statement[1]

                # Get dictionary of tree
                obj_dictionary = (Tree(my_graph, URIRef(obj))).dictionary

                obj_dictionary['action'] = 'deletion'
                obj_dictionary['subject'] = statement[0]
                obj_dictionary['predicate'] = pred
                obj_dictionary['object'] = obj

                deletion_dictionary_list.append(obj_dictionary)


        main_dictionary['deletions'] = deletion_dictionary_list

    # Find insertions in delta
    if Functions.findIfChangedByExists(delta_graph):
        insertion_statements = Functions.findPredicateAndObjectCouplesFromDelta(delta_graph, 'insertion') # TODO: we need subject predicate and object in case where changedby does not exist
    else:
        insertion_statements = Functions.findTriplesFromDelta(delta_graph, 'insertion')

    if len(insertion_statements) == 0:
        main_dictionary['action'] = 'deletion'
        main_dictionary['insertions'] = []

    else:
        # Perform changes in my graph
        my_graph = Functions.applyDeltaChangesToGraph(my_graph, delta_graph)

        insertion_dictionary_list = []

        # For each deletion, produce a Tree
        for statement in insertion_statements:

            if Functions.findIfChangedByExists(delta_graph):
                # In this case, statement variable is in the form of <pred, obj>

                # Object uri
                obj = statement[1]

                # Predicate uri
                pred = statement[0]

                # Get dictionary of tree
                obj_dictionary = (Tree(my_graph, URIRef(obj))).dictionary

                obj_dictionary['action'] = 'insertion'
                obj_dictionary['subject'] = Functions.findChangeSubjectFromDelta(delta_graph)
                obj_dictionary['predicate'] = pred
                obj_dictionary['object'] = obj

                insertion_dictionary_list.append(obj_dictionary)
            else:
                # In this case, statement variable is in the form of <sub, pred, obj>

                # Object uri
                obj = statement[2]

                # Predicate uri
                pred = statement[1]

                # Get dictionary of tree
                obj_dictionary = (Tree(my_graph, URIRef(obj))).dictionary

                obj_dictionary['action'] = 'insertion'
                obj_dictionary['subject'] = statement[0]
                obj_dictionary['predicate'] = pred
                obj_dictionary['object'] = obj

                insertion_dictionary_list.append(obj_dictionary)

        main_dictionary['insertions'] = insertion_dictionary_list


    return main_dictionary