import random
import sys
import threading
import time
from json import *
import os

import template


class Node(object):
    """
    基本节点，包含节点名和节点值两个参数，还有隐藏的孩子节点和深度
    _sell_num: 节点值
    _name: 节点名
    _children: 节点的孩子节点
    _deep: 节点的深度（根节点深度为0）
    _sumsubval: 节点的所有子节点值的和
    _totalval: 节点的总值（_sumsubval+_sell_num*_price）
    _income: 该节点的薪资（收入）
    _discount: 该节点的折扣
    _price: 货源价格
    _discount_money: 折扣金额
    _total_discount: 总折扣金额
    _parent: 父节点
    """

    def __init__(self, sell_num=0, name="", price=0):
        self._sell_num = sell_num
        self._name = name
        self._children = []
        self._deep = 0
        self._sumsubval = 0
        self._totalval = 0
        self._income = 0
        self._discount = 0
        self._price = int(price)
        self._discount_money = 0
        self._total_discount = 0
        self._parent = None

    def add_child(self, obj):
        self._children.append(obj)

    def get_sell_num(self):
        return int(self._sell_num)

    def get_name(self):
        return self._name

    def get_deep(self):
        return int(self._deep)

    def get_sumsubval(self):
        return int(self._sumsubval)

    def get_parent(self):
        return self._parent

    def get_totalval(self):
        return int(self._totalval)

    def get_income(self):
        return float(self._income)

    def get_discount(self):
        return float(self._discount)

    def get_children(self):
        return self._children

    def get_discount_money(self):
        if self._price - self._discount_money != self._price:
            return self._price - self._discount_money
        else:
            return 0

    def get_price(self):
        return int(self._price)

    def set_deep(self, deep):
        self._deep = int(deep)
        return True

    def set_sumsubval(self, sell_num):
        self._sumsubval += int(sell_num)
        return True

    def set_totalval(self, sell_num):
        self._totalval = sell_num
        # 计算总值的时候将其的收益也计算出来
        self.set_income(sell_num)
        self.set_discount(sell_num)
        self.set_discount_money()
        return True

    def set_income(self, sell_num):
        # sell_num 的值按年记，_income的值也按年记
        if sell_num < 1000:
            self._income = 0
        elif 1000 <= sell_num < 6000:
            self._income = 1 * 365
        elif 6000 <= sell_num < 16000:
            self._income = 2 * 365
        elif 16000 <= sell_num < 36000:
            self._income = 3 * 365
        elif 36000 <= sell_num < 76000:
            self._income = 5 * 365
        elif 76000 <= sell_num < 156000:
            self._income = 8 * 365
        elif 156000 <= sell_num < 316000:
            self._income = 13 * 365
        elif 316000 <= sell_num < 636000:
            self._income = 21 * 365
        elif 636000 <= sell_num < 1276000:
            self._income = 34 * 365
        elif 1276000 <= sell_num:
            self._income = 55 * 365
        return True

    def set_discount(self, sell_num):
        # sell_num 的值按年记，_discount的值也按年记
        if sell_num < 1000:
            self._discount = 0
        elif 1000 <= sell_num < 6000:
            self._discount = 0.9
        elif 6000 <= sell_num < 16000:
            self._discount = 0.85
        elif 16000 <= sell_num < 36000:
            self._discount = 0.8
        elif 36000 <= sell_num < 76000:
            self._discount = 0.75
        elif 76000 <= sell_num < 156000:
            self._discount = 0.7
        elif 156000 <= sell_num < 316000:
            self._discount = 0.65
        elif 316000 <= sell_num < 636000:
            self._discount = 0.6
        elif 636000 <= sell_num < 1276000:
            self._discount = 0.55
        elif 1276000 <= sell_num:
            self._discount = 0.5
        return True

    def set_discount_money(self):
        self._discount_money = self._discount * self._price
        return True

    def set_parent(self, node):
        self._parent = node
        return True


