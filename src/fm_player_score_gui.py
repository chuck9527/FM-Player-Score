import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import datetime
from html.parser import HTMLParser

ATTRIBUTE_WEIGHTS = {
    '传球': { 'w1': 0.7000, 'w2': -0.0833, 'w3': 0.4667, 'w2_sp': None, 'w3_sp': None },
    '传中': { 'w1': 0.5800, 'w2': -0.4000, 'w3': 0.4167, 'w2_sp': None, 'w3_sp': None },
    '盯人': { 'w1': 0.1600, 'w2': -0.2717, 'w3': 0.5500, 'w2_sp': None, 'w3_sp': None },
    '点球': { 'w1': 0.0000, 'w2': 0.0000, 'w3': 0.0000, 'w2_sp': None, 'w3_sp': None },
    '技术': { 'w1': -0.7200, 'w2': 0.0167, 'w3': 0.3833, 'w2_sp': None, 'w3_sp': None },
    '角球': { 'w1': 0.0000, 'w2': 0.0000, 'w3': 0.0000, 'w2_sp': None, 'w3_sp': None },
    '界外球': { 'w1': 0.0000, 'w2': 0.0000, 'w3': 0.0000, 'w2_sp': None, 'w3_sp': None },
    '盘带': { 'w1': 1.2000, 'w2': 1.5333, 'w3': 1.3667, 'w2_sp': None, 'w3_sp': None },
    '抢断': { 'w1': 0.7000, 'w2': -0.6167, 'w3': 0.5000, 'w2_sp': None, 'w3_sp': None },
    '任意球': { 'w1': 0.0000, 'w2': 0.0000, 'w3': 0.0000, 'w2_sp': None, 'w3_sp': None },
    '射门': { 'w1': 1.0600, 'w2': 0.3667, 'w3': 0.6667, 'w2_sp': None, 'w3_sp': None },
    '停球': { 'w1': -0.1200, 'w2': 0.0167, 'w3': 0.6333, 'w2_sp': None, 'w3_sp': None },
    '头球': { 'w1': 0.4600, 'w2': -0.0833, 'w3': 0.4667, 'w2_sp': None, 'w3_sp': None },
    '远射': { 'w1': 0.2400, 'w2': 0.0833, 'w3': 0.8333, 'w2_sp': None, 'w3_sp': None },
    '才华': { 'w1': -0.22, 'w2': 0, 'w3': 0, 'w2_sp': -0.125, 'w3_sp': 0.175 },
    '位置': { 'w1': 1.4200, 'w2': -0.4333, 'w3': 0.6667, 'w2_sp': None, 'w3_sp': None },
    '投入': { 'w1': 8.84, 'w2': 0, 'w3': 0, 'w2_sp': 2.2, 'w3_sp': 0.75 },
    '集中': { 'w1': 3.0000, 'w2': 0.7500, 'w3': 0.6833, 'w2_sp': None, 'w3_sp': None },
    '决断': { 'w1': 0.6000, 'w2': -0.7667, 'w3': 0.3667, 'w2_sp': None, 'w3_sp': None },
    '领导力': { 'w1': -0.82, 'w2': 0, 'w3': 0, 'w2_sp': 0.275, 'w3_sp': 0.4 },
    '侵略': { 'w1': 1.08, 'w2': 0, 'w3': 0, 'w2_sp': 0.225, 'w3_sp': 0.2625 },
    '视野': { 'w1': 1.4000, 'w2': -0.6500, 'w3': 0.2000, 'w2_sp': None, 'w3_sp': None },
    '合作': { 'w1': 0.4, 'w2': 0, 'w3': 0, 'w2_sp': -0.625, 'w3_sp': 0.1125 },
    '无球跑': { 'w1': 0.0400, 'w2': -0.0333, 'w3': 0.2667, 'w2_sp': None, 'w3_sp': None },
    '意志': { 'w1': 1.48, 'w2': 0, 'w3': 0, 'w2_sp': -0.125, 'w3_sp': 0.5875 },
    '勇敢': { 'w1': -0.04, 'w2': 0, 'w3': 0.175, 'w2_sp': -0.4, 'w3_sp': None },
    '预判': { 'w1': 1.4600, 'w2': 0.8833, 'w3': 0.9000, 'w2_sp': None, 'w3_sp': None },
    '镇定': { 'w1': 1.5400, 'w2': 0.1333, 'w3': 0.3667, 'w2_sp': None, 'w3_sp': None },
    '爆发': { 'w1': 4.9250, 'w2': 7.2083, 'w3': 4.7292, 'w2_sp': None, 'w3_sp': None },
    '弹跳': { 'w1': 0.8400, 'w2': 1.3833, 'w3': 2.6000, 'w2_sp': None, 'w3_sp': None },
    '灵活': { 'w1': 3.1000, 'w2': -0.3333, 'w3': 0.9667, 'w2_sp': None, 'w3_sp': None },
    '耐力': { 'w1': 2.5600, 'w2': 0.8333, 'w3': 0.5167, 'w2_sp': None, 'w3_sp': None },
    '平衡': { 'w1': 0.6600, 'w2': 1.6833, 'w3': 1.1667, 'w2_sp': None, 'w3_sp': None },
    '强壮': { 'w1': -0.4000, 'w2': 1.2833, 'w3': 0.9500, 'w2_sp': None, 'w3_sp': None },
    '速度': { 'w1': 5.9250, 'w2': 6.2292, 'w3': 4.8750, 'w2_sp': None, 'w3_sp': None },
    '体质': { 'w1': 0.9400, 'w2': 1.5333, 'w3': 0.3000, 'w2_sp': None, 'w3_sp': None },
    '稳定': { 'w1': 0.1, 'w2': 0, 'w3': 0, 'w2_sp': 0.3, 'w3_sp': 0.425 },
    '大赛发挥': { 'w1': 0.44, 'w2': 0, 'w3': 0, 'w2_sp': 0.125, 'w3_sp': 0.375 },
    '抗压': { 'w1': 3.64, 'w2': 0, 'w3': 0, 'w2_sp': 0.55, 'w3_sp': 0.8375 }
}

