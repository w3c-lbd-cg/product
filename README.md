# PRODUCT: Building Product Ontology

This branch contains a proposal for a novel lightweight building product ontology. The ontology only contains two classes and two object properties. The ontology is aligned to BOT and to schema.org.

Example of PRODUCT in [Turtle syntax](https://www.w3.org/TeamSubmission/turtle/).
```turtle
# Copyright 2017 W3C Linked Building Data Community Group.
# 
# This work is licensed under a Creative Commons Attribution License. 
# This copyright applies to the PRODUCT Vocabulary Specification and
# accompanying documentation in RDF. Regarding underlying technology,
# PRODUCT uses W3C's RDF technology, an open Web standard that can be freely 
# used by anyone.

@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl:    <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms:<http://purl.org/dc/terms/> .
@prefix vann:   <http://purl.org/vocab/vann/> .
@prefix voaf:   <http://purl.org/vocommons/voaf#> .
@prefix vs:     <http://www.w3.org/2003/06/sw-vocab-status/ns#> .
@prefix foaf:   <http://xmlns.com/foaf/0.1/> .
@prefix dce:    <http://purl.org/dc/elements/1.1/> .
@prefix dbo:    <http://dbpedia.org/ontology/> .
@prefix bot:    <https://w3id.org/bot#> .
@prefix schema: <http://schema.org/> .


@prefix prod: <https://w3id.org/product#> .
@base <https://w3id.org/product> .


#################################
# METADATA
#################################
<https://w3id.org/product> rdf:type voaf:Vocabulary , 
                                 owl:Ontology ;
    dcterms:title "PRODUCT: The building product ontology "@en ;
    dcterms:description """The PRODUCT Ontology (PRODUCT) extends the Building Topology Ontology (BOT) with more specific building elements."""@en ;
    dcterms:creator [a foaf:Person ; foaf:name "Mads Holten Rasmussen" ] ;
    dcterms:creator [a foaf:Person ; foaf:name "Pieter Pauwels" ] ;
    dcterms:creator [a foaf:Person ; foaf:name "Georg Ferdinand Schneider" ] ;
    dcterms:contributor [a foaf:Person ; foaf:name "Maxime Lefrançois" ] ;
    dcterms:contributor [a foaf:Person ; foaf:name "Gonçal Costa" ] ;
    #dcterms:contributor [a foaf:Person ; foaf:name "" ] ;
    dcterms:license <https://creativecommons.org/licenses/by/1.0/> ;
    vann:preferredNamespacePrefix "prod" ;
    vann:preferredNamespaceUri <https://w3id.org/product#> ;
    dce:Language "en" ;
    dce:title "PRODUCT a ontology for building products" ;
    dce:description "Products in the AEC industry" .
     
#################################
# CLASSES
#################################
prod:Product a owl:Class ;
        rdfs:subClassOf bot:Element ,
                        schema:Product ;
        rdfs:label      "Product"@en ;
        rdfs:comment    "A product is an article or substance that is manufactured or refined for sale"@en .
						
prod:Property a owl:Class ;
        rdfs:subClassOf schema:Property ;
        rdfs:label      "Property"@en ;
        rdfs:comment    "A instance of a property of a product. Usually only a blind node."@en .                        
                        
#################################
# OBJECT PROPERTIES
#################################

prod:aggregates a owl:ObjectProperty ;
        rdfs:domain prod:Product ;
        rdfs:range prod:Product ;
        rdfs:label "aggregates"@en ;
        rdfs:comment "Object property to describe the composition of a product which is aggregated from several sub products."@en .

prod:hasProperty a owl:ObjectProperty ;
        rdfs:subPropertyOf schema:additionalProperty ;
        rdfs:domain prod:Product ;
        rdfs:range prod:Property ;
        rdfs:label "hasProperty"@en ;
rdfs:comment "Generic super property which can be specified depending on the respective needs of a product ontology."@en . 
```



## Extending PRODUCT ontology

The preferred way to extend from PRODUCT ontology is through inheritance (rdfs:subClassof/ rdfs:subPropertyOf).

# Product 4 Building ontology

As one taxonomy to further specify PRODUCT ontology we propose the P4Bldg ontology. A taxonomy for products which had been derived from ifcOWL4Add2 using the included python script.

Exerpt of using P4Bldg in [Turtle syntax](https://www.w3.org/TeamSubmission/turtle/).
```turtle
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ifc: <http://www.buildingsmart-tech.org/ifcOWL/IFC4_ADD2#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix p4bldg: <http://w3id.org/lbd/Product4BuildingOntology#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://w3id.org/lbd/Product4BuildingOntology> a owl:Ontology ;
    dcterms:contributor "Mads Holten Rasmussen"^^xsd:string ;
    dcterms:creator <https://www.researchgate.net/profile/Georg_Schneider3>,
        "Georg Ferdinand Schneider"^^xsd:string,
        "Pieter Pauwels"^^xsd:string ;
    dcterms:description "This ontology provides a taxonomy for product elements in a building. It has been created from the ifcOWL4Add2 OWL ontology."^^xsd:string ;
    dcterms:license <http://creativecommons.org/licenses/by-sa/4.0> ;
    dcterms:title "The Product 4 building ontology."^^xsd:string ;
    owl:imports <https://w3id.org/product> .

p4bldg:Actuator-ELECTRICACTUATOR a owl:Class ;
    rdfs:label "ELECTRICACTUATOR"^^xsd:string ;
    rdfs:comment "Describe products of class ELECTRICACTUATOR a specialisation of Actuator"^^xsd:string ;
    rdfs:seeAlso ifc:IfcActuatorEnumType ;
    rdfs:subClassOf p4bldg:Actuator .

p4bldg:Actuator-HANDOPERATEDACTUATOR a owl:Class ;
    rdfs:label "HANDOPERATEDACTUATOR"^^xsd:string ;
    rdfs:comment "Describe products of class HANDOPERATEDACTUATOR a specialisation of Actuator"^^xsd:string ;
    rdfs:seeAlso ifc:IfcActuatorEnumType ;
rdfs:subClassOf p4bldg:Actuator .

```

