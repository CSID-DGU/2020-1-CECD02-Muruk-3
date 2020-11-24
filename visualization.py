# -*- coding: utf-8 -*-

from bokeh.io import output_file, show, output_notebook
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool,
                          NodesAndLinkedEdges, EdgesAndLinkedNodes,
                          TapTool, BoxSelectTool)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, LabelSet, OpenURL, CustomJSTransform
from bokeh.plotting import from_networkx
#from bokeh.models.graphs import from_networkx
from bokeh.transform import transform, linear_cmap
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8
import random
import networkx as nx
import pandas as pd
from bokeh.io import output_notebook
import os
import find_csv_visual as fcv

def draw_graph(yyyymm):
    visual_df2, yyyy, mm = fcv.find_csv_visual(yyyymm)

    temp_pd = pd.DataFrame()
    G = nx.Graph()

    if len(visual_df2) > 0:
        for k, m in zip(visual_df2['itemsets'], visual_df2['support']):
            text = k[11:-2]
            first, second = text.split(', ')
            edge_tuple = (first, second)
            G.add_edge(first, second, weight=m * 10)

    flag = 0
    for node in G.nodes():
        if node == "'무단'":
            flag = flag + 1
        elif node == "'배포'":
            flag = flag + 1
    if flag == 2:
        G.remove_node("'무단'")
        G.remove_node("'배포'")

    #dir = '/content/drive/My Drive/뉴스분석_소스코드/02. 전처리/김민선/graph_info/'
    dir = './data_storage/graph-info/'

    yyy = str(yyyymm)[:4]
    mm = str(yyyymm)[4:]
    if mm[0] == '0':
        mm = mm[1]
    csv_dir = dir + yyyy + '_' + mm
    csv_list = os.listdir(csv_dir)

    tmp_pd = pd.DataFrame()
    for i in csv_list:
        tmp_pd = pd.read_csv(csv_dir + '/' + i, index_col=0, encoding='utf-8')
    tmp_pd.reset_index(drop=True, inplace=True)

    title = tmp_pd['기사 제목']
    link = tmp_pd['기사 링크']
    content = tmp_pd['기사 내용']

    title.reset_index(drop=True, inplace=True)
    link.reset_index(drop=True, inplace=True)
    content.reset_index(drop=True, inplace=True)

    # 노드의 내용을 읽고 [기사 내용]에서 그 노드 값이 들어간 기사를 찾아서
    # [기사 제목]과 [기사 링크]를 hover로 둔다.

    output_notebook()

    HOVER_TOOLTIPS = [
        # 일단 키워드와 차수만..
        # hover box에 display할 속성들 생각하기.. ######
        ("키워드", "@index"),
        ("연관 단어 수", "@degree"),
        ("관련 기사 제목", "@title"),
        ("관련 기사 링크", "@link")  # 클릭하면 가니까 없어도 될듯?????
    ]

    # 기본 bokeh 플랏 구성
    plot = figure(tooltips=HOVER_TOOLTIPS, plot_width=1000, plot_height=1000,  # 800 800
                  x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), tools="tap, pan, wheel_zoom, save, reset",
                  active_scroll='wheel_zoom')

    plot.title.text = yyyy + "년 " + mm + "월 뉴스 시각화 그래프"

    ## openUrl 기능..##
    ##### 노드마다 속성 추가하고 hover tool tip에서 자동으로 tap 가능해야 함!!####
    # @ 으로 속성 접근 가능

    url = '@link'
    taptool = plot.select(type=TapTool)  ###여기
    taptool.callback = OpenURL(url=url)

    # content = urlopen(link).read()

    # 각 노드의 차수 계산하고 노드 속성에 추가
    degrees = dict(nx.degree(G))
    degrees2 = [0 * val for (node, val) in G.degree()]
    nx.set_node_attributes(G, name='degree', values=degrees)

    # 노드에 기사 링크 속성 추가
    link_set = []
    title_set = []
    for i in G.nodes():
        link_sheet = []
        word = i[1:-1]
        for j, k in zip(content, range(len(content))):
            if j.find(word) > 0:
                link_sheet.append(k)
        num = random.choice(link_sheet)
        link_set.append(link[num])
        title_set.append(title[num])
    link_dictionary = dict(zip(G.nodes(), link_set))
    title_dictionary = dict(zip(G.nodes(), title_set))
    nx.set_node_attributes(G, name='link', values=link_dictionary)
    nx.set_node_attributes(G, name='title', values=title_dictionary)

    #print(link_dictionary)

    # 작은 차수를 가진 노드도 보이도록 수치 조정
    number_to_adjust_by = 7

    # 일단 테스트로 값 5로주고 degree에 더하고
    adjusted_node_size = dict([(node, degree + number_to_adjust_by) for node, degree in nx.degree(G)])
    nx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)

    size_by_this_attribute = 'adjusted_node_size'

    # ("연관도", "@weight")  ########## 호버 기능 수정.....

    # node_hover_tool = HoverTool(tooltips=[("키워드", "@index"), ("Degree", "@degree")])
    # plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

    graph_renderer = from_networkx(G, nx.spring_layout, scale=10, center=(0, 0))

    """
    node_size = {10 * val for (node, val) in G.degree()}
        #{k:5*v for k,v in G.degree()}
    nx.set_node_attributes(G, G.degree(), 'node_size')
    source=ColumnDataSource(pd.DataFrame.from_dict({val for (node, val) in G.nodes(data=True)},orient='nodesize'))
    graph_renderer.node_renderer.data_source = source
    """

    # 노드별 차수 구하는 방법
    # degrees = [10 * val for (node, val) in G.degree()]
    # print(degrees)

    # 노드 사이즈와 컬러 설정
    graph_renderer.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color='#c6dbef')

    # 호버 컬러
    graph_renderer.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color='white', line_width=2)

    # 클릭했을 때 컬러와 사이즈
    graph_renderer.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color='white', line_width=2)

    # 엣지 설정
    graph_renderer.edge_renderer.glyph = MultiLine(line_color='#c6dbef', line_alpha=0.8, line_width=1)

    # 엣지 호버 컬러
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color='black', line_width=2)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color='black', line_width=2)

    # 노드와 엣지 하이라이트
    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(graph_renderer)

    # 노드 레이블링
    x, y = zip(*graph_renderer.layout_provider.graph_layout.values())
    node_labels = list(G.nodes())
    source = ColumnDataSource({'x': x, 'y': y, 'name': [node_labels[i] for i in range(len(x))]})
    labels = LabelSet(x='x', y='y', text='name', source=source, background_fill_color='white', text_font_size='10px',
                      background_fill_alpha=.7)
    plot.renderers.append(labels)
    print('... ###', yyyy, '년', mm, '월 뉴스 시각화를 진행하는 중 ... ###')
    output_file("interactive_graphs_" + yyyy + "_" + mm + ".html")
    show(plot)

    # print(G.nodes(data=True))