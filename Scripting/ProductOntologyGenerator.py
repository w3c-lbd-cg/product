# -*- coding: utf-8 -*-
"""
    Python script to generate product 4 building ontology.
       
    Copyright (C) by Georg Ferdinand Schneider
      
    Created by:
    Georg Ferdinand Schneider
    georg.schneider@ibp.fraunhofer.de

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   
# required package import
import os # working directory etc
import requests # http requests for queries
import time # logs with time
from rdflib import Graph , RDF , URIRef , Literal , XSD
from rdflib import Namespace as nmp

###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   
# Global vars

dNameSpaces = { u"p4bldg"       : u"http://w3id.org/lbd/Product4BuildingOntology#" ,
                u"ifc"          : u"http://www.buildingsmart-tech.org/ifcOWL/IFC4_ADD2#" ,
                u"owl"          : u"http://www.w3.org/2002/07/owl#" ,
                u"rdf"          : u"http://www.w3.org/1999/02/22-rdf-syntax-ns#" ,
                u"rdfs"         : u"http://www.w3.org/2000/01/rdf-schema#" ,
                u"dcterms"      : u"http://purl.org/dc/terms/" ,
                u"xsd"          : u"http://www.w3.org/2001/XMLSchema#" }


def cutPrefix( prefix , strToBeCut ):
    '''Function to cut off prefixes in URIs'''
    if strToBeCut.startswith( prefix ):
        return strToBeCut[ len( prefix ) : ]
    else:
        return strToBeCut

def sendQuery( strEndpointAddress , strQueryType , strQuery ):
    '''
    Function to send a SPARQL query via http to a SPARQL endpoint
    returns results from query in JSON format
    strEndpointAddress - http address of SPARQL endpoint
    strQueryType - Type of sparql query either query or update
    strQuery - string specifiing the sparql query
    '''
    r = requests.post( strEndpointAddress + strQueryType , data={ strQueryType : strQuery } )
    # check http status code of query
    if r.status_code != 200:
        print time.strftime('>[%Y-%m-%d %H:%M:%S]') , ' ERROR:' , '\t' , 'HTTP communication error: ' + '200 ' + strEndpointAddress
        print time.strftime('>[%Y-%m-%d %H:%M:%S]') , ' ERROR:' , '\t' , 'ERROR | The query sent was: '
        strQuery = strQuery[:400] # limit output
        print time.strftime('>[%Y-%m-%d %H:%M:%S]') , ' ERROR:' , '\t' , 'ERROR | ' + strQuery
    else:
        print time.strftime('>[%Y-%m-%d %H:%M:%S]') , ' LOG:' , '\t' , 'Communication worked fine with : '
        print time.strftime('>[%Y-%m-%d %H:%M:%S]') , ' LOG:' , '\t' , strEndpointAddress
        if strQueryType == 'query':    
            return r.json()
            parsed_json = r.json()
            if ( len( parsed_json[ 'results' ][ 'bindings' ]) == 0 ):
                print time.strftime('>[%Y-%m-%d %H:%M:%S]') , ' ERROR:' , '\t' , 'No results found on SPARQL endpoint'
        elif strQueryType == 'update':
            print time.strftime('>[%Y-%m-%d %H:%M:%S]') , ' LOG:' , '\t' , 'Update worked fine'
            
def getProducts( strEndpointAddress ):
    '''
    Function queries for all sub classes of IfcElement
    '''
    d = { } 
    
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ifc: <http://www.buildingsmart-tech.org/ifcOWL/IFC4_ADD2#>
    
    SELECT ?aProduct ?ItsSubClass
    WHERE {
      ?aProduct rdfs:subClassOf* ifc:IfcElement .
      OPTIONAL{ ?ItsSubClass rdfs:subClassOf ?aProduct }
      
    }
    """
        
    res = sendQuery( strEndpointAddress , 'query' , query )
   
    for j in range( len( res[ 'results' ][ 'bindings' ] ) ):
        aProduct = cutPrefix( dNameSpaces[ u"ifc" ] , res[ 'results' ][ 'bindings' ][ j ][ res[ 'head' ][ 'vars' ][ 0 ] ][ 'value' ] )
        if len( res[ 'results' ][ 'bindings' ][ j ] ) > 1:
            itsSubClassOf = cutPrefix( dNameSpaces[ u"ifc" ] ,  res[ 'results' ][ 'bindings' ][ j ][ res[ 'head' ][ 'vars' ][ 1 ] ][ 'value' ] )
        else:
            itsSubClassOf = "None"
        seeAlso = res[ 'results' ][ 'bindings' ][ j ][ res[ 'head' ][ 'vars' ][ 0 ] ][ 'value' ]
        
        d[ str( j ) ] = ( aProduct , itsSubClassOf , seeAlso  )
    return d 



