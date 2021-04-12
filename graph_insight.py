import networkx as nx

def code_path(G,gofrom,goto):
    result_list=[]
    path_iter = nx.all_simple_paths(G, 'web', 'test_connector')
    for i in path_iter:
        result_list.append(i)
    return result_list


def find_max_clique(G):
    from networkx.algorithms.approximation.clique import max_clique,large_clique_size
    return max_clique(G)


def find_bridge(G):
    G=G.to_undirected() 
    from networkx.algorithms.bridges import bridges
    result_list=[]
    path_iter = bridges(G)
    for i in path_iter:
        result_list.append(i)
    return result_list

def find_chains(G):
    G=G.to_undirected()
    from networkx.algorithms.chains import chain_decomposition
    result_list=[]
    path_iter = chain_decomposition(G)
    for i in path_iter:
        result_list.append(i)
    return result_list


def find_community(G):
    from networkx.algorithms import community
    communities_generator = community.girvan_newman(G)
    top_level_communities = next(communities_generator)
    return top_level_communities
    length=0
    final=None
    print()
    for i in top_level_communities:
        x=len(i)
        if x>length:
            length=x
            final=i
        else:
            continue
    return list(final)


def rankpage(G):
    pr=nx.pagerank(G)
    result_list=[]
    s=sorted(pr.items(),key=lambda item:item[1])
    for i in s[::-1]:
        result_list.append(i)
    return result_list

def find_cluster(G):
    from networkx.algorithms import cluster
    nodeDic=cluster.clustering(G)
    result_list=[]
    s=sorted(nodeDic.items(),key=lambda item:item[1])
    for i in s[::-1]:
        result_list.append(i)
    return result_list

def rankpage_order(G):
    nodeDic={}
    d_in=G.in_degree(G)
    for i in G.nodes():
        nodeDic[i]=d_in[i]
        s=sorted(nodeDic.items(),key=lambda item:item[1])
    result_list=[]
    for i in s[::-1]:
        result_list.append(i)
    return result_list