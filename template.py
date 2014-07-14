
from json import *


def add_header_str_begin():
    return "<!DOCTYPE html>" + "<html>" + \
           "<head>" + \
           "<meta http-equiv=\"Content-Type\" content=text/html; charset=utf-8>" + \
           "<script src='chart.min.js'></script>" + \
           "</head>"


def add_style():
    return "<style>" \
           ".tips-wrap{margin: 20px auto; width:100%; height: 100%}" \
           ".tips-wrap>div{display:inline-block;vertical-align: middle;}" \
           ".chart-line{width: 50px;height: 4px;position: relative;margin-right: 20px}" \
           ".node-chart{margin-top: 20px}" \
           "</style>"


body_begin = "<body>"

canvas_wrap = "<div class='tips-wrap'>\
                <div style=''>总销售额</div>" \
              "<div class='chart-line' style='background-color: rgba(0,142,200,1)'></div>" \
              "<div style=''>总利润</div>" \
              "<div class='chart-line' style='background-color: rgba(81,180,67,1)'></div>" \
              "<div style=''>总折扣</div>" \
              "<div class='chart-line' style='background-color: rgba(237,126,23,1)'></div>" \
              "<div style=''>商品实际总价（除去折扣后，经销商购买的价格）</div>" \
              "<div class='chart-line' style='background-color: rgba(96,8,254,1)'></div>" \
              "</div>"


def add_canvas(name):
    return "<canvas id=" + name + " width=23920 height=300px></canvas>"


def add_div(content, class_name="", style=""):
    return "<div class=" + class_name + " style='" + style + "'>" \
           + content + \
           "</div>"


def add_input(type, id="", value=0, class_name="", style="", placeholder=""):
    return "<input type='" + type + "' id='" + id + "' class='" + class_name + "' value='" + str(value) + "' style='" + \
           style + "' placeholder='" + placeholder + "' >"


body_end = "</body>"


def add_script(script):
    return "<script>" \
           + script + \
           "</script>"


header_str_end = "</html>"