def initRDF():
    """
    Function to initialise a Graph using rdflib API
    """
    g = Graph()
    
    # Register namespaces                    
    for n in dNameSpaces:
        aNS = nmp( dNameSpaces[ n ] )
        g.bind( n , aNS )
    return g , dNameSpaces

def saveRdf( g , fileName ):
    """
    Function to save generated RDF graph to file.
    """
    g.serialize( destination = fileName , format = "turtle" )


def genRDF( g , strEndpointAddress ):
    """
    Function to create product 4 building ontology
    from IFC taxonomy
    """
    # Retrieve all subclasses of IfcElement
    d = getProducts( strEndpointAddress )
    
    # Ontology annotation
    s = URIRef( dNameSpaces[ "p4bldg" ].replace( "#" , "" ) )
    o = URIRef( dNameSpaces[ "owl" ] + "Ontology" )
    g.add( ( s , RDF.type , o ) )
    p = URIRef( dNameSpaces[ "owl" ] + "imports" )
    o = URIRef( u"https://w3id.org/product" )
    g.add( ( s , p , o ) )
    p = URIRef( dNameSpaces[ "dcterms" ] + "creator" )
    o = URIRef( "https://www.researchgate.net/profile/Georg_Schneider3" )
    g.add( ( s , p , o ) )
    p = URIRef( dNameSpaces[ "dcterms" ] + "creator" )
    o = Literal( "Georg Ferdinand Schneider" , datatype = XSD.string )
    g.add( ( s , p , o ) )
    p = URIRef( dNameSpaces[ "dcterms" ] + "creator" )
    o = Literal( "Pieter Pauwels" , datatype = XSD.string )
    g.add( ( s , p , o ) )
    p = URIRef( dNameSpaces[ "dcterms" ] + "contributor" )
    o = Literal( "Mads Holten Rasmussen" , datatype = XSD.string )
    g.add( ( s , p , o ) )
    o = URIRef( "https://www.researchgate.net/profile/Georg_Schneider3" )
    o1 = URIRef( dNameSpaces[ "owl" ] + "NamedIndividual" )
    g.add( ( o , RDF.type , o1 ) )
    p = URIRef( dNameSpaces[ "dcterms" ] + "description" )
    o = Literal( u"""This ontology provides a taxonomy for product elements in a building. It has been created from the ifcOWL4Add2 OWL ontology.""" , datatype = XSD.string )
    g.add( ( s , p , o ) )
    p = URIRef( dNameSpaces[ "dcterms" ] + "title" )
    o = Literal( u"""The Product 4 building ontology.""" , datatype = XSD.string )
    g.add( ( s , p , o ) )
    p = URIRef( dNameSpaces[ "dcterms" ] + "license" )
    o = URIRef( u"http://creativecommons.org/licenses/by-sa/4.0" )
    g.add( ( s , p , o ) )
    
    # Align to PRODUCT ontology
    s = URIRef( dNameSpaces[ "p4bldg" ] + "Element" )
    p = URIRef( dNameSpaces[ "rdfs" ] + "subClassOf" )
    o = URIRef( u"https://w3id.org/product#Product" )
    g.add( ( s , p , o ) )
        
    # Create new taxonomy from original class hierachy
    for key , value in d.iteritems():
        # Owl class
        s = URIRef( dNameSpaces[ "p4bldg" ] + value[ 0 ].replace( "Ifc" , "" ) )
        o = URIRef( dNameSpaces[ "owl" ] + "Class" )
        g.add( ( s , RDF.type , o ) )
        # Label
        p = URIRef( dNameSpaces[ "rdfs" ] + "label" )
        o = Literal( value[ 0 ].replace( "Ifc" , "" ) , datatype = XSD.string)
        g.add( ( s , p , o ) )
        # Comment
        p = URIRef( dNameSpaces[ "rdfs" ] + "comment" )
        o = Literal( "Describe products of class " + value[ 0 ].replace( "Ifc" , "" ) , datatype = XSD.string)
        g.add( ( s , p , o ) )
        # subClassOf
        s1 = URIRef( dNameSpaces[ "p4bldg" ] + value[ 1 ].replace( "Ifc" , "" ) )
        p = URIRef( dNameSpaces[ "rdfs" ] + "subClassOf" )
        if value[ 1 ] != "None":
            g.add( ( s1 , p , s ) )
        # leaves as Classes
        o = URIRef( dNameSpaces[ "owl" ] + "Class" )
        g.add( ( s1 , RDF.type , o ) )
        # seeAlso
        p = URIRef( dNameSpaces[ "rdfs" ] + "seeAlso" )
        o = URIRef( value[ 2 ] )
        g.add( ( s , p , o ) )
        
    return g
        
