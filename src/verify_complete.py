import csv
import openpyxl

attr_name_map = {
    '传​球': '传球', '传​中': '传中', '盯​人': '盯人', '点​球': '点球',
    '技​术': '技术', '角​球': '角球', '界​外球': '界外球', '盘​带': '盘带',
    '抢​断': '抢断', '任​意球': '任意球', '射​门': '射门', '停​球': '停球',
    '头​球': '头球', '远​射': '远射', '才​华': '才华', '位​置': '位置',
    '投​入': '投入', '集​中': '集中', '决​断': '决断', '领​导力': '领导力',
    '侵​略': '侵略', '视​野': '视野', '合​作': '合作', '无​球跑': '无球跑',
    '意​志': '意志', '勇​敢': '勇敢', '预​判': '预判', '镇​定': '镇定',
    '爆​发': '爆发', '弹​跳': '弹跳', '灵​活': '灵活', '耐​力': '耐力',
    '平​衡': '平衡', '强​壮': '强壮', '速​度': '速度', '体​质': '体质',
    '稳​定': '稳定', '大​赛发​挥': '大赛发挥', '抗​压': '抗压'
}

attribute_weights = {
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

def calculate_score(value, weights):
    w1 = weights['w1']
    w2 = weights['w2']
    w3 = weights['w3']
    w2_sp = weights['w2_sp']
    w3_sp = weights['w3_sp']
    
    # 特殊公式：区间为 1-6, 6-10, 10-20
    if w2_sp is not None:
        if value <= 6:
            return (value - 1) * w1
        elif value <= 10:
            return 5 * w1 + (value - 4) * w2_sp
        else:
            final_w3 = w3_sp if w3_sp is not None else w3
            return 5 * w1 + 4 * w2_sp + (value - 10) * final_w3
    else:
        # 标准公式：区间为 1-6, 6-12, 12-20
        if value <= 6:
            return (value - 1) * w1
        elif value <= 12:
            return 5 * w1 + (value - 6) * w2
        else:
            return 5 * w1 + 6 * w2 + (value - 12) * w3

csv_attr_order = [
    '传球', '传中', '盯人', '点球', '技术', '角球', '界外球', '盘带', '抢断', '任意球', '射门',
    '停球', '头球', '远射', '才华', '位置', '投入', '集中', '决断', '领导力', '侵略',
    '视野', '合作', '无球跑', '意志', '勇敢', '预判', '镇定', '爆发', '弹跳', '灵活',
    '耐力', '平衡', '强壮', '速度', '体质', '稳定', '大赛发挥', '抗压'
]

def verify_single_attributes():
    wb = openpyxl.load_workbook('工作表18+FM24.xlsx', data_only=True)
    ws_score = wb['分数 ']
    ws_data = wb['数据']
    
    print("=" * 100)
    print("第一步：对比单个属性的计算得分")
    print("=" * 100)
    
    row = 3
    
    print(f"\n球员: 利桑德罗·马丁内斯")
    print(f"\n{'属性':15} {'原始值':6} {'Excel得分':12} {'计算得分':12} {'差异':10}")
    print("-" * 70)
    
    total_excel = 0
    total_calc = 0
    matched_count = 0
    
    for col in range(12, 52):
        excel_attr = ws_score.cell(row=1, column=col).value
        if not excel_attr or excel_attr == '出击':
            continue
        
        simple_name = attr_name_map.get(excel_attr, None)
        
        excel_score = ws_score.cell(row=row, column=col).value
        raw_value = ws_data.cell(row=row, column=col).value
        
        if simple_name and simple_name in attribute_weights and raw_value is not None and excel_score is not None:
            calc_score = calculate_score(raw_value, attribute_weights[simple_name])
            diff = excel_score - calc_score
            
            total_excel += excel_score
            total_calc += calc_score
            matched_count += 1
            
            print(f"{simple_name:15} {raw_value:6} {excel_score:12.4f} {calc_score:12.4f} {diff:10.4f}")
    
    print("-" * 70)
    print(f"{'总计':15} 匹配数:{matched_count} {total_excel:12.4f} {total_calc:12.4f} {total_excel-total_calc:10.4f}")

def verify_total_scores():
    with open('FM2024_球员评分.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        results = []
        
        for row in reader:
            player = row[0]
            expected_score = float(row[1])
            
            total_score = 0
            for i, attr in enumerate(csv_attr_order):
                if i < len(row) - 2:
                    value = int(row[i + 2])
                    if attr in attribute_weights:
                        total_score += calculate_score(value, attribute_weights[attr])
            
            results.append({
                'player': player,
                'expected_score': expected_score,
                'calculated_score': total_score,
                'difference': abs(total_score - expected_score)
            })
        
        print("\n" + "=" * 100)
        print("第二步：对比总得分")
        print("=" * 100)
        
        differences = [r['difference'] for r in results]
        avg_diff = sum(differences) / len(differences)
        max_diff = max(differences)
        min_diff = min(differences)
        
        print(f"\n验证结果统计:")
        print(f"  样本数: {len(results)}")
        print(f"  平均差异: {avg_diff:.4f}")
        print(f"  最大差异: {max_diff:.4f}")
        print(f"  最小差异: {min_diff:.4f}")
        
        print(f"\n前10个样本详情:")
        for r in results[:10]:
            print(f"  {r['player'][:25]}: 预期={r['expected_score']:.2f}, 计算={r['calculated_score']:.2f}, 差异={r['difference']:.4f}")

if __name__ == "__main__":
    verify_single_attributes()
    verify_total_scores()
