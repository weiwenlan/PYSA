# PYSA
python module and files analysis with Graphviz
### 目前封装成可以通过命令行调用的包的形式

该包通过展示文件和文件夹的调用关系以获得深入的探索视角，暂时可选的各项如下。

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
  --cluster            use cluster edges
```

下面根据每个选项展示实现效果

## 依赖库

```python
glob
os
re
random
**graphviz
networkx 
math**
```

# —all全文件分析

展示全文件之间的调用关系

```python
python pysa YOLOv5master  --all
```

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/1e87f6b0-6be3-43fa-aa3b-4395bcd9ad07/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/1e87f6b0-6be3-43fa-aa3b-4395bcd9ad07/Untitled.png)

# —module全文件夹分析

展示所有文件夹之间由内部文件组成的调用关系，该指向箭头越粗表示调用关系越强烈

```python
python pysa YOLOv5master  --module
```

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/84d671c1-5df9-445f-927b-7757cec2db17/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/84d671c1-5df9-445f-927b-7757cec2db17/Untitled.png)

# —twopie引擎生成图

该选项可以与任意其他选项一起使用，生成图将为放射图样，但原有的分组关系将被破坏

```python
python pysa YOLOv5master  --all --twopie
```

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cc8498f1-eebd-43c7-9217-11e220e2386c/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cc8498f1-eebd-43c7-9217-11e220e2386c/Untitled.png)

# —func选项

该选项可以与任意其他选项一起使用，生成图中加入调用的方法图（仅与被调用最高的文件有关的函数）

```python
python pysa YOLOv5master  --func
```

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c889795a-f0f3-490b-8cb7-93d93cff6f6c/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c889795a-f0f3-490b-8cb7-93d93cff6f6c/Untitled.png)

# —output选项

规定名字，默认为call_graph.dot

# —file_num 选项

该选项可以规定默认精选的文件的数量，默认为20个，小于该值会直接展示所有的文件。

```python
python pysa tornado  --file_num 30
```

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c173102b-03e1-40d1-82b8-7f35bd2bf7dd/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c173102b-03e1-40d1-82b8-7f35bd2bf7dd/Untitled.png)

```python
python pysa tornado 
```

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3d29a955-eb76-47f7-807b-cce4b90c513a/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3d29a955-eb76-47f7-807b-cce4b90c513a/Untitled.png)

# —no_edges

该选项直接禁用所有的边输出

```python
python pysa tornado --no_edges
```

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cbdeb3df-931d-4088-b455-189e4a50be67/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cbdeb3df-931d-4088-b455-189e4a50be67/Untitled.png)

# —cluster聚类分析

该选项使用聚类算法，展示的精选文件将首要展示聚类指数较大的

```python
python pysa tornado --cluster --file_num 40
```

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5dc8b189-d215-41c0-9336-3978fed3e7fa/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5dc8b189-d215-41c0-9336-3978fed3e7fa/Untitled.png)

这里展示的没有edge主要是由于，聚类指数较高的文件都是相对独立的调用了很多其他文件，所以极有可能互相没有任何调用，tornado代码中有超过400个文件，很有可能选出20个没有任何相对调用关系的函数。
