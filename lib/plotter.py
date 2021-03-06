import networkx as nx
import matplotlib.pyplot as plt
import basic
from lib.similarity import Similarity
import config
import pickle

class Plot():
    def __init__(self):
        self.G = nx.DiGraph()
        self.operation_nodes=[]
        self.input_nodes=[]
        self.output_nodes=[]
        self.node_color=[]
        self.node_size=[]
        self.id=0

    def show(self):
        for v in self.G:
            self.node_size.append(500)
            if v in self.operation_nodes:
                self.node_color.append(1.0)
            elif v in self.input_nodes:
                self.node_color.append(2.0)
            else:
                self.node_color.append(3.0)

        nx.draw(self.G,node_color=self.node_color,node_size=self.node_size,alpha=0.3,edge_color='b',font_size=8)
        plt.savefig("joker.png")

        plt.show()

    def __wsdl__(self,wsdl):
        data=wsdl.nodes
        operation=data['nodes']['operation']
        input_nodes=data['nodes']['input']
        output_nodes=data['nodes']['output']

        operation_node=self.node_name(operation,wsdl.id)
        self.operation_connect(operation_node,input_nodes,wsdl.id,True)
        self.operation_connect(operation_node,output_nodes,wsdl.id,False)
        self.operation_nodes.append(operation_node)

    def operation_connect(self,operation_node,nodes,id,isInward=True):
        #self.node_color.append(1.0)
        for node in nodes:
            data_node=self.node_name(node['name'],id)
            if isInward: #input nodes
                self.input_nodes.append(data_node)
                self.G.add_edge(data_node,operation_node)
            else:
                self.output_nodes.append(data_node)
                self.G.add_edge(operation_node,data_node)
            self.data_node_connect(data_node,node,id,isInward)

    def data_node_connect(self,center,nodes,id, isInward=True):
        if nodes.has_key("name"):
            del(nodes['name'])
        for node in nodes.iterkeys():
            #self.node_color.append(2.0)
            if node != " ".join(center.split(" ")[:1]):
                new_node=self.node_name(node,id)
                if not isInward:
                    self.G.add_edge(center,new_node)
                    self.output_nodes.append(new_node)
                else:
                    self.G.add_edge(new_node,center)
                    self.input_nodes.append(new_node)
                self.data_node_connect(new_node, nodes[node],isInward)

    def wsdl_connect(self,wsdl_input,wsdl_output):
        input_operation=wsdl_input.operation()
        output_operation=wsdl_output.operation()
        print wsdl_input.id,wsdl_output.id
        input_nodes=[]
        for __input__ in input_operation['nodes']['input']:
            input_nodes.append(__input__['name'])
            del(__input__['name'])
            basic.dict_to_list(__input__,input_nodes)

        output_nodes=[]
        for __output__ in output_operation['nodes']['output']:
            output_nodes.append(__output__['name'])
            del(__output__['name'])
            basic.dict_to_list(__output__,input_nodes)

        for input_node in input_nodes:
            for output_node in output_nodes:
                if Similarity(input_node,output_node).value > config.threshold:
                #if True:
                    print "DRAW",input_node, output_node
                    self.G.add_edge(self.node_name(output_node,wsdl_output.id),self.node_name(input_node,wsdl_input.id))

    @staticmethod
    def node_name(name,id):
        return name+" "+str(id)

    def save_sdg(self):
        _file=open(config.SDG,"w")
        pickle.dump(self.G,_file)

        _file=open(config.OPERATION_NODES,"w")
        pickle.dump(self.operation_nodes,_file)

        _file=open(config.INPUT_NODES,"w")
        pickle.dump(self.input_nodes,_file)

        _file=open(config.OUTPUT_NODES,"w")
        pickle.dump(self.output_nodes,_file)

    def load_sdg(self):
        _file=open(config.SDG,"r")
        self.G=pickle.load(_file)

        _file=open(config.OPERATION_NODES,"r")
        self.operation_nodes=pickle.load(_file)

        _file=open(config.INPUT_NODES,"r")
        self.input_nodes=pickle.load(_file)

        _file=open(config.OUTPUT_NODES,"r")
        self.output_nodes=pickle.load(_file)

    #def search_node(self,node):
    #    for v in self.G.nodes():
    #        if node == self.node_name(str(v)):
    #            return v
    #    return None
    #
    #@staticmethod
    #def node_name(node):
    #    return " ".join(node.split(" ")[:1])