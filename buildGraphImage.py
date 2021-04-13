
from glob import glob
import os
import re
import random
import graphviz
from draw_func import draw_func
import networkx as nx
import math
import graph_insight as GI


file_hie={}
file_edges={}
all_files=[]
all_edges=[]
all_files_hie=[]
sorted_vertex={}
file_hie={}
important_edge=[]
n=0
Graph=None

# cut off other irrelevent vertex
show_less_relevent_vertex=False
# whether draw the function of the topnode
func=False
 # show all vertexes or main ones
show_all=False
# clear txts
clearFiles = True
# only show edges between important vertexes
show_important_edge=True
show_all_edge=True

exclude = {'.png','.json','.xlsx','.sh','.pdf','.model','.jpg','.so','txt'}
include = {'.py','.ipynb','.md','.sh'}
merge = "directory"






fixedColors = {".sh" : "cyan",
               ".py" : "white",
               ".ipynb" : "lawngreen",
               "sad": "blue",
               "Interface" : "gold",
               "Kernel" : "peachpuff",
               "Keyboard" : "dodgerblue",
               "Library" : "chocolate",
               "First" : "#ff7b54",
               "Second" : "#ffb26b",
               "Third" : "#ffd56b"}


# box, polygon, ellipse, oval, circle, point, egg, triangle, plaintext, plain, diamond,
# trapezium, parallelogram, house, pentagon, hexagon, septagon, octagon, doublecircle,
# doubleoctagon, tripleoctagon, invtriangle, invtrapezium, invhouse, Mdiamond, Msquare,
# Mcircle, rect, rectangle, square, star, none
fixedShapes = {".sh" : "\"box\"",
               ".py" : "\"rectangle\"",
               ".ipynb" : "\"rectangle\"",
               ".md" : "\"box\"",
               }

def randomizeColor():
    return str('#%02X%02X%02X' % (random.randint(64, 255),
                                  random.randint(64, 255),
                                  random.randint(64, 255)))

def isCode(name):
    
    result = os.path.splitext(name)[-1]
    
    if result in include:
        return True
    if (result in exclude):
        return False
    if (result is None):
        return False


# def getColor(name):
#     if (fixedColors.get(name) == None):
#         return randomizeColor()
#     else:
#         return fixedColors.get(name)


def getColor(name):

    # if name in sorted_vertex.keys():
    #     return "olive"
    #(sorted_vertex.keys())
    if name in sorted_vertex.keys():
        
        return fixedColors.get(sorted_vertex[name])
    return "white"


def shapeVertex(type_name,name):
    s = "["
    typeOfCode = os.path.splitext(type_name)[-1]
    if (fixedShapes.get(typeOfCode) != None):
        s += "shape=" + fixedShapes.get(typeOfCode)
    if (sorted_vertex.get(name) != None):
        s += ", " + "fillcolor=\"" + getColor(name) + "\""
    s += ','+'color="#dfe0df"'
    s += "];\n"
    return s




def funcjudge(result,result_list):
    if '.' in result:
        result=result.split('.')[-1]
    if result in all_files:
        result_list.append(result)
    return result_list


def findinclude(line):
    result_list=[]
    if 'from' in line:
        try:
            result=line.split(' ')[1]
            result_list=funcjudge(result,result_list)
        except:
            pass
        
        try:
            result=line.split(' ')[-1][:-1]
            result_list=funcjudge(result,result_list)
        except:
            pass

    elif 'import' in line:
        try:
            result= line.split(' ')[1]
            result_list=funcjudge(result,result_list)
        except:
            pass
    
    if result_list !=[]:    
        return result_list
    else:
        return ""
    

def writeedges(code, way):
    filename=way+ '/' + code
    f = open(filename)
    code = os.path.splitext(code)[-2]
    for line in f:
        included = findinclude(line)
        if (included != ""):
            for i in included:
                all_edges.append((str(i),str(code)))
        
    f.close()


def writedges(getfrom,getto,vertexes, edges):
    if getfrom !=getto:
        if getfrom in sorted_vertex.keys() and getto in sorted_vertex.keys():
            if show_important_edge:
                global important_edge
                for s in important_edge:
                    
                    if getfrom in s and getto in s:
                        edges.write("\"" + getfrom + "\" -> ")
                        edges.write("\"" + getto+ "\" ")
                        edges.write("[color=\"#440a67\",penwidth=12];\n")
            
            edges.write("\"" + getfrom + "\" -> ")
            edges.write("\"" + getto+ "\" ")
            edges.write(";\n")
        elif show_all_edge:
            edges.write("\"" + getfrom + "\" -> { ")
            edges.write("\"" + getto+ "\" ")
            edges.write("};\n")

