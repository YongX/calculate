
class Node(object):
    def __init__(self, data=0, name=""):
        self._data = data
        self._name = name
        self._children = []
        self._deep = 0

    def add_child(self, obj):
        self._children.append(obj)

    def get_data(self):
        return self._data

    def get_name(self):
        return self._name

    def get_deep(self):
        return self._deep

    def set_deep(self, deep):
        self._deep = deep




# 创建根节点
root=Node(0, 'root')

def generate_node(data, name):
    return Node(data, name)



#实现一个队列
queue = []

#根节点进入队列
queue.append(root)

#如果队列非空，循环，弹出队列第一个元素
deep = 1 #当前深度为1，根节点深度为0
while len(queue)>0:
    cur_node = queue.pop(0)
    #print(cur_node.get_deep())
    if cur_node.get_deep() < 2:  # 由于根节点记为0，所以这里的5实际上是6层
        for i in range(5):
            if deep - cur_node.get_deep() > 1:
                deep -= 1
            node = generate_node(i, "#" + str(i))
            node.set_deep(deep)
            queue.append(node)
            cur_node.add_child(node)
            deep += 1
    else:
        continue
        
def print_node(node):
    if len(node._children):
        print("  "*node.get_deep(),node.get_name(),"值="+str(node.get_data()))
        for i in node._children:
            print_node(i)
    else:
        print("  "*node.get_deep(),node.get_name(),"值="+str(node.get_data()))
# 格式化打印出树，根据层数显示
print_node(root)
