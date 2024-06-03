const totalItems = 50; // 表示する要素の総数
const itemsPerPage = 7; // 一度に表示する要素の数
let currentPage = 0; // 現在のページ

// コンテナ要素を取得
const container = document.getElementById('container');

// 要素を生成してコンテナに追加（デモ用）
for (let i = totalItems; i > 0; i--) {
    const item = document.createElement('div');
    item.id = `item-${i}`;
    item.textContent = `Item ${i}`;
    item.style.display = 'none'; // 初期状態では非表示
    container.appendChild(item);
}

// 要素を表示する関数
function showItems() {
    // 全要素を一旦非表示にする
    const allItems = document.querySelectorAll('#container div');
    allItems.forEach(item => item.style.display = 'none');

    // 現在のページに対応する要素を表示
    const start = currentPage * itemsPerPage;
    const end = Math.min(start + itemsPerPage, totalItems);
    for (let i = start; i < end; i++) {
        allItems[i].style.display = 'block';
    }
}

// 「次へ」ボタンのハンドラ
function showNext() {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    if (currentPage < totalPages - 1) {
        currentPage++;
        showItems();
    }
}

// 「前へ」ボタンのハンドラ
function showPrevious() {
    if (currentPage > 0) {
        currentPage--;
        showItems();
    }
}

// 初期表示
showItems();
