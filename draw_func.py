import pyan
from glob import glob
from pyan.analyzer import CallGraphVisitor
from pyan.visgraph import VisualGraph
import networkx as nx


def draw_func(Root_file,func_name):
    unknown_args=Root_file
    unknown_args=glob(unknown_args,recursive=True)


    filenames = [fn2 for fn in unknown_args for fn2 in glob(fn, recursive=True)]
    


    v = CallGraphVisitor(filenames, None)

    Filter_Function=func_name
    Filter_namespace=None


    if Filter_Function or Filter_namespace:

        if Filter_Function:
            function_name = Filter_Function.split(".")[-1]
            namespace = ".".join(Filter_Function.split(".")[:-1])
            node = v.get_node(namespace, function_name)

        else:
            node = None
        
        v.filter(node=node, namespace=Filter_namespace)

    graph_options = {
            "draw_defines": False,
            "draw_uses": True,
            "colored": True,
            "grouped_alt": True,
            "grouped": True,
            "nested_groups": True,
            "annotated": False,
        }

    graph = VisualGraph.from_visitor(v, options=graph_options, logger=None)
    
    
    

    # import networkx as nx
    # G=nx.DiGraph()
    # for i in graph.nodes:
    #     G.add_node(i.label)
    # for i in graph.edges:
    #     G.add_edge(i.source.label,i.target.label)

    # d_in=G.in_degree(G)
    # nodeDic={}
    # for i in G.nodes():
    #     nodeDic[i]=d_in[i]
    # print(G.number_of_nodes())
    # print(G.order())
    # print(sorted(nodeDic.items(),key=lambda item:item[1])[-int(G.order()/5):])



    print('test_image')
    with open('edges.txt','a') as f:
        for i in graph.edges:
            f.write("\"" + i.source.label + "\" -> "+"\"" + i.target.label+"\"" +"["+"constraint=false"+"]"+";\n")
        
