PREFIX adr: <https://example.com/adr#>
PREFIX schema: <https://schema.org/>
PREFIX sioc_arg: <https://rdfs.org/sioc/argument#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?g ?issue ?issueLabel ?issueTime ?issueAuthor ?issueAuthorName ?decision ?decisionLabel ?rationale ?arg ?comment ?argTime ?argAuthor ?argAuthorName ?stance
WHERE {
    # Extract Issue Data
    ?issue a sioc_arg:Issue ;
           adr:hasTimeStamp ?issueTime ;
           adr:hasAuthor ?issueAuthor ;
           adr:hasDescription ?descNode .
    
    ?issueAuthor schema:name ?issueAuthorName .
    ?descNode schema:text ?issueLabel .
    
    # Extract Decision Data
    ?decision a schema:Decision ;
              adr:decides ?issue ;
              schema:name ?decisionLabel ;
              schema:text ?rationale .
    
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