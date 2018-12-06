"""

TODO:
-----

[x] - AnnotationProperties
[x] - NamedIndividuals
[x] - DataProperties
[x] - ObjectProperties
[x] - Classes
[.] - Namespaces

[.] - Table of Contents
[.] - Templates


Types
-----

- URI
- email
- string

"""
import rdflib
from rdflib.namespace import RDF, RDFS, OWL, SKOS, DC, DCTERMS, URIRef
import pprint as pp

import toolkit


class RDFBase:

    def __init__(self, IRI, property_name, properties):
        self.IRI = IRI
        self.property_name = property_name
        self.properties = properties


class RDFClass(RDFBase):

    def __init__(self, IRI, property_name, properties):
        super(RDFClass, self).__init__(IRI, property_name, properties)


class RDFObjectProperty:

    def __init__(self, IRI, property_name, properties):
        self.IRI = IRI
        self.property_name = property_name
        self.properties = properties


class RDFDataProperty:

    def __init__(self, IRI, property_name, properties):
        self.IRI = IRI
        self.property_name = property_name
        self.properties = properties


class RDFNamedIndividual:

    def __init__(self, IRI, property_name, properties):
        self.IRI = IRI
        self.property_name = property_name
        self.properties = properties


class RDFAnnotationProperty:

    def __init__(self, IRI, property_name, properties):
        self.IRI = IRI
        self.property_name = property_name
        self.properties = properties


class RDFModel:
    def __init__(self, source, format):

        g = rdflib.Graph()
        g.parse(source, format=format)

        self.get_ontology_properties(g)
        self.annotation_properties = RDFModel.get_object_type_properties(g, OWL.AnnotationProperty, RDFAnnotationProperty)
        self.named_individuals = RDFModel.get_object_type_properties(g, OWL.NamedIndividual, RDFNamedIndividual)
        self.data_properties = RDFModel.get_object_type_properties(g, OWL.DatatypeProperty, RDFDataProperty)
        self.object_properties = RDFModel.get_object_type_properties(g, OWL.ObjectProperty, RDFObjectProperty)
        self.class_properties = RDFModel.get_object_type_properties(g, OWL.Class, RDFClass)

        print(isinstance(self.annotation_properties[0].IRI, rdflib.URIRef))
        print()

    @staticmethod
    def get_object_type_properties(g, object_type, class_type):
        object_type_properties = [] # like AnnotationProperties, NamedIndividuals, etc.
        ss = [] # list of subjects

        # find all the subjects and append to list ss
        for s, p, o in g.triples((None, RDF.type, object_type)):
            ss.append(s)

        for s_ in ss:
            ps = [] # list of predicates
            for s, p, o in g.triples((s_, None, None)):
                if p not in ps: # find all unique predicates and add to list ps
                    ps.append(p)

            properties = [] # properties of the object_type
            for p_ in ps:
                for s, p, o in g.triples( (s_, p_, None) ):
                    properties.append( (p, o) )
            class_type_property = class_type(s, toolkit.extract_property_name_from_uri(s), properties)
            object_type_properties.append((class_type_property))
        return object_type_properties

    def get_ontology_properties(self, g):
        self.IRI = RDFModel.get_IRI(g)
        # print(self.IRI)

        self.title = RDFModel.get_title(g, self.IRI)
        # print(self.title)

        self.version_IRI = RDFModel.get_version_IRI(g, self.IRI)
        # print(self.version_IRI)

        self.version = RDFModel.get_version(g, self.IRI)
        # print(self.version)

        self.authors = RDFModel.get_authors(g, self.IRI)
        # print(self.authors)

        self.contributors = RDFModel.get_contributors(g, self.IRI)
        # print(self.contributors)

        self.publishers = RDFModel.get_publishers(g, self.IRI)
        # print(self.publisher)

        self.imported_ontologies = RDFModel.get_imported_ontologies(g, self.IRI)
        # print(self.imported_ontologies)

        self.source = RDFModel.get_source(g, self.IRI)
        # print(self.source)

        self.comment = RDFModel.get_comment(g, self.IRI)
        # print(self.comment)

    @staticmethod
    def get_comment(g, IRI):
        for s, p, o in g.triples((URIRef(IRI), RDFS.comment, None)):
            if o is not None:
                return o

    @staticmethod
    def get_source(g, IRI):
        for s, p, o in g.triples((URIRef(IRI), DCTERMS.source, None)):
            if o is not None:
                return o

    @staticmethod
    def get_imported_ontologies(g, IRI):
        imported_ontologies = []
        for s, p, o in g.triples((URIRef(IRI), OWL.imports, None)):
            if o is not None:
                imported_ontologies.append(o)
        imported_ontologies.sort()
        return imported_ontologies

    @staticmethod
    def get_publishers(g, IRI):
        publishers = []
        for s, p, o in g.triples((URIRef(IRI), DCTERMS.publisher, None)):
            if o is not None:
                publishers.append(o)
        for s, p, o in g.triples((URIRef(IRI), DC.publisher, None)):
            if o is not None:
                publishers.append(o)
        publishers.sort()
        return publishers

    @staticmethod
    def get_contributors(g, IRI):
        contributors = []
        for s, p, o in g.triples((URIRef(IRI), DC.contributor, None)):
            if o is not None:
                contributors.append(o)
        for s, p, o in g.triples((URIRef(IRI), DCTERMS.contributor, None)):
            if o is not None:
                contributors.append(o)
        contributors.sort()
        return contributors

    @staticmethod
    def get_authors(g, IRI):
        authors = []
        for s, p, o in g.triples( (URIRef(IRI), DC.creator, None) ):
            if o is not None:
                authors.append(o)
        for s, p, o in g.triples( (URIRef(IRI), DCTERMS.creator, None) ):
            if o is not None:
                authors.append(o)
        authors.sort()
        return authors

    @staticmethod
    def get_version(g, IRI):
        for s, p, o in g.triples( (URIRef(IRI), OWL.versionInfo, None) ):
            if o is not None:
                return o

    @staticmethod
    def get_version_IRI(g, IRI):
        for s, p, o in g.triples((URIRef(IRI), OWL.versionIRI, None)):
            if o is not None:
                return o

    @staticmethod
    def get_title(g, IRI):
        for s, p, o in g.triples( ( URIRef(IRI), RDFS.label, None) ):
            if o is not None:
                return o
        for s, p, o in g.triples( ( URIRef(IRI), SKOS.prefLabel, None) ):
            if o is not None:
                return o
        for s, p, o in g.triples( ( URIRef(IRI), DC.title, None) ):
            if o is not None:
                return o
        for s, p, o in g.triples( ( URIRef(IRI), DCTERMS.title, None) ):
            if o is not None:
                return o

    @staticmethod
    def get_IRI(g):
        for s, p, o in g.triples( (None, RDF.type, OWL.Ontology) ):
            if s is not None:
                return s

