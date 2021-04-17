# PYSA

python module and files analysis with Graphviz



# Demo

Visit https://weiwenlan.github.io/code-graph-test/



## Dependencies

```
networkx
jinjia2
glob
graphviz
```

This module have multiple options as below

```python
optional arguments:
  -h, --help           show this help message and exit
  --all                output all files
  --module             output only file modules
  --twopie             use twopie engine
  --func               output functions graph
  --output OUTPUT      output filename default:call_graph
  --file_num FILE_NUM  output files number
  --no_edges           output without edges
  --cluster            use cluster algorithm
  --community          use community algorithm
  --multi              use both module and file algorithm
  --Folder_calls       Show edges between Folder
```

Some examples are shown below.

# Legend

![legend](img/legend.png)

# No options

```python
python pysa YOLOv5master 
```

this cmd let pysa dealing with the yolov5 files and generate the call graph. The bigger rectangle means the affiliation. 

![image1](img/image1.png)

# — multi [mix analysis]

Multi call graph will provide the call graph both in file calls and module calls. This graph contains two parts, the grey folders stand for the folders and the colorful squares stand for file calls. See more in legend.

```python
python pysa aiohttpmaster --multi
```

![image2](img/image2.png)

# —all [show all files]

Show all files in the call graph. **NOT RECOMMENDED** graph could be so complicated.

```bash
python pysa YOLOv5master  --all
```



# —module [show all modules]

Show call relations between modules, the closer the relation, the wider the pen width.

```bash
python pysa tornado --module
```

![image3](img/image3.png)

# —twopie

Use with any options, this will generate a image using twopi (default is dot)

```python
python pysa YOLOv5master  --all --twopie
```

![image4](img/image4.png)

# —func [use with default]

this will generate some of the nodes from PYAN

```python
python pysa YOLOv5master  --func
```



# —output

Setting the output name default is call_graph.dot

# —file_num 

Setting the number of files , this decided the number of files showed, these files are chosen by the algorithm, the default setting is **20**。

```python
python pysa tornado  --file_num 30
```

![image5](img/image5.png)

```python
python pysa tornado 
```

![image6](img/image6.png)

# —no_edges [used with any options]

Under this setting, only nodes will be shown.

```python
python pysa tornado --no_edges
```

![image7](img/image7.png)

# —cluster [used with file calls]

This option uses cluster algorithm and show the files with high cluster index.

```python
python pysa aiohttpmaster --cluster 
```

![image8](img/image8.png)

# —community [used with file calls]

This option uses community algorithm and show all files in the community way.

```bash
 python pysa aiohttpmaster --community
```



![image9](img/image9.png)