def writedges_cross_files(getfrom,getto):
    same_hie=False
    target_hie=None
    source_hie=None
    global file_hie,file_edges

    for key in file_hie:
        if getto in file_hie[key]:
            target_hie=key
            break
    for key in file_hie:
        if getfrom in file_hie[key]:
            source_hie=key
            break
    if target_hie == None or source_hie== None:
        pass
    else:
        file_edges[str(source_hie)][str(target_hie)]+=1


def writeGraph_cross_files(code, way):
    filename=way+ '/' + code
    f = open(filename)
    
    code = os.path.splitext(code)[-2]
    for line in f:
        included = findinclude(line)
        if (included != ""):
            for i in included:
                
                writedges_cross_files(i,code)
    f.close()

def writeGraph(code, way, vertexes, edges):
    filename=way+ '/' + code
    f = open(filename)
    
    code = os.path.splitext(code)[-2]
    for line in f:
        included = findinclude(line)
        if (included != ""):
            for i in included:
                print(i,code)
                writedges(i,code,vertexes, edges)
    f.close()

def skip(name):
    if name=='__init__.py':
        return True
    else:
        return False



def walkfilesfirst(file):
    '''
    walk among all files and get all names
    '''
    g = os.walk(file)  
    for path,dir_list,file_list in g:  
        for file_name in file_list:  
            if isCode(file_name):
                all_files.append(os.path.splitext(file_name)[0])

    g = os.walk(file)
    for path,dir_list,file_list in g:  
        for file_name in file_list:
            if isCode(file_name):
                writeedges(file_name,path)


def walk_communities(vertexes,res):
    global n
    n+=1
    vertexes.write("subgraph cluster_" + str(n) + " {\n")
    vertexes.write("node [style=\"filled\", " +
                   "shape=\"box\", " +
                   "color=\"#dfe0df\", " +
                   "bgcolor=\"" + "#dfe0df" + "\"];\n")
    
    vertexes.write("label = \"" + "Ind" + "\";\n")
    for i in res:
        vertexes.write("\""+str(i)+"\"[shape=\"rectangle\", fillcolor=\"#ffd56b\"];\n")
    vertexes.write("}\n")


def walkFiles_without_nodes(adress, way, vertexes, edges):
    
    global n
    n += 1
    way = way + "/" + adress
    cat = os.listdir(way)


    for obj in cat:
        
        if (os.path.isdir(way+"/" + obj)):
            walkFiles(obj, way, vertexes, edges)
        else:
            if skip(obj):
                continue
            if (isCode(obj)):
                
                obj_t=os.path.splitext(obj)[-2]
                global show_less_relevent_vertex
                if obj_t not in sorted_vertex and show_less_relevent_vertex:
                    continue
                
                writeGraph(obj, way, vertexes, edges)
    


def walkFiles(adress, way, vertexes, edges):
    
    global n
    n += 1
    way = way + "/" + adress
    cat = os.listdir(way)

    vertexes.write("subgraph cluster_" + str(n) + " {\n")
    vertexes.write("node [style=\"filled\", " +
                   "shape=\"box\", " +
                   "color=\"#dfe0df\", " +
                   "bgcolor=\"" + "#dfe0df" + "\"];\n")
    
    vertexes.write("label = \"" + adress + "\";\n")
    for obj in cat:
        
        if (os.path.isdir(way+"/" + obj)):
            walkFiles(obj, way, vertexes, edges)
        else:
            if skip(obj):
                continue
            if (isCode(obj)):
                
                obj_t=os.path.splitext(obj)[-2]
                global show_less_relevent_vertex
                if obj_t not in sorted_vertex and show_less_relevent_vertex:
                    continue
                vertexes.write("\""+obj_t+"\""+shapeVertex(obj,obj_t))
                
                writeGraph(obj, way, vertexes, edges)
    
    vertexes.write("}\n")

def cross_files(adress, way, totems):
    '''
    generate the file tree and save as a dic {a:{b,c,d},{},{{}}}
    save in file_hie

    '''
    file_tmp=[]
    way = way + "/" + adress
    cat = os.listdir(way)
    for obj in cat:
        
        if (os.path.isdir(way+"/" + obj)):
            x=totems+"."+str(obj)
            cross_files(obj, way,x)
        else:
            if skip(obj):
                continue
            if (isCode(obj)):
                
                obj_t=os.path.splitext(obj)[-2]
                
                
                file_tmp.append(str(obj_t))
    
    global file_hie           
    file_hie[totems]=file_tmp


