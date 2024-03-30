

// カスタム画像アップロードハンドラ
function customImageUploadHandler(event) {
    // ここで独自の画像アップロード処理を行います。
    // 例: AWS S3へアップロードする処理など

    // 例：画像ファイルを取得
    let file = event.data.fileLoader.file;

    // 画像をAWS S3にアップロードする処理を実装
    // アップロード処理が成功したら、画像のURLを取得
    let imageUrl = "アップロード後の画像URL";

    // CKEditorのインスタンスに画像を挿入
    CKEDITOR.instances['todo-details'].insertHtml('<img src="' + imageUrl + '"/>');

    // 通常のファイルアップロード処理をキャンセル
    event.stop();
}

// CKEditorインスタンスに対するイベントリスナー設定
function setUpEditor() {
    let richTextEdited = CKEDITOR.replace('todo-details', {
        toolbar: [
            { name: 'undo', items: ['Undo', 'Redo'] },
            { name: 'links', items: ['Link', 'Unlink'] },
            { name: 'insert', items: ['Image', 'Table'] },
            { name: 'insert', items: ['Table'] },
            { name: 'tools', items: ['Source'] },
            { name: 'basicstyles', items: ['Bold', 'Strike'] },
            { name: 'paragraph', items: ['NumberedList', 'BulletedList', '-', 'Blockquote'] },
            { name: 'formatting', items: ['Format'] }
        ]
    });

    // ファイルアップロードリクエストイベントにリスナーを設定
    richTextEdited.on('fileUploadRequest', function(event) {
        customImageUploadHandler(event);
    });
}

// DOMの読み込み完了後にエディタをセットアップ
window.onload = function() {
    let todoDetails = document.getElementById('todo-details');
    if (todoDetails) {
        setUpEditor();
    }
};


// Todoの未完了・完了タブ切り替え
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tab-link");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.add("inactive"); // すべてのタブに先にinactiveを適用
        tablinks[i].classList.remove("active"); // activeクラスを削除
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.classList.remove("inactive"); // クリックされたタブからinactiveを除去
    evt.currentTarget.classList.add("active"); // そして、activeを追加

    // "addTodoButton" の表示/非表示を切り替える
    var addButton = document.getElementById("add-todo-button");
    if (tabName === "Complete") {
        // 完了タブが選択されたらボタンを非表示にする
        addButton.style.display = "none";
    } else {
        // それ以外のタブが選択されたらボタンを表示する
        addButton.style.display = "flex"; // 以前にflexを指定していたため
    }
}

// 初期タブを開く
document.getElementsByClassName("tab-link")[0].click();

const profileIcon = document.getElementById("profile-icon");
const closeModal = document.getElementById('close-profile');
profileIcon.onclick = event => {
    let modal = document.getElementById('modal');
    let mask = document.getElementById('mask');
    modal.classList.remove('hidden');
    mask.classList.remove('hidden');

    closeModal.addEventListener('click', function () {
        modal.classList.add('hidden');
        mask.classList.add('hidden');
    });
}

// Todoの詳細を開く
function toggleTodoDetails(event) {

    // 全てのtodo-detailを取得し、hidden属性をtrueに設定
    document.querySelectorAll('.todo-detail').forEach(detail => {
        // クリックされた要素のtodo-detail以外を非表示にする
        if (event.currentTarget.querySelector('.todo-detail') !== detail) {
            detail.hidden = true;
        }
    });
    // 全てのtodo-detailを取得し、hidden属性をtrueに設定
    document.querySelectorAll('.reg-todo-date').forEach(regTodoDate => {
        // クリックされた要素のtodo-detail以外を非表示にする
        if (event.currentTarget.querySelector('.reg-todo-date') !== regTodoDate) {
            regTodoDate.hidden = true;
        }
    });
    // 全てのtodo-edit-buttonsを取得し、hidden属性をtrueに設定
    document.querySelectorAll('.todo-edit-buttons').forEach(buttons => {
        // クリックされた要素のtodo-edit-buttons以外を非表示にする
        if (event.currentTarget.querySelector('.todo-edit-buttons') !== buttons) {
            buttons.hidden = true;
        }
    });

    // クリックされた要素の子要素を取得し、詳細の表示状態を切り替える
    // Todo詳細
    const details = event.currentTarget.querySelector('.todo-detail');
    if (details) {
        details.hidden = !details.hidden; // hidden属性をトグル
    }
    // 登録日
    const regTodoDate = event.currentTarget.querySelector('.reg-todo-date');
    if (regTodoDate) {
        regTodoDate.hidden = !regTodoDate.hidden; // hidden属性をトグル
    }
    // Todoコントロールボタン
    const todoEditButtons = event.currentTarget.querySelector('.todo-edit-buttons');
    if (todoEditButtons) {
        todoEditButtons.hidden = !todoEditButtons.hidden; // hidden属性をトグル
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    // ページ上の全ての編集ボタンにイベントリスナーを追加
    document.querySelectorAll('.todo-edit-btn, .todo-del-btn, .todo-due-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            event.stopPropagation(); // イベントの伝播を停止
        });
    });
});


let startX;

function touchStart(event) {
    startX = event.touches[0].clientX;
}

function touchMove(event) {
    // スライドの移動距離を計算
    const touchX = event.touches[0].clientX;
    const moveX = startX - touchX;
    // 移動距離に基づいてボタンを表示
    const button = event.currentTarget.querySelector('.complete-btn');
    if (moveX > 0) { // 右から左にスライド
        button.style.right = `${-100 + moveX}px`;
        button.style.opacity = 1;
    }
}

function touchEnd(event) {
    const button = event.currentTarget.querySelector('.complete-btn');
    // スライドをリセット
    button.style.right = `-100px`;
    button.style.opacity = 0;
}
