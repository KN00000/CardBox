import json
from collections import deque

class CardBox:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cards = deque()

    def is_full(self):
        if self.capacity is None:
            return False
        return len(self.cards) >= self.capacity

def save_data(boxes, filename='cards.json'):
    data = {
        'boxes': [
            {'cards': [list(card) for card in box.cards]}
            for box in boxes
        ]
    }
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n数据已保存到 {filename}")
    except Exception as e:
        print(f"保存数据失败: {str(e)}")

def load_data(boxes, filename='cards.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i, box_data in enumerate(data['boxes']):
                if i < len(boxes):
                    boxes[i].cards.clear()
                    for card in box_data['cards']:
                        boxes[i].cards.append(tuple(card))
        print("成功加载上次保存的数据")
    except FileNotFoundError:
        print("未找到保存文件，将创建新记录")
    except Exception as e:
        print(f"加载数据失败: {str(e)}")

def get_user_choice(card):
    """处理用户输入，返回有效选择"""
    while True:
        choice = input("记得吗？ (1:记得 / 2:不记得 / 3:展示含义): ").strip()
        if choice == "3":
            print(f"\n含义: {card[1]}")
            continue
        if choice in ("1", "2"):
            return choice
        print("输入无效，请输入1、2或3")

def main():
    boxes = [
        CardBox(100),   # 1号箱
        CardBox(5),   # 2号箱
        CardBox(6),   # 3号箱
        CardBox(7),   # 4号箱
        CardBox(8),  # 5号箱
        CardBox(None)   # 6号箱
    ]
    
    load_data(boxes)

    # 用户输入阶段
    print("请输入单词及其含义（格式：单词:含义），输入完成后输入'复习'开始复习")
    while True:
        user_input = input("> ").strip()
        if user_input == "复习":
            break
        
        if ":" not in user_input:
            print("格式错误，请使用'单词:含义'的格式")
            continue
            
        word, meaning = user_input.split(":", 1)
        boxes[0].cards.append((word.strip(), meaning.strip()))
        print(f"已添加单词到1号箱（当前数量：{len(boxes[0].cards)}/{boxes[0].capacity}）")

    # 复习阶段
    # 处理1号箱
    while len(boxes[0].cards) > 3:
        current_cards = list(boxes[0].cards)
        boxes[0].cards.clear()
        remember = []
        forget = []

        for card in current_cards:
            print(f"\n单词: {card[0]}")
            choice = get_user_choice(card)
                
            if choice == "1":
                remember.append(card)
            else:
                forget.append(card)

        boxes[0].cards.extend(forget)
        boxes[1].cards.extend(remember)
        print(f"\n当前1号箱剩余单词：{len(boxes[0].cards)}个")
        save_data(boxes)

    # 处理其他满的卡片箱
    while True:
        processed = False
        for box_idx in range(1, 5):
            current_box = boxes[box_idx]
            next_box = boxes[box_idx+1]
            
            if current_box.is_full():
                processed = True
                review_count = min(150, len(current_box.cards))
                print(f"\n{'='*30}")
                print(f"开始处理{box_idx+1}号箱（容量已满）")
                print(f"需要复习前{review_count}个单词")
                
                for _ in range(review_count):
                    if not current_box.cards:
                        break
                    card = current_box.cards.popleft()
                    
                    print(f"\n单词: {card[0]}")
                    choice = get_user_choice(card)
                        
                    if choice == "1":
                        next_box.cards.append(card)
                    else:
                        boxes[0].cards.append(card)
                
                print(f"处理完成，当前{box_idx+1}号箱剩余：{len(current_box.cards)}个")
                save_data(boxes)
        
        if not processed:
            break

    save_data(boxes)
    print("\n各卡片箱当前状态：")
    for idx, box in enumerate(boxes):
        capacity = "∞" if box.capacity is None else box.capacity
        print(f"{idx+1}号箱：{len(box.cards)}/{capacity}")

if __name__ == "__main__":
    main()