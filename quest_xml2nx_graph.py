# -*- coding: utf-8 -*-
import lxml
import networkx as nx

def is_tech_article(article:lxml.etree._Element):
    '''
    In the xml files we use some items with tag 'article' contain data 
    and some - scripts. The function is used to filter the first type of items

    Parameters
    ----------
    article : lxml.etree._Element
        An item from parsed xml which has a tag 'article'

    Returns
    -------
    Boolean
        True if article has one child and it is a script

    '''
    assert article.tag == 'article'
    return len(article) == 1 and article[0].tag == 'script'

def xml2graph(xml_path:str):
    '''

    Parameters
    ----------
    xml_path : str
        The path to the xml file, parsed from quest-book.ru

    Returns
    -------
    quest_graph : nx.DiGraph
        Graph representation of the text quest

    '''
    #parse xml
    tree = lxml.etree.parse(xml_path)
    root = tree.getroot()
    #init empty Digraph
    quest_graph = nx.DiGraph()
    for root_child in root:
        #items with tag 'article' can contain data or a script, we need the first one
        if root_child.tag == 'article' and not is_tech_article(root_child):
            current_fragment_id = root_child.values()[0]
            for article_child in root_child:
                if article_child.tag == 'text':
                    current_fragment_text = article_child.text
                    ##add node and set fragment text as its attribute
                    quest_graph.add_nodes_from([current_fragment_id], fragment_text = current_fragment_text)
                elif article_child.tag == 'action':
                    ##add edge and set button text as its attribute
                    ##each 'action' has 2 values: next fragment id (containes '-') and button type
                    transition_point_id = [value for value in article_child.values() if '-' in value][0]
                    transition_command = article_child.text
                    quest_graph.add_edges_from([(current_fragment_id, transition_point_id, {'command':transition_command})])
    return quest_graph