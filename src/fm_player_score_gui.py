import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import os
import datetime
from html.parser import HTMLParser
from score_calculator import ATTRIBUTE_WEIGHTS, REQUIRED_ATTRIBUTES, calculate_total_score, calculate_score, HIDDEN_ATTRIBUTES

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
    '出击': '出击', '才华': '才华',
    '姓名': '球员', '角球': '角球', '传中': '传中', '盘带': '盘带', '射门': '射门',
    '停球': '停球', '任意球': '任意球', '头球': '头球', '远射': '远射', '界外球': '界外球',
    '盯人': '盯人', '传球': '传球', '点球': '点球', '抢断': '抢断', '技术': '技术',
    '侵略性': '侵略', '预判': '预判', '勇敢': '勇敢', '镇定': '镇定', '集中': '集中',
    '决断力': '决断', '意志力': '意志', '才华': '才华', '领导力': '领导力', '无球跑动': '无球跑',
    '防守站位': '位置', '团队合作': '合作', '视野': '视野', '工作投入': '投入', '爆发力': '爆发',
    '灵活': '灵活', '平衡': '平衡', '弹跳': '弹跳', '体质': '体质', '速度': '速度',
    '耐力': '耐力', '强壮': '强壮', '状态稳定性': '稳定', '大赛发挥': '大赛发挥', '抗压能力': '抗压'
}

REQUIRED_ATTRIBUTES = list(ATTRIBUTE_WEIGHTS.keys())

def clean_text(text):
    text = text.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    text = text.replace(' - 选择球员', '').replace('- 选择球员', '')
    return text.strip()

import re

class TableParser:
    def __init__(self):
        self.headers = []
        self.rows = []
        
    def feed(self, html):
        header_pattern = re.compile(r'<th[^>]*>([^<]*)</th>', re.IGNORECASE)
        td_pattern = re.compile(r'<t[dh][^>]*>([^<]*)</t[dh]>', re.IGNORECASE)
        
        thead_match = re.search(r'<thead[^>]*>(.*?)</thead>', html, re.DOTALL | re.IGNORECASE)
        if thead_match:
            thead_content = thead_match.group(1)
            self.headers = [clean_text(m.group(1)) for m in header_pattern.finditer(thead_content)]
        
        tbody_match = re.search(r'<tbody[^>]*>(.*?)</tbody>', html, re.DOTALL | re.IGNORECASE)
        if tbody_match:
            tbody_content = tbody_match.group(1)
            tr_matches = re.finditer(r'<tr[^>]*>(.*?)</tr>', tbody_content, re.DOTALL | re.IGNORECASE)
            for tr_match in tr_matches:
                tr_content = tr_match.group(1)
                cells = [clean_text(m.group(1)) for m in td_pattern.finditer(tr_content)]
                if cells:
                    self.rows.append(cells)

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score REAL,
                normal_score REAL,
                hidden_score REAL,
                import_time TEXT,
                attributes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_all_players(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM players ORDER BY id')
        rows = cursor.fetchall()
        conn.close()
        
        players = []
        for row in rows:
            import json
            attributes = json.loads(row['attributes']) if row['attributes'] else {}
            players.append({
                'id': row['id'],
                'name': row['name'],
                'score': row['score'],
                'normal_score': row['normal_score'],
                'hidden_score': row['hidden_score'],
                'import_time': row['import_time'],
                'attributes': attributes
            })
        
        return players
    
    def add_player(self, name, score, normal_score, hidden_score, import_time, attributes):
        import json
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO players (name, score, normal_score, hidden_score, import_time, attributes) VALUES (?, ?, ?, ?, ?, ?)',
            (name, score, normal_score, hidden_score, import_time, json.dumps(attributes))
        )
        
        conn.commit()
        conn.close()
    
    def update_player(self, player_id, name, attributes, score, normal_score, hidden_score):
        import json
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE players SET name = ?, attributes = ?, score = ?, normal_score = ?, hidden_score = ? WHERE id = ?',
            (name, json.dumps(attributes), score, normal_score, hidden_score, player_id)
        )
        
        conn.commit()
        conn.close()
    
    def delete_player(self, player_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM players WHERE id = ?', (player_id,))
        
        conn.commit()
        conn.close()
    
    def clear_all(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM players')
        
        conn.commit()
        conn.close()

class FMPlayerScoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FM球员评分工具")
        self.root.geometry("1200x700")
        
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'players.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db = Database(db_path)
        
        self.players_data = []
        self.sort_column = None
        self.sort_reverse = False
        
        self.load_data()
        self.create_widgets()
    
    def load_data(self):
        self.players_data = self.db.get_all_players()
    
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
        columns = ['姓名', '评分', '正常属性评分', '隐藏属性评分'] + REQUIRED_ATTRIBUTES
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')
        
        self.tree.heading('姓名', text='姓名', command=lambda: self.sort_by('姓名'))
        self.tree.heading('评分', text='评分', command=lambda: self.sort_by('评分'))
        self.tree.heading('正常属性评分', text='正常属性评分', command=lambda: self.sort_by('正常属性评分'))
        self.tree.heading('隐藏属性评分', text='隐藏属性评分', command=lambda: self.sort_by('隐藏属性评分'))
        
        for attr in REQUIRED_ATTRIBUTES:
            self.tree.heading(attr, text=attr, command=lambda a=attr: self.sort_by(a))
        
        self.tree.column('姓名', width=150)
        self.tree.column('评分', width=100)
        self.tree.column('正常属性评分', width=120)
        self.tree.column('隐藏属性评分', width=120)
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
        dialog.geometry("1100x500")
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
            row = i // 5
            col = i % 5
            
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
            
            label = ttk.Label(frame, text=label_text + ":", width=10, anchor='e')
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
                normal_score, hidden_score, score = calculate_total_score(self.players_data[player_idx]['attributes'])
            else:
                score = None
                normal_score = None
                hidden_score = None
            
            player_id = self.players_data[player_idx]['id']
            self.db.update_player(
                player_id,
                self.players_data[player_idx]['name'],
                self.players_data[player_idx]['attributes'],
                score,
                normal_score,
                hidden_score
            )
            
            self.players_data[player_idx]['score'] = score
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
            normal_score, hidden_score, score = calculate_total_score(player['attributes'])
            import_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.db.add_player(player['name'], score, normal_score, hidden_score, import_time, player['attributes'])
            imported_count += 1
        
        if imported_count > 0:
            self.load_data()
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
                normal_str = f"{player.get('normal_score', 0):.2f}" if player.get('normal_score') is not None else ""
                hidden_str = f"{player.get('hidden_score', 0):.2f}" if player.get('hidden_score') is not None else ""
            else:
                score_str = ""
                normal_str = ""
                hidden_str = ""
            
            values = [player['name'], score_str, normal_str, hidden_str]
            
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
        elif column == '正常属性评分':
            self.players_data.sort(key=lambda x: x.get('normal_score', 0) or 0, reverse=self.sort_reverse)
        elif column == '隐藏属性评分':
            self.players_data.sort(key=lambda x: x.get('hidden_score', 0) or 0, reverse=self.sort_reverse)
        else:
            self.players_data.sort(
                key=lambda x: x.get('attributes', {}).get(column, 0),
                reverse=self.sort_reverse
            )
        
        self.refresh_tree()
    
    def clear_all(self):
        if messagebox.askyesno("确认", "确定要清空所有数据吗?"):
            self.db.clear_all()
            self.load_data()
            self.refresh_tree()
            messagebox.showinfo("成功", "已清空所有数据")

def main():
    root = tk.Tk()
    app = FMPlayerScoreApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