class Tree:
    """
    通过层序遍历的方式构建一深度为deep，最大度为degree，节点值为sell_num的树，
    deep: 深度
    degree: 度
    sell_num: 节点值
    _price: 商品进货价格
    _sell_price: 商品销售价格
    _ratio: 单件商品利润率
    _total_income: 树的总薪资（劳保）
    _tree_discount: 整个树的折扣总额
    _tree_goods_total_price: 整个树的商品（按原价）总额
    status: 0 表示不处理degree和sell_num
            1 表示随机degree，不随机sell_num
            2 表示随机sell_num，不随机degree
            3 表示degree和sell_num都随机
    """

    def __init__(self, deep, degree, sell_num, price=0, ratio=0, status=0):
        self._deep = deep
        self._degree = degree
        self._sell_num = sell_num
        self._price = price
        self._ratio = ratio
        self._node_val = 0
        self._tree_discount = 0
        self._tree_goods_total_price = 0
        self._node_num = 0
        self._sell_price = 0
        self._total_income = 0

        # 保存建树结构的一个队列（用于后续进行节点值计算）
        self._nodequeue = []

        # 建树所用的一个临时队列
        queue = []

        # 根据status设置当前节点的度和子节点值
        node_deg, node_val, node_price = self.handle_deg_val(degree, sell_num, price, status)
        self._node_val = node_val
        self._sell_price = node_price * sell_num

        # 创建根节点
        self._root = Node(node_val, 'root', node_price)

        # 根节点进入队列
        queue.append(self._root)
        self._nodequeue.append(self._root)
        # 树的总节点值加1
        self._node_num += 1

        # 如果队列非空，循环，弹出队列第一个元素
        cur_deep = 1  # 当前深度为1，根节点深度为0

        while len(queue) > 0:
            cur_node = queue.pop(0)
            # print(cur_node.get_deep())
            if cur_node.get_deep() < deep:  # 由于根节点记为0，所以这里的deep实际上是deep+1层
                # print(node_deg)
                for i in node_deg:
                    if cur_deep - cur_node.get_deep() > 1:
                        cur_deep -= 1
                    # 生成节点
                    node = self.generate_node(node_val, "#" + str(i), node_price)
                    # 树的总节点值加1
                    self._node_num += 1
                    # 记录深度
                    node.set_deep(cur_deep)
                    # 记录父节点
                    node.set_parent(cur_node)
                    # 加到队列中
                    queue.append(node)
                    self._nodequeue.append(node)
                    # 追加到当前节点的子节点中
                    cur_node.add_child(node)
                    cur_deep += 1
            else:
                continue

    # 返回根节点
    def get_root(self):
        return self._root

    # 返回树的节点总数
    def get_node_num(self):
        return self._node_num

    # 返回商品实际销售价
    def get_sell_price(self):
        return self._sell_price

    # 返回单件商品利润率
    def get_ratio(self):
        return self._ratio

    # 返回树的总薪资
    def get_total_income(self):
        return self._total_income

    # 返回树的每一层第一个节点的信息。
    def get_each_node_info(self):
        node_deep = []
        nodes_queue = []
        nodes_deep = []
        temp_deep = 0
        count = 0
        last_node = self._nodequeue[-1]
        for node in self._nodequeue:
            cur_deep = node.get_deep()
            if temp_deep == cur_deep:
                count += 1
                cur_node = node
                if node == last_node:
                    nodes = {}
                    nodes['deep'] = temp_deep
                    nodes['sell_num'] = cur_node.get_sell_num()
                    nodes['price'] = cur_node.get_price()
                    nodes['income'] = cur_node.get_income()
                    nodes['discount'] = cur_node.get_discount_money()
                    nodes['total'] = cur_node.get_totalval()
                    nodes['sub_val'] = cur_node.get_sumsubval()
                    nodes['count'] = count
                    nodes_queue.append(nodes)
                    nodes_deep.append(temp_deep)
            else:
            # node_deep.append(cur_deep)
            # if cur_deep not in nodes_deep:
                nodes = {}
                nodes['deep'] = temp_deep
                nodes['sell_num'] = cur_node.get_sell_num()
                nodes['price'] = cur_node.get_price()
                nodes['income'] = cur_node.get_income()
                nodes['discount'] = cur_node.get_discount_money()
                nodes['total'] = cur_node.get_totalval()
                nodes['sub_val'] = cur_node.get_sumsubval()
                nodes['count'] = count
                nodes_queue.append(nodes)
                nodes_deep.append(temp_deep)
                temp_deep = cur_deep
                count = 1
        return nodes_queue


    # 生成节点
    @staticmethod
    def generate_node(sell_num, name, price):
        return Node(sell_num, name, price)

    # 处理节点的度和子节点的销售数量以及销售单价
    def handle_deg_val(self, deg=0, sell_num=0, price=0, stat=0):
        """
        stat: 0 表示不处理degree和sell_num
              1 表示随机degree，不随机sell_num
              2 表示随机sell_num，不随机degree
              3 表示degree和sell_num都随机
        """
        # 根据是否设置单价商品利率来调整子节点的值（商品售价）
        price += round(self._ratio / 100 * price, 2)
        #print("price: %d" % price)
        if stat == 1:
            return (range(random.randint(0, deg)), sell_num, price)
        elif stat == 2:
            return (range(deg), random.randint(0, sell_num), price)
        elif stat == 3:
            return (range(random.randint(0, deg)), random.randint(0, sell_num), price)
        return (range(deg), sell_num, price)

        # 打印这个树
    def print_tree(self, file=sys.stdout):
        self.print_node(self._root, file=file)

    # 打印一个节点
    def print_node(self, node, file=None):
        if len(node.get_children()):
            print("  " * node.get_deep() + "<ul>", node.get_name()
                  , "卖出数量=" + str(node.get_sell_num())
                  , "子经销=" + str(node.get_sumsubval())
                  , "总收入=" + str(node.get_totalval())
                  , '薪资=' + str(node.get_income())
                  , '折扣=' + str(node.get_discount_money())
                  , '商品单价=' + str(node.get_price())
                  , file=file)
            for i in node.get_children():
                self.print_node(i, file=file)
            print("  " * node.get_deep() + "</ul>", file=file)
        else:
            print("  " * node.get_deep() + "<li>", node.get_name()
                  , "卖出数量=" + str(node.get_sell_num())
                  , "子经销=" + str(node.get_sumsubval())
                  , "总收入=" + str(node.get_totalval())
                  , '薪资=' + str(node.get_income())
                  , '折扣=' + str(node.get_discount_money())
                  , '商品单价=' + str(node.get_price())
                  , file=file, end="</li>\n")

    # 根据node_queue的值计算父节点的值
    def node_queue_cal(self):
        for i in self._nodequeue[::-1]:
            # 当前节点父节点
            parent = i.get_parent()
            # 当前节点的销售数量
            sell_num = i.get_sell_num()
            # 当前节点商品售价
            price = i.get_price()
            # 当前节点的子节点值的和
            sum_sub_val = i.get_sumsubval()
            # 设置当前节点总值
            i.set_totalval(sell_num * price + sum_sub_val)
            # 当前节点的总值（子节点的和+自身的值）
            total_val = i.get_totalval()
            # 树的总薪资
            self._total_income += i.get_income()
            if parent:
                # 设置父节点的子节点值的和
                parent.set_sumsubval(total_val)

    # 获得整个树的折扣总额，和商品按照原价时的总额
    def get_tree_discount(self):
        for i in self._nodequeue[::-1]:
            self._tree_discount += i.get_discount_money()
            self._tree_goods_total_price += self._price * self._node_val
        return (self._tree_discount, self._tree_goods_total_price)