def cross_Multi_files(adress, way, totems,vertexes,edges):
    jumped=['.git','.github','__pycache__']
    file_tmp=[]
    way = way + "/" + adress
    cat = os.listdir(way)
    for obj in cat:
        
        if (os.path.isdir(way+"/" + obj)):
            if str(obj) not in jumped:
                x=totems+"."+str(obj)
                edges.write("\"" + totems + "\" -> ")
                edges.write("\"" + x+ "\" ")
                edges.write("[color=\"#dfe0de\"];\n")
                cross_Multi_files(obj, way,x,vertexes,edges)
        else:
            if skip(obj):
                continue
            if (isCode(obj)):
                
                obj_t=os.path.splitext(obj)[-2]
                if obj_t in sorted_vertex:
                    vertexes.write("\""+obj_t+"\""+shapeVertex(obj,obj_t))

                    edges.write("\"" + totems + "\" -> ")
                    edges.write("\"" + obj_t+ "\" ")
                    edges.write("[color=\"#dfe0df\"];\n")
                file_tmp.append(str(obj_t))
    
    global file_hie           
    file_hie[totems]=file_tmp


def walkfiles_cross_files(adress, way):
    '''
    count calls among files and conclude them on the folder node
    '''

    way = way + "/" + adress
    cat = os.listdir(way)


    for obj in cat:
        if (os.path.isdir(way+"/" + obj)):
            walkfiles_cross_files(obj, way)
            
        else:
            if skip(obj):
                continue
            if (isCode(obj)):
                writeGraph_cross_files(obj, way)
  

def buildGraph():
    global G
    G = nx.DiGraph() 
    G.add_nodes_from(all_files)
    G.add_edges_from(all_edges)


def show_important_edge_func():
    global important_edge
    important_edge = GI.find_bridge(G)
    
def show_chains(G):
    result=GI.find_chains(G)
    for i in result:
        print(i)


def show_clique(G):
    result=GI.find_max_clique(G)
    for i in result:
        print(i)


def show_community(G):
    result=GI.find_community(G)
    for i in result:
        print(i)


def find_top_node(num,en_cluster):
    
    print('Number of nodes',G.order())
    print('Number of edges',G.number_of_edges())

    
    #node_list= GI.rankpage_order(G)
    node_list=GI.rankpage(G)
    if en_cluster:
        node_list=GI.find_cluster(G)


    
    count=0
    if G.order()>num:
        control_number=num
    else:
        control_number=G.order()
    
    for i in node_list:
        if len(sorted_vertex)>=control_number:
            break
        if count<=control_number/5:
            sorted_vertex[i[0]]='First'
        elif count<=control_number/2.5:
            sorted_vertex[i[0]]='Second' 
        else:
            sorted_vertex[i[0]]='Third' 
        count+=1
    return node_list[0]





def show_image(engine,name):
    #generate the image
    from graphviz import Source
    image=Source.from_file(os.getcwd()+'/'+name,engine=engine)
    image.view()

def show_image_html():
    os.system('dot  code_graph_html/demo.gv -T svg -o  code_graph_html/demo.svg')


