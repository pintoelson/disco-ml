PREFIX adr: <https://example.com/adr#>
PREFIX schema: <https://schema.org/>
PREFIX sioc_arg: <https://rdfs.org/sioc/argument#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?g ?issue ?issueLabel ?issueBody ?issueTime ?issueAuthor ?issueAuthorName ?decision ?decisionLabel ?rationaleText ?costText ?riskText ?arg ?comment ?argTime ?argAuthor ?argAuthorName ?stance
WHERE {
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
        ?arg a sioc_arg:Argument ;
             schema:about ?decision ;
             schema:text ?comment ;
             adr:hasTimeStamp ?argTime ;
             adr:hasAuthor ?argAuthor .
        ?argAuthor schema:name ?argAuthorName .
        
        # Determine stance based on the property used from Decision to Argument
        { ?decision adr:agrees_with ?arg . BIND("supports" AS ?stance) }
        UNION
        { ?decision adr:disagrees_with ?arg . BIND("opposes" AS ?stance) }
        UNION
        { ?decision adr:neutral_towards ?arg . BIND("neutral" AS ?stance) }
    }
}