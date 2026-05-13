PREFIX : <https://example.com/adr#>
PREFIX adr: <https://example.com/adr#>
PREFIX schema: <https://schema.org/>
PREFIX sioc_arg: <https://rdfs.org/sioc/argument#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX mops: <https://example.com//mops#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX bridge: <https://example.com/decision-bridge#>

INSERT DATA {
    GRAPH <{{GRAPH_URI}}> {
        {{TRIPLES}}
    }
}
