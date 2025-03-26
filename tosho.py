books = []  # 図書リスト（辞書形式）
members = []  # 会員リスト（辞書形式）
borrow_records = []  # 貸出記録（辞書形式）

"""
図書管理
"""
# 新しい図書を追加
def add_book(book_id, title, author, copies):
    # 図書の存在確認（すでに存在していたら追加しない）
    for book in books:
        if book["book_id"] == book_id:
            print(f"図書ID「{book_id}」の本は既に存在します。")
            return

    books.append({"book_id": book_id, "title": title, "author": author, "copies": copies, "available_copies": copies})
    print(f"図書「{title}」（ID: {book_id}, 著者: {author}, 冊数: {copies}）を追加しました。")

# 図書一覧を表示
def list_books():
    # 図書の存在確認
    if not books:
        print("現在、登録されている図書はありません。")
        return

    print("--- 図書一覧 ---")
    for book in books:
        print(f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 総冊数: {book['copies']}, 在庫: {book['available_copies']}")

"""
会員管理
"""
# 新しい会員を追加
def add_member(member_id, name):
    # 会員の存在確認（すでに存在していたら追加しない）
    for member in members:
        if member["member_id"] == member_id:
            print(f"会員ID「{member_id}」の会員は既に存在します。")
            return

    members.append({"member_id": member_id, "name": name})
    print(f"会員「{name}」（ID: {member_id}）を追加しました。")

# 会員一覧を表示
def list_members():
    # 会員の存在確認
    if not members:
        print("現在、登録されている会員はいません。")
        return

    print("--- 会員一覧 ---")
    for member in members:
        print(f"ID: {member['member_id']}, 名前: {member['name']}")

"""
貸出管理
"""
# 図書を貸し出す
def borrow_book(book_id, member_id):
    # 図書の存在確認
    book = "None"
    for b in books:
        if b["book_id"] == book_id:
            book = b
            break
    if not book:
        print(f"図書ID「{book_id}」の本は存在しません。")
        return

    # 会員の存在確認
    member = None
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    if not member:
        print(f"会員ID「{member_id}」の会員は存在しません。")
        return

    # 在庫確認
    if book["available_copies"] <= 0:
        print(f"図書「{book['title']}」は現在貸出可能な冊数がありません。")
        return

    # 貸出記録に追加
    borrow_records.append({
        "book_id": book_id,
        "member_id": member_id,
        "borrow_date": "2024-11-24",  # 現在日付として固定値
        "due_date": "2024-12-01",  # 1週間後を返却期限と仮定
        "returned": False # 返却状況（Trueなら返却済み、Falseなら未返却）
    })
    print(f"図書「{book['title']}」を会員「{member['name']}」に貸し出しました。\n返却期限: 2024-12-01")

    # 在庫を減らす処理
    book["available_copies"] -= 1

# 貸出中の図書を表示
def list_borrowed_books():
    print("--- 貸出中の図書一覧 ---")
    # 貸出中でステータスが未返却の図書を一覧表示
    borrow_count = 0
    for record in borrow_records:
        if not record["returned"]:
            book = ""
            for b in books:
                if b["book_id"] == record["book_id"]:
                    book = b
            member = ""
            for m in members:
                if m["member_id"] == record["member_id"]:
                    member = m
            print(f"図書: {book['title']}（ID: {record['book_id']}）, 会員: {member['name']}（ID: {record['member_id']}）, 貸出日: {record['borrow_date']}, 返却期限: {record['due_date']}")
            borrow_count += 1
    # 貸出中の図書の存在確認
    if borrow_count == 0:
        print("現在、貸出中の図書はありません。")

"""
貸出管理
"""
# 図書を返却
def return_book(book_id, member_id):
    # 存在確認
    record = ""
    for r in borrow_records:
        if r["book_id"] == book_id and r["member_id"] == member_id and not r["returned"]:
            r["returned"] = True # ステータスを「返却済」に変更
            record = r
            break
    if not record:
        print(f"図書ID「{book_id}」本を会員ID「{member_id}」の会員は借りていません。")
        return

    book = ""
    for b in books:
        if b["book_id"] == book_id:
            b["available_copies"] += 1
            book = b
            break
    print(f"図書「{book['title']}」が返却されました。")

"""
延滞料金計算
"""
def calculate_fines():
    print("--- 延滞料金一覧 ---")
    borrow_count = 0
    for record in borrow_records:
        if not record["returned"]:
            book = ""
            for b in books:
                if b["book_id"] == record["book_id"]:
                    book = b
                    break
            member = ""
            for m in members:
                if m["member_id"] == record["member_id"]:
                    member = m
                    break
            # 仮に本日を "2024-12-24" として計算
            due_date = "2024-12-01"
            today = "2024-12-24"
            # 最大の延滞日数を1ヶ月と仮定して計算
            overdue_days = max((int(today[-2:]) - int(due_date[-2:])), 0)
            # 延滞料金計算（仮定: 1日あたり100円）
            fine = overdue_days * 100
            print(f"図書: {book['title']}（ID: {record['book_id']}）, 会員: {member['name']}（ID: {record['member_id']}）, 延滞料金: {fine}円")
    if borrow_count == 0:
        print("現在、貸出中の図書はありません。")

# メイン処理
def main():
    while True:
        print("図書館管理システムメニュー:")
        print("1: 図書を追加")
        print("2: 図書一覧を表示")
        print("3: 会員を追加")
        print("4: 会員一覧を表示")
        print("5: 図書を貸し出す")
        print("6: 貸出中の図書一覧を表示")
        print("7: 図書を返却")
        print("8: 延滞料金を計算")
        print("9: 終了")

        try:
            choice = int(input("操作を選択してください（1-9）: "))

            if choice == 1:
                book_id = input("図書IDを入力してください: ")
                title = input("タイトルを入力してください: ")
                author = input("著者名を入力してください: ")
                copies = int(input("冊数を入力してください: "))
                add_book(book_id, title, author, copies)

            elif choice == 2:
                list_books()

            elif choice == 3:
                member_id = input("会員IDを入力してください: ")
                name = input("名前を入力してください: ")
                add_member(member_id, name)

            elif choice == 4:
                list_members()

            elif choice == 5:
                book_id = input("貸し出す図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                borrow_book(book_id, member_id)

            elif choice == 6:
                list_borrowed_books()

            elif choice == 7:
                book_id = input("返却する図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                return_book(book_id, member_id)

            elif choice == 8:
                calculate_fines()

            elif choice == 9:
                print("図書館管理システムを終了します。")
                break

            else:
                print("無効な選択です。1-9の数字を入力してください。")

        except ValueError as e:
            print(f"入力エラー: {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")

# メイン処理の実行
main()