def getEnumTypes( g , strEndpointAddress , pre ):
    """
    Function to generate Subclasses of enumtypes
    can be seen as leaves below IfcElement taxonomy.
    """
    strGetClasses = u"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX p4bldg: <http://w3id.org/lbd/Product4BuildingOntology#>
    SELECT ?aClass
    WHERE {
      ?aClass rdf:type owl:Class . 
    }
    """
        
    # Query all generated classes in local rdf store g
    lClasses = g.query( strGetClasses )
    
       
    strGetEnumType = u"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ifc: <http://www.buildingsmart-tech.org/ifcOWL/IFC4_ADD2#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?ItsSubClass
    WHERE {
      ?ItsSubClass rdf:type ifc:Ifc$CLASSNAME$TypeEnum . 
    }
    """
    
    for row in lClasses:
        # query for each subclass if there is enumtype instances
        aClass = row.aClass.replace( dNameSpaces[ u"p4bldg" ] , u"" )
            
        query = strGetEnumType.replace( "$CLASSNAME$" , aClass )
    
        res = sendQuery( strEndpointAddress , 'query' , query )
        
        # Check if there is instances
        if len( res[ 'results' ][ 'bindings' ] ) != 0:
            for j in range( len( res[ 'results' ][ 'bindings' ] ) ):
                aInd = cutPrefix( dNameSpaces[ u"ifc" ] , res[ 'results' ][ 'bindings' ][ j ][ res[ 'head' ][ 'vars' ][ 0 ] ][ 'value' ] )
                # gen RDF
                # Owl class
                s = URIRef( dNameSpaces[ "p4bldg" ] + aClass + u"-" + aInd )
                o = URIRef( dNameSpaces[ "owl" ] + "Class" )
                g.add( ( s , RDF.type , o ) )
                # subClassOf
                p = URIRef( dNameSpaces[ "rdfs" ] + "subClassOf" )
                o = URIRef( dNameSpaces[ "p4bldg" ] + aClass )
                g.add( ( s , p , o ) )
                # seeAlso
                p = URIRef( dNameSpaces[ u"rdfs" ] + u"seeAlso" )
                o = URIRef( dNameSpaces[ u"ifc" ] + u"Ifc" + aClass + u"EnumType" )
                g.add( ( s , p , o ) )
                # Label
                p = URIRef( dNameSpaces[ "rdfs" ] + "label" )
                o = Literal( aInd , datatype = XSD.string)
                g.add( ( s , p , o ) )
                # Comment
                p = URIRef( dNameSpaces[ "rdfs" ] + "comment" )
                o = Literal( "Describe products of class " + aInd + " a specialisation of " + aClass , datatype = XSD.string)
                g.add( ( s , p , o ) )
    
    return g



def run():
    '''
    Run function of script to create product 4 Building ontology
    '''
    # Settings
    strSPARQLEndpoint = 'http://localhost:3030/'
    strDataset = 'ifcOWL'
    strEndpointAddress = strSPARQLEndpoint + strDataset + '/'
    print time.strftime('>[%Y-%m-%d %H:%M:%S]') , ' LOG:' , '\t' , "Started generating the Product4BuildingOntology"
    print time.strftime('>[%Y-%m-%d %H:%M:%S]') , ' LOG:' , '\t' , 'Triple story with ifcOWL4Add2 ontology needs to be available here: ' , strEndpointAddress
       
    # get SM description from knowledge base
    
    ( g , dNameSpaces ) = initRDF()
    g = genRDF( g  , strEndpointAddress )
    g = getEnumTypes( g , strEndpointAddress , dNameSpaces[ u"p4bldg" ] )
    saveRdf( g , "../PROD4Bldg.ttl" )
    
    print time.strftime('>[%Y-%m-%d %H:%M:%S]') , ' LOG:' , '\t' , "Finished! See file " , "PROD4Bldg.ttl"

run()