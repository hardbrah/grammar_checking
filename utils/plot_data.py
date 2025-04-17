import matplotlib.pyplot as plt
import numpy as np

# 🎨 饼状图：显示百分比 + 数值
def autopct_format(pct, allvals):
    total = sum(allvals)
    absolute = int(round(pct * total / 100.0))
    return f"{pct:.1f}%\n({absolute})"

def plot_pie(data:list[dict], title = "Operation Distribution (Pie Chart)", color="skyblue", file_path="images/pie_chart.png"):
    """
    绘制饼图
    :param data: 数据字典，键为标签，值为数值
    :param title: 图表标题
    :param color: 饼图颜色
    """
    def autopct_format(pct, allvals):
        total = sum(allvals)
        absolute = int(round(pct * total / 100.0))
        return f"{pct:.1f}%\n({absolute})"
    plt.figure(figsize=(8, 8))
    plt.pie(data.values(), labels=data.keys(),
            autopct=lambda pct: autopct_format(pct, list(data.values())),
            startangle=140)
    plt.title(title)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
    
def plot_bar(data:list[dict], title = "Statistics Overview (Bar Chart)", color="skyblue", file_path="images/bar_chart.png"):
    """
    绘制条形图
    :param data: 数据字典，键为标签，值为数值
    :param title: 图表标题
    :param color: 条形图颜色
    """
    plt.figure(figsize=(10, 6))
    bars = plt.bar(data.keys(), data.values(), color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Count')
    plt.title('Statistics Overview (Bar Chart)')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 500, f'{yval}', ha='center', va='bottom')  # 在条形上方添加数据标签
    plt.tight_layout()
    plt.savefig(file_path)  # ✅ 保存图像
    plt.close()
    
def plot_line(data_x:list, data_y:list, x_label="token length", y_label="modift times", title="relationship between token length and modify times", file_path="images/line_chart.png"):
    plt.plot(data_x, data_y, marker='o', linestyle='-', color='b', label='token length vs modify times')

    # 添加标题和标签
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.grid(True)
    plt.savefig(file_path)  # ✅ 保存图像
    # 显示图像
    plt.close()
    
def plot_scatter(data_x:list, data_y:list, x_label="token length", y_label="modift times", title="relationship between token length and modify times", file_path="images/scatter_chart.png"):
    plt.scatter(data_x, data_y, color='b', alpha=0.5)
    
    x_min, x_max = min(data_x), max(data_x)
    x_ref = np.linspace(x_min, x_max, 100)
    plt.plot(x_ref, x_ref, color='red', linestyle='--', label='y = x')

    # 添加标题和标签
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.grid(True)
    plt.savefig(file_path)  # ✅ 保存图像
    # 显示图像
    plt.close()