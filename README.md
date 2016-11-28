# PERSIsT-API
PERICLES Semantic Interpretation API (PERSIsT API) serves as an intermediate module capable of achieving high level communication between the ERMR and the related PERICLES components (WE, MICE, SPIN rule Engine, LMR-S). This service can operate as a semantic interpretation (translation layer) of the ontology stored in the ERMR.

Description
-------------
The main purpose of PERSIsT API is to serve as an intermediate layer between the ERMR and other involved PERICLES components, so as to achieve the semantic interpretation of the ontology stored in the triple store. Standard SPARQL queries are handled by the ERMR; what the PERSIsT API does is that it combines complex SPARQL queries, and creates their sequence, so as to interpret and retrieve the required information from the repository. 

Two main LRM notions should be adopted in the ontology representation in order for the PERSIsT API to be functional: the *lrm:Dependency* and *lrm:RDF-Delta*. 

Features
-----------
In its current state, PERSIsT handles two main tasks: (a) the creation of dependency graphs, and (b) the manipulation and interpretation of lrm-deltas. For these, PERSIsT API offers the following web services:
* http://persist.iti.gr:5000/api/dependency_graph - with an HTTP POST request, a dependency graph can be created, regarding the changed resource described in a delta stream. 
* http://persist.iti.gr:5000/api/conversion - with an HTTP POST request, a SPARQL UPDATE query is created and applied to the ERMR repository, regarding the change described in a delta stream. 
* http://persist.iti.gr:5000/api/conversion_multiple_deltas - similarily to the previous one, apart from the fact that this service hanldes multiple deltas existing in one delta stream. 

For more details and examples, see [documentation link](https://goo.gl/jPY0zU).

Requirements
---------------
PERSIsT API is implemented in [Python 2.7](https://www.python.org/download/releases/2.7/).
External Python libraries ([RDFLib](http://rdflib.readthedocs.io/en/stable/gettingstarted.html), [Requests](http://docs.python-requests.org/en/master/), and [Flask](http://flask.pocoo.org/)) should be already installed into your computer. 

Instructions
--------------
1. Install **Python 2.7** and external python libraries, from which PERSIsT API depends on.
2. Clone the project locally in your computer.
3. Open command prompt and change directory to the local path of the stored project:
    ``` cd "C:\your_path_to_project" ```
4. Run MainAPIFunctions.py through the command:
    ``` "C:\your_path_to_python27_library\python.exe" MainAPIFunctions.py ``` 
    As a result, the PERSIsT API will be **up and running locally**. The **base URL** for the API is http://127.0.0.1:5000/api
5. Create a script on any preffered language or run curl commands to make **POST calls** to PERSIsT API (for more detailed examples, see [documentation link](https://goo.gl/jPY0zU))  


Documentation
--------------
A short documentation of PERSIsT API is [here](https://goo.gl/jPY0zU).

Credits
-------------
PERSIsT API was created by <a href="http://mklab.iti.gr/" target="_blank">MKLab group</a> under the scope of <a href="http://pericles-project.eu/" target="_blank">PERICLES</a> FP7 Research Project.

![mklab logo](http://mklab.iti.gr/prophet/_static/mklab_logo.png)  ![pericles logo](http://mklab.iti.gr/prophet/_static/pericles_logo.png)
