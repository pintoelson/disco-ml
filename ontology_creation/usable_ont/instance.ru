PREFIX : <https://example.com/instance#>
PREFIX dd: <https://example.com/dd#>
PREFIX mlops: <https://example.com/mlops#>
PREFIX bridge: <https://example.com/decision-bridge#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sioc_arg: <https://rdfs.org/sioc/argument#>

INSERT DATA {
    # We encapsulate the ticket in its own Named Graph for versioning/traceability[cite: 1]
    GRAPH <https://example.com/graphs/ticket-12345678> {
        
        :mock_user a prov:Agent .

        # The Issue Instance[cite: 1]
        :issue_12345678 a dd:Issue ;
            rdfs:label "Mock Issue: Implement a new model architecture" ;
            dd:isAddressedBy :decision_12345678 ;
            bridge:hasAuthor :mock_user ;
            dd:hasTimeStamp "2026-05-01T10:00:00Z"^^xsd:dateTime ;
            bridge:occursInPhase mlops:ModelingTraining .

        # The Decision Instance[cite: 1]
        :decision_12345678 a dd:Decision ;
            rdfs:label "Decision: Adopt 6-layer Transformer architecture" ;
            dd:resultsFrom :issue_12345678 .

        # The MLOps Artifact Instance[cite: 1]
        :transformer_model_v1 a mlops:ModelArchitecture, prov:Entity ;
            rdfs:label "Model architecture (Transformer)" .

        # The Argument Instance[cite: 1]
        :comment_1 a dd:Argument ;
            dd:agrees_with :decision_12345678 ;
            rdfs:comment "Let's use 6 layers and a hidden dimension of 512." ;
            # dd:hasJustification "Improves results and endorses specific design parameters." ;
            dd:hasTimeStamp "2026-05-01T10:00:00Z"^^xsd:dateTime ;
            bridge:hasAuthor :mock_user .
    }
}