def make_tree(deep, deg, sell_num, price=0, ratio=0, mode=0):
    """
    usage: make_tree(deep, deg, sell_num[, price][, mode])

    mode:   0 表示不处理degree和sell_num
            1 表示随机degree，不随机sell_num
            2 表示随机sell_num，不随机degree
            3 表示degree和sell_num都随机
            4 表示不处理degree，穷举sell_num
            5 表示不处理degree，根据sell_num和price进行穷举

    sample: make_tree(4, 3, 10, 60, 2)
    """
    if mode == 4:
        # 穷举sell_num,新建一个生成树的队列用于多线程
        tree_queue = []
        for i in range(1, sell_num + 1):
            tree = Tree(deep, deg, i, price, ratio, 0)
            tree_queue.append(tree)

        # 调用线程处理
        multi_thread(tree_queue)
    elif mode == 5:
        # 根据sell_num和price进行组合穷举
        tree_queue = []
        for i in range(1, sell_num + 1):
            for j in range(10, ratio + 1, 10):
                tree = Tree(deep, deg, i, price, j, 0)
                tree_queue.append(tree)

        multi_thread(tree_queue)
    else:
        tree = Tree(deep, deg, sell_num, price, ratio, mode)
        calculate_tree(tree)
        write_to_file(tree, 1)


def calculate_tree(tree):
    # 计算树的节点值
    tree.node_queue_cal()


def write_to_file(tree, file_num):
    # 确定需要生成的文件数
    file_num = file_num
    # 根节点总收入
    root_total = {}
    for i in range(file_num):
        file_name = str(i) + ".html"
        with open(file_name, 'a+', encoding='utf-8') as f:
            # 输出到文件
            tree.print_tree(file=f)
            # 输出到控制台
            # tree.print_tree()
            # 根节点总收入
            root_total['root_total_val'] = tree.get_root().get_totalval()
            # 根节点总薪资
            root_total['root_total_income'] = tree.get_total_income()
            # 树的总折扣和商品原价总和
            root_total['tree_total_discount'], root_total['tree_goods_total_price'] = tree.get_tree_discount()
            # 树的实际销售额
            root_total['tree_final_goods_price'] = root_total['tree_goods_total_price'] - root_total['tree_total_discount']
            # 树的节点总数
            root_total['tree_node_num'] = tree.get_node_num()
            # 树的总利润
            root_total['tree_total_profit'] = root_total['root_total_val'] - root_total['root_total_income'] - root_total['tree_goods_total_price']
            # 树的实际商品销售单价
            root_total['tree_sell_price'] = tree.get_sell_price()
            # 当前单件商品利润率
            root_total['tree_goods_ratio'] = tree.get_ratio()
            # 树的每一层节点的信息
            root_total['tree_each_deep_infos'] = tree.get_each_node_info()

            print(tree.get_root().get_totalval())

    with open("result.txt", 'a+', encoding='utf-8') as r:
        print(JSONEncoder().encode(root_total), file=r)