def canvas():
    with open("result.txt") as f:
        # count = 0
        # labels = []
        # 总销售额
        root_total_val = []
        # 总利润
        root_total_income = []
        # 总折扣
        tree_total_discount = []
        # 商品进货总价
        tree_goods_total_price = []
        # 商品实际总价
        tree_final_goods_price = []
        # 树的总利润
        tree_total_profit = []
        # 节点数
        tree_node_num = []
        # 商品单价
        tree_sell_price = []
        # 单件商品利润率
        tree_goods_ratio = []
        # 每层的总的节点信息
        tree_each_deep_infos = []

        for line in f:
            #count += 1
            line = JSONDecoder().decode(line)
            tree_sell_price.append(line['tree_sell_price'])
            root_total_val.append(line['root_total_val'])
            root_total_income.append(line['root_total_income'])
            tree_total_discount.append(line['tree_total_discount'])
            tree_goods_total_price.append(line['tree_goods_total_price'])
            tree_final_goods_price.append(line['tree_final_goods_price'])
            tree_node_num.append(line['tree_node_num'])
            tree_total_profit.append(line['tree_total_profit'])
            tree_goods_ratio.append(line['tree_goods_ratio'])  # 可以改进
            tree_each_deep_infos.append(line['tree_each_deep_infos'])

        # 每层节点的深度
        node_deep = []
        # 每层节点的深度
        node_sell_num = []
        # 每层节点的深度
        node_price = []
        # 每层节点的深度
        node_income = []
        # 每层节点的深度
        node_discount = []
        # 每层节点的深度
        node_total = []
        # 每层节点的深度
        node_sub_val = []
        # 每层节点的数目
        node_count = []
        for infos in tree_each_deep_infos:
            for info in infos:
                node_deep.append(info['deep'])
                node_sell_num.append(info['sell_num'])
                node_price.append(info['price'])
                node_income.append(info['income'])
                node_discount.append(info['discount'])
                node_total.append(info['total'])
                node_sub_val.append(info['sub_val'])
                node_count.append(info['count'])

    with open("chart.html", "w+", encoding="utf-8") as c:
        c.write(add_header_str_begin())
        c.write(body_begin)
        c.write(add_style())

        c.write(canvas_wrap)
        c.write(add_canvas("chart"))
        script = ("\n" + 'var data = {\
				            labels:' + str(tree_sell_price) + ',\
				            datasets: [\
					            {\
						            fillColor : "rgba(0,142,200,1)",\
						            strokeColor : "rgba(0,142,200,1)",\
						            data:' + str(root_total_val) + '\
					            },\
					            {\
						            fillColor : "rgba(81,180,67,1)",\
						            strokeColor: "rgba(81,180,67,1)",\
						            data:' + str(root_total_income) + '\
					            },\
					            {\
						            fillColor : "rgba(237,126,23,1)",\
						            strokeColor: "rgba(237,126,23,1)",\
						            data:' + str(tree_total_discount) + '\
					            },\
					            {\
						            fillColor : "rgba(96,8,254,1)",\
						            strokeColor: "rgba(96,8,254,1)",\
						            data:' + str(tree_final_goods_price) + '\
					            }\
				            ]\
			            }\
			            ' + "\n" + 'var ctx = document.getElementById("chart").getContext("2d");\
			            ' + "\n" + 'var myNewChart = new Chart(ctx).Bar(data);')

        c.write(add_script(script))

        c.write(add_div(add_div("节点总数", "") +
                        add_div("", "chart-line", "background-color: rgba(0,142,200,1)") +
                        add_div("商品总进价", "") +
                        add_div("", "chart-line", "background-color: rgba(96,8,254,1)") +
                        add_div("最终盈利", "") +
                        add_div("", "chart-line", "background-color: rgba(239,75,75,1)") +
                        add_div("单件商品利润率：") +
                        add_div("", "chart-line", "background-color: rgba(139, 175, 75,1)"), "tips-wrap"))

        c.write(add_canvas("chart_node"))
        script_node = ("\n" + 'var node_data = {\
				            labels:' + str(tree_sell_price) + ',\
				            datasets: [\
					            {\
						            fillColor : "rgba(0,142,200,1)",\
						            strokeColor : "rgba(0,142,200,1)",\
						            data:' + str(tree_node_num) + '\
					            },\
					            {\
						            fillColor : "rgba(96,8,254,1)",\
						            strokeColor: "rgba(96,8,254,1)",\
						            data:' + str(tree_goods_total_price) + '\
					            },\
					            {\
						            fillColor : "rgba(239, 75, 75,1)",\
						            strokeColor: "rgba(239, 75, 75,1)",\
						            data:' + str(tree_total_profit) + '\
					            },\
					            {\
						            fillColor : "rgba(139, 175, 75,1)",\
						            strokeColor: "rgba(139, 175, 75,1)",\
						            data:' + str(tree_goods_ratio) + '\
					            }\
				            ]\
			            }\
			            ' + "\n" + 'var ctx = document.getElementById("chart_node").getContext("2d");\
			            ' + "\n" + 'var myNewChart = new Chart(ctx).Bar(node_data);')
        c.write(add_script(script_node))

        c.write(add_div(add_div("最终盈利", "") +
                        add_div("", "chart-line", "background-color: rgba(239,75,75,1)") +
                        add_div("单件商品利润率：") +
                        add_div("", "chart-line", "background-color: rgba(139,175,75,1)"), "tips-wrap"))

        c.write(add_canvas("chart_profile"))
        script_profile = ("\n" + 'var profile_data = {\
				            labels:' + str(tree_sell_price) + ',\
				            datasets: [\
					            {\
						            fillColor : "rgba(239, 75, 75,0)",\
						            strokeColor: "rgba(239, 75, 75,1)",\
                                    pointColor : "rgba(239, 75, 75,1)",\
						            data:' + str(tree_total_profit) + '\
					            },\
					            {\
						            fillColor : "rgba(139, 175, 75,0)",\
						            strokeColor: "rgba(139, 175, 75,1)",\
                                    pointColor : "rgba(139, 175, 75,1)",\
						            data:' + str(tree_goods_ratio) + '\
					            }\
				            ]\
			            }\
			            ' + "\n" + 'var ctx = document.getElementById("chart_profile").getContext("2d");\
			            ' + "\n" + 'var myNewChart = new Chart(ctx).Line(profile_data, {bezierCurve: false});')
        c.write(add_script(script_profile))

        # ***********************************************************************************
        c.write(add_div(add_div("销售数量", "") +
                        add_div("", "chart-line", "background-color: rgba(96,8,254,1)") +
                        add_div("销售单价", "") +
                        add_div("", "chart-line", "background-color: rgba(239,75,75,1)") +
                        add_div("劳保薪资", "") +
                        add_div("", "chart-line", "background-color: rgba(81,180,67,1)") +
                        add_div("总销售", "") +
                        add_div("", "chart-line", "background-color: rgba(60,100,100,1)") +
                        add_div("子销售", "") +
                        add_div("", "chart-line", "background-color: rgba(139,75,75,1)") +
                        add_div("节点个数", "") +
                        add_div("", "chart-line", "background-color: rgba(139,139,139,1)"), "tips-wrap"))

        c.write(add_canvas("chart_deep_nodes"))
        script_node = ("\n" + 'var deep_nodes_data = {\
				            labels:' + str(node_deep) + ',\
				            datasets: [\
					            {\
						            fillColor : "rgba(96,8,254,1)",\
						            strokeColor: "rgba(96,8,254,1)",\
						            data:' + str(node_sell_num) + '\
					            },\
					            {\
						            fillColor : "rgba(239, 75, 75,1)",\
						            strokeColor: "rgba(239, 75, 75,1)",\
						            data:' + str(node_price) + '\
					            },\
					            {\
						            fillColor : "rgba(81,180,67,1)",\
						            strokeColor: "rgba(81,180,67,1)",\
						            data:' + str(node_income) + '\
					            },\
					            {\
						            fillColor : "rgba(60,100,100,1)",\
						            strokeColor: "rgba(60,100,100,1)",\
						            data:' + str(node_total) + '\
					            },\
					            {\
						            fillColor : "rgba(139,75,75,1)",\
						            strokeColor: "rgba(139,75,75,1)",\
						            data:' + str(node_sub_val) + '\
					            },\
					            {\
						            fillColor : "rgba(139,139,139,1)",\
						            strokeColor: "rgba(139,139,139,1)",\
						            data:' + str(node_count) + '\
					            }\
				            ]\
			            }\
			            ' + "\n" + 'var ctx = document.getElementById("chart_deep_nodes").getContext("2d");\
			            ' + "\n" + 'var myNewChart = new Chart(ctx).Bar(deep_nodes_data);')
        c.write(add_script(script_node))

        c.write(header_str_end)


if __name__ == "__main__":
    canvas()