def initialize_graph(ori,**params):
    
    global func
    func=params['func']
    # show important edges in the file
    global show_important_edge
    show_important_edge=False
    # clear txts
    global clearFiles
    clearFiles = True
    global show_all
    # show all vertexes or main ones
    # show all edges in the file
    show_all=params['all']
    global show_less_relevent_vertex,show_all_edge
    if show_all:
        show_less_relevent_vertex=False
        show_all_edge=True
    else:
        show_less_relevent_vertex=True
        show_all_edge=False

    
    
    vertexes = open("vertexes.txt", "w")
    edges  = open("edges.txt", "w")

    outfile = open(params['output'], "w")
    n = 0
    vertexes.write("digraph G{\n")
    vertexes.write("concentrate=\"True\"\n")
    vertexes.write('''fontsize=15;\nstyle = \"bold\";\nrankdir=\"TB\";\n
        fontname=Arial;\nnodesep=0.5;\noverlap=False;\nranksep=2;\n
        concentrate=False;\nordering=out;\nsplines=polyline;\nrank=\"max\";\n''')
    vertexes.write("edge[arrowtail=none,style=tapered,penwidth=6,arrowhead=none,dir=forward,color=\"#a3d2ca\",dir=back;]\n")
    vertexes.write("node [style=\"filled\", " +
                    "fillcolor=\"" + getColor("base_color") + "\"];\n")
    
    # path of file
    # ori='/Users/wwl/Downloads/graph_Of_Included-master/YOLOv5master/aiohttpmaster'
    ori = ori
    srcname=ori.split('/')[-1]
    src=ori.replace('/'+srcname,'')

    walkfilesfirst(src+'/'+srcname)

    buildGraph()
    global G
    #show_chains(G)
    #show_clique(G)
    

    top_node=find_top_node(int(params['file_num']),params['cluster'])

    if show_important_edge:
        show_important_edge_func()
        #print(important_edge)
    
    if params['community']:
        res=GI.find_community(G)
        for i in res:
            walk_communities(vertexes,i)
        walkFiles_without_nodes(srcname, src, vertexes, edges)
    else:    
        walkFiles(srcname, src, vertexes, edges)
    


    print('top_node',top_node)
    vertexes.close()
    edges.close()
    if func:
        draw_func(ori+'/**/*.py',top_node[0])


    for line in open("vertexes.txt"):
        outfile.write(line)
    if not params['no_edges']:
        for line in open("edges.txt"):
            outfile.write(line)
    
    outfile.write("}")
    outfile.close()
    vertexes.close()
    edges.close()

    if (clearFiles):
        os.remove("vertexes.txt")
        os.remove("edges.txt")
    
    if params['twopie']:
        engine='twopi'
    else:
        engine = 'dot'
    show_image(engine,params['output'])
    



def initialize_File_graph(ori,**params):
    
    global func
    func=params['func']
    # show important edges in the file
    global show_important_edge
    show_important_edge=True
    # clear txts
    global clearFiles
    clearFiles = True
    global show_all
    # show all vertexes or main ones
    # show all edges in the file
    show_all=params['all']
    global show_less_relevent_vertex,show_all_edge
    if show_all:
        
        show_less_relevent_vertex=False
        show_all_edge=True
    else:
        
        show_less_relevent_vertex=True
        show_all_edge=False

    
    vertexes = open("vertexes.txt", "w")
    edges  = open("edges.txt", "w")

    outfile = open(params['output'], "w")
    n = 0
    vertexes.write("digraph G{\n")
    vertexes.write("concentrate=\"True\"\n")
    vertexes.write('''fontsize=15;\nstyle = \"bold\";\nrankdir=\"TB\";\nfontname=Arial;\nnodesep=0.5;\n
        overlap=False;\nranksep=2;\nconcentrate=False;\nordering=out;\n
        splines=polyline;\nrank=\"max\";\n''')
    vertexes.write("edge[arrowtail=none,style=tapered,penwidth=6,arrowhead=none,dir=forward,color=\"#a3d2ca\"];\n")
    vertexes.write("node [style=\"filled\", " +
                    "fillcolor=\"" + getColor("base_color") + "\"];\n")


    """
    initiate file path
    """
    ori = ori
    srcname=ori.split('/')[-1]
    src=ori.replace('/'+srcname,'')

    """
    walk file to draw the inner connection
    """
    walkfilesfirst(src+'/'+srcname)
    cross_files(srcname,src,srcname)


    """
    file_hie{xxx:{xxx:234}} contains the num 
    of connections between different files
    """
    global file_hie
    for i in list(file_hie.keys()):
        if file_hie[i]==[]:
            del file_hie[i]
            continue
    
    global file_edges
    for i in list(file_hie.keys()):
        tmp={}
        for j in list(file_hie.keys()):
            
            tmp[j]=0
        file_edges[i]=tmp

    '''
    count the num of calls
    '''


    walkfiles_cross_files(srcname, src)
    

    """
    build Graph and use pagerank 
    """
    global G
    G = nx.DiGraph()

    for i in list(file_hie.keys()):
        for j in list(file_hie.keys()):
            if file_edges[i][j]!=0:
                G.add_edge(i,j)
                

    find_top_node(params['file_num'],False)
    global sorted_vertex

    for i in list(file_hie.keys()):
        if i in sorted_vertex:
            for j in list(file_hie.keys()):
                if j in sorted_vertex:
                    if file_edges[i][j]!=0:
                        num = file_edges[i][j]
                        if num>10:
                            num = math.log2(num)
                        
                        if num<=1:
                            num=1
                        num = int(num)
                        edges.write("\"" + str(i) + "\" -> ")
                        edges.write("\"" + str(j)+ "\" ")
                        edges.write("[penwidth="+str(num)+ 'color = "#dfe0df"'+"];\n")
                        


    for key in sorted_vertex:
        vertexes.write('node [style="filled", shape="folder", color="#dfe0df", bgcolor="#dfe0df"];\n')
        vertexes.write(' \"'+str(key)+"\";\n")
    
    vertexes.close()
    edges.close()
    

    for line in open("vertexes.txt"):
        outfile.write(line)
    if not params['no_edges']:
        for line in open("edges.txt"):
            outfile.write(line)
    
    outfile.write("}")
    outfile.close()
    vertexes.close()
    edges.close()

    if (clearFiles):
        os.remove("vertexes.txt")
        os.remove("edges.txt")
    
    if params['twopie']:
        engine='twopi'
    else:
        engine = 'dot'
    show_image(engine,params['output'])
    


