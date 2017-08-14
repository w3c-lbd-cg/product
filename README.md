# PRODUCT: Building Product Ontology

## Version control
The latest version is available from w3id.org/product#. This points to the master branch of this repository.
Developments are stored in the Development branch and feature branches are created for features that are not yet implemented in the development branch.

## Adding content to PRODUCT
1. Fork this repository. 
2. Add contribution to product or separate alignment file.
3. Commit your changes and submit a [pull request](https://github.com/perma-id/w3id.org/pulls).
4. w3c-lbd administrators will review your pull request and merge it if everything looks correct. Once the pull request is merged, the changes go live immediately.

## Example of using PRODUCT

Example of using PRODUCT in [Turtle syntax](https://www.w3.org/TeamSubmission/turtle/).
```turtle
@prefix bot:  <https://w3id.org/bot#> .
@prefix product:  <https://w3id.org/product#> .
@prefix inst: <https://example.org/projectXX/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

inst:buildingA a bot:Building ;
               bot:hasStorey inst:storey00 ,
                             inst:storey01 .
							 
inst:storey00 a bot:Storey ;
              bot:hasSpace inst:space00aa ,
                           inst:space00cg .
						   
inst:storey01 a bot:Storey .

inst:space00aa a bot:Space ;
               bot:containsElement inst:heater235 .
               bot:adjacentElement inst:wall443 ,
                                   inst:wall769 .
                                   inst:wall209 .
                                   inst:floor23 .
								   
inst:space00cg a bot:Space .
inst:heater235 a product:Heater .
inst:wall443 a product:Wall .
inst:wall769 a product:Wall .
inst:wall209 a product:Wall .
inst:floor23 a product:Floor .
```
specifying classes is not necessary as these are inferred by the domain and range specified in the ontology.

## Extending PRODUCT
### By specifying subclasses
The following will automatically infer that an instance arch:MySpecialCurtainWall is a product:Product and by consequence also a bot:Element given that the instance is specified as a product:CutainWall.
```turtle
@prefix product:  <https://w3id.org/product#> .
@prefix arch:  <https://example.org/architecture#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .

arch:MySpecialCurtainWall a owl:Class ;
              rdfs:subClassOf product:CurtainWall .
```
### By specifying subproperties
The following will automatically infer bot:adjacentElement between a space and an element when the arch:hasFacadeSystem property is present between the two. Furthermore it will be inferred that the element is an arch:MySpecialCurtainWall, a product:CurtainWall, a product:Product and a bot:Element.
```turtle
@prefix product:  <https://w3id.org/product#> .
@prefix arch:  <https://example.org/architecture#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .

arch:MySpecialCurtainWall a owl:Class .
arch:hasFacadeSystem a owl:ObjectProperty ;
             rdfs:subPropertyOf bot:adjacentElement ;
             rdfs:range arch:MySpecialCurtainWall .
```
