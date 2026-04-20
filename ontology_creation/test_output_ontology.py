import sys
import pathlib
import rdflib
from pyshacl import validate
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def check_syntax(file_path: pathlib.Path):
    """Attempt to parse the TTL file with rdflib."""
    # Use oxigraph store if available for RDF-star support
    try:
        g = rdflib.Graph(store="oxigraph")
        logger.info("Using oxigraph store for RDF-star support.")
    except Exception:
        g = rdflib.Graph()
        logger.warning("Oxigraph store not found or failed to init. Falling back to default Memory store.")
        
    try:
        g.parse(file_path, format="ox-turtle")
        logger.info(f"âœ… Syntactic Check Passed: {file_path.name}")
        return g
    except Exception as e:
        logger.error(f"â Œ Syntactic Check Failed: {file_path.name}")
        # Extract line number from rdflib exception if possible
        error_msg = str(e)
        logger.error(f"Error Detail: {error_msg}")
        return None

def check_shacl_constraints(data_graph, shapes_file: pathlib.Path):
    """Validate data graph against SHACL shapes."""
    if data_graph is None:
        return
        
    # Create a SHACL-safe graph (Memory store) by filtering out triple-term tuples
    # which pyshacl's internal cloning doesn't support.
    shacl_safe_graph = rdflib.Graph()
    for s, p, o in data_graph:
        if isinstance(s, tuple) or isinstance(o, tuple):
            continue
        shacl_safe_graph.add((s, p, o))
        
    shapes_graph = rdflib.Graph()
    shapes_graph.parse(shapes_file, format="turtle")
    
    conforms, results_graph, results_text = validate(
        shacl_safe_graph,
        shacl_graph=shapes_graph,
        inference='rdfs',
        abort_on_first=False,
        allow_warnings=False,
        meta_shacl=False,
        advanced=True,
        js=False,
        debug=False
    )
    
    if conforms:
        logger.info(f"âœ… SHACL Validation Passed: {shapes_file.name}")
    else:
        logger.error(f"â Œ SHACL Validation Failed: {results_text}")

def explain_inconsistency_detection():
    """Explain how to interface with reasoners like HermiT."""
    explanation = """
### Inconsistency Detection with Reasoners (e.g., HermiT)

To check for disjoint class violations or logical inconsistencies (e.g., an entity being both a 'Human' and a 'Machine' where classes are disjoint):

1. **Standalone Reasoners (Desktop)**: Use ProtÃ©gÃ© with the HermiT plugin. Load your .ttl file, start the reasoner, and it will highlight inconsistent nodes in red.
2. **Python Integration (Owlready2)**:
   - Install: `pip install owlready2`
   - Code snippet:
     ```python
     from owlready2 import *
     onto = get_ontology("file://path/to/ontology.ttl").load()
     with onto:
         sync_reasoner_hermit(infer_property_values=True)
     ```
   - This will raise an `OwlReadyInconsistencyError` if disjointness or cardinality constraints are violated.
3. **SPARQL-based checking**: You can also write manual SPARQL queries to detect known 'impossible' patterns if you don't want to run a full reasoner.
    """
    print(explanation)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_output_ontology.py <path_to_ontology.ttl>")
        sys.exit(1)
        
    target_file = pathlib.Path(sys.argv[1])
    constraints_file = pathlib.Path("constraints.shacl.ttl")
    
    # 1. Syntactic Check
    graph = check_syntax(target_file)
    
    # 2. Structural Validation (SHACL)
    if constraints_file.exists():
        check_shacl_constraints(graph, constraints_file)
    else:
        logger.warning("constraints.shacl.ttl not found, skipping SHACL validation.")
        
    # 3. Inconsistency Detection Explanation
    explain_inconsistency_detection()
