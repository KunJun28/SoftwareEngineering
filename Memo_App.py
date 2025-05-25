import os

MEMO_DIR = "memos"

# 메모 저장 폴더 생성
if not os.path.exists(MEMO_DIR):
    os.makedirs(MEMO_DIR)


class Storage:
    def save_memo(self, title, content):
        filename = os.path.join(MEMO_DIR, f"{title}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

    def load_all_memo_titles(self):
        files = os.listdir(MEMO_DIR)
        return [os.path.splitext(f)[0] for f in files if f.endswith('.txt')]

    def load_memo(self, title):
        filename = os.path.join(MEMO_DIR, f"{title}.txt")
        if not os.path.exists(filename):
            return None
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()

    def memo_exists(self, title):
        filename = os.path.join(MEMO_DIR, f"{title}.txt")
        return os.path.exists(filename)


class NoteController:
    def __init__(self):
        self.storage = Storage()

    def create_memo(self, title, content):
        if self.storage.memo_exists(title):
            return False
        self.storage.save_memo(title, content)
        return True

    def get_all_memo_titles(self):
        return self.storage.load_all_memo_titles()

    def get_memo(self, title):
        return self.storage.load_memo(title)

    def update_memo(self, title, new_content):
        if not self.storage.memo_exists(title):
            return False
        self.storage.save_memo(title, new_content)
        return True


class MemoUI:
    def __init__(self):
        self.controller = NoteController()

    def run(self):
        while True:
            print("\n===== 메모장 메뉴 =====")
            print("1. 새 메모 작성")
            print("2. 저장된 메모 목록 보기")
            print("3. 메모 내용 보기")
            print("4. 메모 수정")
            print("5. 종료")

            choice = input("선택: ")

            if choice == '1':
                self.create_memo()
            elif choice == '2':
                self.show_memo_list()
            elif choice == '3':
                self.view_memo()
            elif choice == '4':
                self.edit_memo()
            elif choice == '5':
                print("메모장을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다. 다시 선택하세요.")

    def create_memo(self):
        title = input("제목 입력: ")
        content = input("내용 입력: ")
        success = self.controller.create_memo(title, content)
        if success:
            print(f"[저장 완료] '{title}' 메모가 저장되었습니다.")
        else:
            print(f"[오류] 제목이 '{title}'인 메모가 이미 존재합니다.")

    def show_memo_list(self):
        titles = self.controller.get_all_memo_titles()
        if not titles:
            print("저장된 메모가 없습니다.")
        else:
            print("저장된 메모 목록:")
            for t in titles:
                print("- " + t)

    def view_memo(self):
        title = input("열람할 메모 제목 입력: ")
        content = self.controller.get_memo(title)
        if content is None:
            print("해당 제목의 메모가 존재하지 않습니다.")
        else:
            print(f"\n[{title}]")
            print(content)

    def edit_memo(self):
        title = input("수정할 메모 제목 입력: ")
        old_content = self.controller.get_memo(title)
        if old_content is None:
            print("해당 제목의 메모가 존재하지 않습니다.")
        else:
            print(f"\n현재 내용:\n{old_content}")
            new_content = input("\n새 내용 입력: ")
            success = self.controller.update_memo(title, new_content)
            if success:
                print(f"[수정 완료] '{title}' 메모가 수정되었습니다.")
            else:
                print("[오류] 메모 수정에 실패했습니다.")


if __name__ == "__main__":
    app = MemoUI()
    app.run()
