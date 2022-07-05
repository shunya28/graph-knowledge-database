const modes = {
    normal: 1,
    create: 2,  // 記事の新規作成画面が表示されている状態
    delete: 3   // 記事の削除画面が表示されている状態
};

let now_mode = modes.normal;  // 現在の画面状態を表す変数
const clicked_node_list = [];
const node_color = '#719ddc';

// ノードに色付けすると同時に、クリックされたノードとしてリストに保持する
const color_node = (node, color) => {
    node.style('background-color', color);
    clicked_node_list.push(node);
};

// 全てのノードの色を元に戻し、リストも空にする
const decolor_all_nodes = () => {
    while(clicked_node_list.length !== 0) {
        const node = clicked_node_list.pop();
        node.removeStyle();
    }
};

// ノードのリストからidのリストを生成する
create_id_list = () => {
    const id_list = [];
    for(let i = 0; i < clicked_node_list.length; i++) {  // for in構文を使うとなぜか要素を取り出せず、node.id()でエラーが出る
        const node = clicked_node_list[i]
        id_list.push(node.id());
    }
    return id_list;
};

const cy_style = [
    {
        selector: 'node',
        style: {
            'background-color': '#666',
            'label': 'data(title)'
        }
    },
    {
        selector: 'edge',
        style: {
            'width': 3,
            'line-color': '#ccc',
            'target-arrow-color': '#ccc',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            // 'label': 'data(label)'
        }
    }
];

const cy_layout = {
    name: 'dagre',
    rows: 1,
};

const cy = cytoscape({
    container: document.getElementById('cy'),            
    elements: graph_data,
    style: cy_style,
    layout: cy_layout,
    wheelSensitivity: 0.2,
});

// ノードがクリックされたときの設定
cy.on('tap', 'node', function(evt) {
    const node = evt.target;

    if(now_mode === modes.normal) {

        // idの一致するノードを線形探索し、記事を表示する
        for(let i = 0; i < graph_data.length; i++) {
            if(node.id() === graph_data[i].data.id) {
                document.getElementById('article-title').textContent = graph_data[i].data.title;                 
                document.getElementById('article-body').innerHTML = markdown_to_sanitized_html(graph_data[i].data.body);
                break;
            }
        }
        document.getElementById('article-detail').style.display = 'block';
        
        // ノードに色を付ける
        decolor_all_nodes();
        color_node(node, node_color);
        
        return;
    }
    
    // 以下、途中までcreateモードとdeleteモードの共通処理

    // フォームの二重送信防止
    document.getElementsByTagName('form')[0].addEventListener('submit', function() {
        document.getElementsByClassName('submit-button')[0].disabled = true;
    });

    // クリックされたノードが既にリスト内に存在するかチェック
    let is_node_in_list = false;
    let node_idx;
    for(let i = 0; i < clicked_node_list.length; i++) {
        if(node === clicked_node_list[i]) {
            is_node_in_list = true;
            node_idx = i;
            break;
        }
    }

    // クリックしたノードが色無しなら色を付け、色付きなら色を無くす処理
    if(is_node_in_list) {
        const del_node_list = clicked_node_list.splice(node_idx, 1);
        
        for(let i = 0; i < del_node_list.length; i++) {
            del_node_list[i].removeStyle();
        }
    }
    else {
        color_node(node, node_color);
    }                 
    
    if(now_mode === modes.create) {
        const ref_list = create_id_list();
        document.getElementById('references').textContent = ref_list;
    }
    else {  // deleteモードの時
        const del_list = create_id_list();
        document.getElementById('delnodes').textContent = del_list;
    }
});

// 背景がクリックされたときの設定
cy.on('tap', function(event){                
    const evtTarget = event.target;

    // 背景をクリックしたとき
    if(evtTarget === cy && now_mode === modes.normal){
        document.getElementById('article-detail').style.display = 'none';
        decolor_all_nodes();
    }
});


// 以下はページの表示に関わる関数

const show_create_page = () => {
    document.getElementById('article-detail').style.display = 'none';
    document.getElementById('article-delete').style.display = 'none';

    now_mode = modes.create;
    decolor_all_nodes();
    document.getElementById('references').textContent = '';

    document.getElementById('article-create').style.display = 'block';
};

const hide_create_page = () => {

    decolor_all_nodes();
    document.getElementById('article-create').style.display = 'none';

    now_mode = modes.normal;
};

const show_delete_page = () => {
    document.getElementById('article-detail').style.display = 'none';
    document.getElementById('article-create').style.display = 'none';

    now_mode = modes.delete;
    decolor_all_nodes();
    document.getElementById('delnodes').textContent = '';

    document.getElementById('article-delete').style.display = 'block';
};

const hide_delete_page = () => {
    decolor_all_nodes();
    document.getElementById('article-delete').style.display = 'none';

    now_mode = modes.normal;
};

const hide_article_page = () => {
    decolor_all_nodes();
    document.getElementById('article-detail').style.display = 'none';
};
