from argparse import ArgumentParser
from glob import glob
import logging
import os

from buildGraphImage import initialize_graph,initialize_File_graph,initialize_Multi_graph



def main(cli_args=None):
    usage = """%(prog)s FILENAME... [--all|--module|--func]"""
    desc = (
        "Analyse Python source files and generate an"
        "approximate call graph of the modules, classes and functions." 
    )

    parser = ArgumentParser(usage=usage, description=desc)

    parser.add_argument("--all", action="store_true", default=False, help="output all files")

    parser.add_argument("--module", action="store_true", default=False, help="output only file modules")

    parser.add_argument("--twopie", action="store_true", default=False, help="use twopie engine")

    parser.add_argument("--func", action="store_true", default=False, help="output functions graph")
 
    parser.add_argument("--output", default="call_graph.dot", help="output filename default:call_graph")

    parser.add_argument("--file_num", default=20, help="output files number")

    parser.add_argument("--no_edges", action="store_true", default=False, help="output without edges")

    parser.add_argument("--cluster", action="store_true", default=False, help="use cluster algorithm")

    parser.add_argument("--community", action="store_true", default=False, help="use community algorithm")

    parser.add_argument("--multi", action="store_true", default=False, help="use both module and file algorithm")

    parser.add_argument("--Folder_calls", action="store_true", default=False, help="Show edges between Folder")


    known_args, unknown_args = parser.parse_known_args(cli_args)
    filenames = unknown_args

    if unknown_args==[]:
        raise Exception('ERROR: No Filename Input {python pysa filename --multi}')


    if known_args.module:
         initialize_File_graph(os.path.abspath(unknown_args[0]),all=known_args.all,
                    module=known_args.module,func=known_args.func,
                    twopie=known_args.twopie, output=known_args.output,no_edges=known_args.no_edges)
    elif known_args.multi:
        initialize_Multi_graph(os.path.abspath(unknown_args[0]),all=known_args.all,
                    module=known_args.module,func=known_args.func,
                    twopie=known_args.twopie, output=known_args.output,file_num=known_args.file_num,
                    no_edges=known_args.no_edges,cluster=known_args.cluster,
                    community=known_args.community,Folder_calls=known_args.Folder_calls)
    else:
        initialize_graph(os.path.abspath(unknown_args[0]),all=known_args.all,
                    module=known_args.module,func=known_args.func,
                    twopie=known_args.twopie, output=known_args.output,file_num=known_args.file_num,
                    no_edges=known_args.no_edges,cluster=known_args.cluster,
                    community=known_args.community)
      
      
if __name__ == "__main__":
    main()