OPTIONAL_ATTRIBUTES = ['稳定', '大赛发挥', '抗压']

HTML_ATTR_MAPPING = {
    '球员': '球员',
    '投入': '投入', '速度': '速度', '爆发': '爆发', '盘带': '盘带', '弹跳': '弹跳',
    '平衡': '平衡', '预判': '预判', '集中': '集中', '灵活': '灵活', '意志': '意志',
    '制空': '制空', '指挥': '指挥', '镇定': '镇定', '远射': '远射', '勇敢': '勇敢',
    '意外': '意外', '一对一': '一对一', '无球跑': '无球跑', '合作': '合作', '头球': '头球',
    '停球': '停球', '体质': '体质', '手抛球': '手抛球', '手控球': '手控球', '视野': '视野',
    '射门': '射门', '任意球': '任意球', '击球': '击球', '侵略': '侵略', '抢断': '抢断',
    '强壮': '强壮', '耐力': '耐力', '领导力': '领导力', '拦截传中': '拦截传中', '决断': '决断',
    '界外球': '界外球', '角球': '角球', '技术': '技术', '位置': '位置', '反应': '反应',
    '点球': '点球', '盯人': '盯人', '开球': '开球', '传中': '传中', '传球': '传球',
    '出击': '出击', '才华': '才华'
}

REQUIRED_ATTRIBUTES = list(ATTRIBUTE_WEIGHTS.keys())

def clean_text(text):
    text = text.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    text = text.replace(' - 选择球员', '').replace('- 选择球员', '')
    return text.strip()

def calculate_score(value, weights):
    w1 = weights['w1']
    w2 = weights['w2']
    w3 = weights['w3']
    w2_sp = weights['w2_sp']
    w3_sp = weights['w3_sp']
    
    if w2_sp is not None:
        if value <= 6:
            return (value - 1) * w1
        elif value <= 10:
            return 5 * w1 + (value - 4) * w2_sp
        else:
            final_w3 = w3_sp if w3_sp is not None else w3
            return 5 * w1 + 4 * w2_sp + (value - 10) * final_w3
    else:
        if value <= 6:
            return (value - 1) * w1
        elif value <= 12:
            return 5 * w1 + (value - 6) * w2
        else:
            return 5 * w1 + 6 * w2 + (value - 12) * w3

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_th = False
        self.in_td = False
        self.headers = []
        self.rows = []
        self.current_row = []
        self.current_cell = ""
        
    def handle_starttag(self, tag, attrs):
        if tag == 'th':
            self.in_th = True
            self.current_cell = ""
        elif tag == 'td':
            self.in_td = True
            self.current_cell = ""
        elif tag == 'tr':
            self.current_row = []
    
    def handle_endtag(self, tag):
        if tag == 'th':
            self.in_th = False
            self.headers.append(clean_text(self.current_cell))
        elif tag == 'td':
            self.in_td = False
            self.current_row.append(clean_text(self.current_cell))
        elif tag == 'tr' and self.current_row:
            self.rows.append(self.current_row)
    
    def handle_data(self, data):
        if self.in_th or self.in_td:
            self.current_cell += data

class FMPlayerScoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FM球员评分工具")
        self.root.geometry("1200x700")
        
        self.data_file = "players_data.json"
        self.players_data = []
        self.sort_column = None
        self.sort_reverse = False
        
        self.load_data()
        self.create_widgets()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.players_data = json.load(f)
            except:
                self.players_data = []
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.players_data, f, ensure_ascii=False, indent=2)
    
    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="选择HTML文件:").pack(side=tk.LEFT)
        self.html_path = tk.StringVar()
        ttk.Entry(top_frame, textvariable=self.html_path, width=60).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="浏览...", command=self.browse_html).pack(side=tk.LEFT)
        ttk.Button(top_frame, text="导入", command=self.import_file).pack(side=tk.LEFT, padx=20)
        ttk.Button(top_frame, text="清空数据", command=self.clear_all).pack(side=tk.LEFT)
        
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_tree()
    
    def create_tree(self):
        columns = ['姓名', '评分'] + REQUIRED_ATTRIBUTES
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')
        
        self.tree.heading('姓名', text='姓名', command=lambda: self.sort_by('姓名'))
        self.tree.heading('评分', text='评分', command=lambda: self.sort_by('评分'))
        
        for attr in REQUIRED_ATTRIBUTES:
            self.tree.heading(attr, text=attr, command=lambda a=attr: self.sort_by(a))
        
        self.tree.column('姓名', width=150)
        self.tree.column('评分', width=100)
        for attr in REQUIRED_ATTRIBUTES:
            self.tree.column(attr, width=50)
        
        scrollbar_y = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        self.tree.bind('<Double-Button-1>', self.on_tree_click)
    
    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            item_id = self.tree.identify("row", event.x, event.y)
            
            player_idx = self.tree.get_children().index(item_id)
            
            if player_idx < len(self.players_data):
                player = self.players_data[player_idx]
                self.open_edit_dialog(player, player_idx)
    
    def open_edit_dialog(self, player, player_idx):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"编辑球员: {player['name']}")
        dialog.geometry("600x700")
        dialog.transient(self.root)
        
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"球员: {player['name']}", font=('Arial', 14, 'bold')).pack(pady=10)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding="10")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.entry_vars = {}
        
        for i, attr in enumerate(REQUIRED_ATTRIBUTES):
            row = i // 2
            col = i % 2
            
            frame = ttk.Frame(scrollable_frame)
            frame.grid(row=row, column=col, sticky='w', padx=10, pady=5)
            
            current_value = player['attributes'].get(attr, '')
            
            if current_value:
                var = tk.StringVar(value=str(current_value))
            else:
                var = tk.StringVar(value="")
            
            label_text = attr
            if attr not in OPTIONAL_ATTRIBUTES:
                label_text += " *"
            
            label = ttk.Label(frame, text=label_text + ":", width=15, anchor='e')
            label.pack(side=tk.LEFT)
            
            entry = ttk.Entry(frame, textvariable=var, width=10)
            entry.pack(side=tk.LEFT, padx=5)
            
            self.entry_vars[attr] = var
            
            if not current_value and attr not in OPTIONAL_ATTRIBUTES:
                label.config(foreground='red')
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        btn_frame = ttk.Frame(dialog, padding="10")
        btn_frame.pack(fill=tk.X)
        
        ttk.Label(btn_frame, text="* 为必填项", foreground='red').pack(side=tk.LEFT)
        
        def save():
            has_missing = False
            
            for attr, var in self.entry_vars.items():
                new_value = var.get().strip()
                
                if new_value:
                    try:
                        val = int(new_value)
                        if val < 1 or val > 20:
                            messagebox.showwarning("警告", f"{attr}值必须在1-20之间")
                            return
                        self.players_data[player_idx]['attributes'][attr] = val
                    except ValueError:
                        messagebox.showerror("错误", f"{attr}请输入有效的数字")
                        return
                else:
                    self.players_data[player_idx]['attributes'].pop(attr, None)
                    if attr not in OPTIONAL_ATTRIBUTES:
                        has_missing = True
            
            if not has_missing and self.is_data_complete(self.players_data[player_idx]['attributes']):
                self.players_data[player_idx]['score'] = self.calculate_total_score(
                    self.players_data[player_idx]['attributes']
                )
            else:
                self.players_data[player_idx]['score'] = None
            
            self.save_data()
            self.refresh_tree()
            dialog.destroy()
        
        ttk.Button(btn_frame, text="保存", command=save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def browse_html(self):
        filename = filedialog.askopenfilename(title="选择HTML文件", filetypes=[("HTML文件", "*.html"), ("所有文件", "*.*")])
        if filename:
            self.html_path.set(filename)
    
    def parse_html_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            parser = TableParser()
            parser.feed(content)
            
            if not parser.headers or not parser.rows:
                return []
            
            header_map = {}
            for i, h in enumerate(parser.headers):
                h_clean = clean_text(h)
                if h_clean in HTML_ATTR_MAPPING:
                    header_map[i] = HTML_ATTR_MAPPING[h_clean]
            
            players = []
            for row in parser.rows:
                if len(row) < len(header_map):
                    continue
                
                player_name = row[0] if row else ""
                if not player_name:
                    continue
                
                player_name = clean_text(player_name)
                
                attributes = {}
                for idx, attr_name in header_map.items():
                    if idx < len(row):
                        val_str = row[idx]
                        if attr_name != '球员' and val_str.isdigit():
                            attributes[attr_name] = int(val_str)
                
                if len(attributes) >= 10:
                    players.append({
                        'name': player_name,
                        'attributes': attributes
                    })
            
            return players
        except Exception as e:
            print(f"解析错误: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def is_data_complete(self, attributes):
        for attr in REQUIRED_ATTRIBUTES:
            if attr not in attributes and attr not in OPTIONAL_ATTRIBUTES:
                return False
        return True
    
    def validate_attributes(self, attributes):
        missing = []
        for attr in REQUIRED_ATTRIBUTES:
            if attr not in attributes and attr not in OPTIONAL_ATTRIBUTES:
                missing.append(attr)
        return missing
    
    def calculate_total_score(self, attributes):
        total = 0
        for attr, value in attributes.items():
            if attr in ATTRIBUTE_WEIGHTS:
                total += calculate_score(value, ATTRIBUTE_WEIGHTS[attr])
        
        has_all_required = all(attr in attributes for attr in REQUIRED_ATTRIBUTES if attr not in OPTIONAL_ATTRIBUTES)
        
        if not has_all_required:
            return None
        
        return total
    
    def import_file(self):
        html_path = self.html_path.get()
        
        if not html_path:
            messagebox.showwarning("警告", "请选择HTML文件")
            return
        
        players = self.parse_html_file(html_path)
        
        if not players:
            messagebox.showerror("错误", "无法解析HTML文件或文件中没有球员数据")
            return
        
        imported_count = 0
        for player in players:
            score = self.calculate_total_score(player['attributes'])
            
            player_data = {
                'name': player['name'],
                'attributes': player['attributes'],
                'score': score,
                'import_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.players_data.append(player_data)
            imported_count += 1
        
        if imported_count > 0:
            self.save_data()
            self.refresh_tree()
            messagebox.showinfo("成功", f"成功导入 {imported_count} 名球员!")
        else:
            messagebox.showwarning("警告", "没有可导入的球员数据")
    
    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for player in self.players_data:
            if player.get('score') is not None:
                score_str = f"{player['score']:.2f}"
            else:
                score_str = "缺少数据"
            
            values = [player['name'], score_str]
            
            for attr in REQUIRED_ATTRIBUTES:
                attr_value = player.get('attributes', {}).get(attr, '-')
                values.append(attr_value if attr_value == '-' else str(attr_value))
            
            self.tree.insert("", tk.END, values=values)
    
    def sort_by(self, column):
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        if column == '姓名':
            self.players_data.sort(key=lambda x: x['name'], reverse=self.sort_reverse)
        elif column == '评分':
            self.players_data.sort(key=lambda x: x.get('score', 0) or 0, reverse=self.sort_reverse)
        else:
            self.players_data.sort(
                key=lambda x: x.get('attributes', {}).get(column, 0),
                reverse=self.sort_reverse
            )
        
        self.refresh_tree()
    
    def clear_all(self):
        if messagebox.askyesno("确认", "确定要清空所有数据吗?"):
            self.players_data = []
            self.save_data()
            self.refresh_tree()
            messagebox.showinfo("成功", "已清空所有数据")

def main():
    root = tk.Tk()
    app = FMPlayerScoreApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