def multi_thread(queue):
    """
    queue: 一个待处理的树的列表
    return: 将处理好的树的列表返回

    """
    # 活动线程数
    threads = len(threading.enumerate())

    # 保存处理好后的tree列表
    tree_result = []
    while len(queue):
        # 这个多线程其实没必要。因为计算就是线性的。线程之间没有等待时间，所以基本上都是一个线程跑完了
        if threads < 2:
            tree = queue.pop(0)
            t = threading.Thread(target=calculate_tree(tree), name='thread-' + str(threads))
            t.start()
            print('线程：' + t.getName() + '开启')
            threads = len(threading.enumerate())
            tree_result.append(tree)
        else:
            time.sleep(2)

    for i in tree_result:
        # 写入到文件
        write_to_file(i, 1)
    return tree_result


def get_final_result():
    # 读取文件，并计算最终值
    root_total_val = 0
    root_total_income = 0
    tree_total_discount = 0
    tree_goods_total_price = 0
    tree_final_goods_price = 0
    tree_total_profit = 0
    with open("result.txt") as f:
        for line in f:
            line = JSONDecoder().decode(line)
            root_total_val += line['root_total_val']
            root_total_income += line['root_total_income']
            tree_total_discount += line['tree_total_discount']
            tree_goods_total_price += line['tree_goods_total_price']
            tree_final_goods_price += line['tree_final_goods_price']
            tree_total_profit += line['tree_total_profit']
    print("总收入：" + str(root_total_val)
          , "总薪资：" + str(root_total_income)
          , "总折扣：" + str(tree_total_discount)
          , "商品总价：" + str(tree_goods_total_price)
          , "商品总价：" + str(tree_final_goods_price)
          , "总利润：" + str(tree_total_profit)
          , sep="  ")


def start(deep, degree, sell_num, price, ratio, mode):
    make_tree(deep, degree, sell_num, price, ratio, mode)
    # make_tree(4, 10, 100, 60, 4)
    get_final_result()

    # 生成图标。生成的文件名为chart.html
    # 注意：如果想要查看单次的图表生成记录，需要把result.txt文件先删除。否则每次生成的记录会累加进result.txt文件
    template.canvas()
    time.sleep(2)
    os.startfile("chart.html")


if __name__ == "__main__":
    """
    usage: make_tree(deep, degree, sell_num[, price][, ratio][, mode])
    sample: make_tree(4, 2, 100, 60, 0, 4)
    mode:   0 表示不处理degree和sell_num
            1 表示随机degree，不随机sell_num
            2 表示随机sell_num，不随机degree
            3 表示degree和sell_num都随机
            4 表示不处理degree，穷举sell_num
    note: 默认会在脚本文件夹下面创建一个0.html的文件，以及一个result.txt文件。
          0.html为类似于树的结构
          result.txt存放的是每一个树结构对应的root的总收入情况
          每次运行的结果都会追加到这两个文件中
    """
    tips = """"
    mode:   0 表示不处理degree和sell_num
            1 表示随机degree，不随机sell_num
            2 表示随机sell_num，不随机degree
            3 表示degree和sell_num都随机
            4 表示不处理degree，穷举sell_num
            请选择模式：
           """
    mode = int(input(tips))
    print(mode, type(mode))
    if mode == 4:
        print(mode)
        confirm = input("穷举模式需要清除原始的result.txt文件和0.html文件，确认清除吗？（Y/N）")
        if confirm.lower() == "y":
            target_files = ['result.txt', '0.html']
            for file in target_files:
                if os.path.isfile(file):
                    os.remove(file)
                    print(file + " 已删除")
                else:
                    make_tree(4, 10, 100, 60, 0, mode)
            print("删除完成.")
            make_tree(4, 3, 100, 60, 0, mode)
        else:
            exit()
    else:
        make_tree(4, 2, 10, 100, 10, mode)
    # make_tree(4, 10, 100, 60, 4)
    get_final_result()

    # 生成图标。生成的文件名为chart.html
    # 注意：如果想要查看单次的图表生成记录，需要把result.txt文件先删除。否则每次生成的记录会累加进result.txt文件
    template.canvas()
    time.sleep(2)
    os.startfile("chart.html")