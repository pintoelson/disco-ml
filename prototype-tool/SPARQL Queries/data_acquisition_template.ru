PREFIX adr: <https://example.com/adr#>
PREFIX schema: <https://schema.org/>
PREFIX sioc_arg: <https://rdfs.org/sioc/argument#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX mops: <https://example.com//mops#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX bridge: <https://example.com/decision-bridge#>

SELECT ?g ?issue ?issueLabel ?issueBody ?issueTime ?issueAuthor ?issueAuthorName ?issueAuthorRole ?decision ?decisionLabel ?rationaleText ?costText ?riskText ?arg ?comment ?argTime ?argAuthor ?argAuthorName ?argAuthorRole ?stance ?stageClass ?asset ?assetName ?assetClass ?assetLocation
WHERE {
    {{GRAPH_FILTER}}
    GRAPH ?g {
        # Extract Issue Data
        ?issue a sioc_arg:Issue ;
               schema:name ?issueLabel ;
               adr:hasTimeStamp ?issueTime ;
               adr:hasAuthor ?issueAuthor ;
               adr:hasDescription ?descNode .
        
        ?issueAuthor schema:name ?issueAuthorName .
        ?descNode schema:text ?issueBody .
        
        # Extract Decision Data
        ?decision a schema:Decision ;
                  adr:decides ?issue .
        OPTIONAL { ?decision schema:text ?decisionLabel }
        OPTIONAL { ?decision schema:name ?decisionLabel }
                  
        OPTIONAL { ?decision adr:hasRationale ?rat . ?rat schema:text ?rationaleText }
        OPTIONAL { ?decision adr:hasCost ?cost . ?cost schema:text ?costText }
        OPTIONAL { ?decision adr:hasRisk ?risk . ?risk schema:text ?riskText }
        
        # Extract optional Arguments and their stances
        OPTIONAL {
            # Determine stance based on the property used from Decision to Argument
            { ?decision adr:agrees_with ?arg . BIND("supports" AS ?stance) }
            UNION
            { ?decision adr:disagrees_with ?arg . BIND("opposes" AS ?stance) }
            UNION
            { ?decision adr:neutral_towards ?arg . BIND("neutral" AS ?stance) }
            
            ?arg a sioc_arg:Argument ;
                 schema:text ?comment ;
                 adr:hasTimeStamp ?argTime ;
                 adr:hasAuthor ?argAuthor .
            ?argAuthor schema:name ?argAuthorName .
            
            OPTIONAL {
                ?argAuthor bridge:hasRole ?argAuthorRoleURI .
                BIND(REPLACE(STR(?argAuthorRoleURI), "^.*#", "") AS ?argAuthorRole)
            }
        }
        
        # Extract Lifecycle Activity and Stage Class
        OPTIONAL {
            ?issue prov:wasGeneratedBy ?activity .
            ?activity a ?stageClassURI .
            FILTER(STRSTARTS(STR(?stageClassURI), "https://example.com//mops#"))
            BIND(REPLACE(STR(?stageClassURI), "^.*#", "") AS ?stageClass)
        }
        
        # Extract Issue Author Role
        OPTIONAL {
            ?issueAuthor bridge:hasRole ?issueAuthorRoleURI .
            BIND(REPLACE(STR(?issueAuthorRoleURI), "^.*#", "") AS ?issueAuthorRole)
        }
        
        # Extract Main Assets
        OPTIONAL {
            ?issue prov:wasGeneratedBy ?activity .
            ?asset prov:wasGeneratedBy ?activity ;
                   schema:name ?assetName ;
                   a ?assetClassURI .
            FILTER(STRSTARTS(STR(?assetClassURI), "https://example.com//mops#"))
            BIND(REPLACE(STR(?assetClassURI), "^.*#", "") AS ?assetClass)
            OPTIONAL { ?asset mops:hasLocation ?assetLocation }
        }
    }
}