def initialize_Multi_graph(ori,**params):
    global func
    func=params['func']
    # show important edges in the file
    global show_important_edge
    show_important_edge=True
    # clear txts
    global clearFiles
    clearFiles = True
    global show_all
    # show all vertexes or main ones
    # show all edges in the file
    show_all=params['all']
    global show_less_relevent_vertex,show_all_edge
    if show_all:
        
        show_less_relevent_vertex=False
        show_all_edge=True
    else:
        
        show_less_relevent_vertex=True
        show_all_edge=False

    
    vertexes = open("vertexes.txt", "w")
    edges  = open("edges.txt", "w")

    outfile = open(params['output'], "w")
    n = 0
    vertexes.write("digraph G{\n")
    #vertexes.write("concentrate=\"True\"\n")
    # vertexes.write('''fontsize=15;\nstyle = \"bold\";\nrankdir=\"TB\";\nfontname=Arial;\nnodesep=0.5;\nsplines=polyline;\n
    #     overlap=False;\nordering=out;\n
    #     rank=\"max\";\n''')
    vertexes.write("edge[arrowtail=none,style=tapered,penwidth=4,arrowhead=none,dir=forward,color=\"#a3d2ca\"];\n")
    vertexes.write("node [style=\"filled\", " +
                    "fillcolor=\"" + getColor("base_color") + "\"];\n")
    vertexes.write('node [style="filled", shape="folder", color="#dfe0df", bgcolor="#dfe0df"];\n')

    """
    initiate file path
    """
    ori = ori
    srcname=ori.split('/')[-1]
    src=ori.replace('/'+srcname,'')

    '''
    walk file to generate all file names
    '''
    walkfilesfirst(src+'/'+srcname)


    '''
    build Graph of the files 
    '''
    buildGraph()
    top_node=find_top_node(int(params['file_num']),params['cluster'])



    '''
    build Graph of all Folders 
    '''

    cross_Multi_files(srcname,src,srcname,vertexes,edges)

    global file_hie
    for i in list(file_hie.keys()):
        if file_hie[i]==[]:
            del file_hie[i]
            continue





    '''
    this shows the important calls cross modules by using --Folder_calls
    '''
    if params['Folder_calls']:  
        global file_edges
        for i in list(file_hie.keys()):
            tmp={}
            for j in list(file_hie.keys()):
                
                tmp[j]=0
            file_edges[i]=tmp

        walkfiles_cross_files(srcname, src)

        for i in list(file_hie.keys()):
            for j in list(file_hie.keys()):
                if file_edges[i][j]!=0:
                    num = file_edges[i][j]
                    if num>10:
                        num = math.log2(num)
                    
                    if num<=1:
                        num=1
                    num = int(num)
                    edges.write("\"" + str(i) + "\" -> ")
                    edges.write("\"" + str(j)+ "\" ")
                    edges.write("[color=\"#1687a7\",penwidth="+str(2*num)+"];\n")
                    


    
    vertexes.close()
    edges.close()
    

    for line in open("vertexes.txt"):
        outfile.write(line)

    if not params['no_edges']:
        for line in open("edges.txt"):
            outfile.write(line)
    
    outfile.write("}")
    outfile.close()
    vertexes.close()
    edges.close()

    if (clearFiles):
        os.remove("vertexes.txt")
        os.remove("edges.txt")
    
    if params['twopie']:
         engine='twopi'
    else:
         engine = 'dot'
    show_image(engine,params['output'])
    #show_image_html()
