class CytoscapeSettings {

    #graph_data;
    #modes = {
        normal: 1,
        create: 2,  // 記事の新規作成画面が表示されている状態
        delete: 3   // 記事の削除画面が表示されている状態
    };
    #now_mode;  // 現在の画面状態を表す変数
    #clicked_node_list;
    #node_color;
    #cy;

    articles = []  // FIXME: 別のものに置き換えた後削除する
    
    constructor(graph_data) {
        this.#graph_data = graph_data;
        this.#now_mode = this.#modes.normal;  // 現在の画面状態を表す変数
        this.#clicked_node_list = [];
        this.#node_color = '#719ddc';

        this.#cy = this.#create_cy_object();
        this.#settings_when_node_clicked();
        this.#settings_when_background_clicked();
    }

    #create_cy_object() {
        const _cy = cytoscape({
            container: document.getElementById('cy'),            
            elements: this.#graph_data,
            style: [
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
                        'label': 'data(label)'
                    }
                }
            ],
            layout: {
                name: 'dagre',
                rows: 1
            },
            wheelSensitivity: 0.2,
        });
        return _cy;
    }

    // ノードに色付けすると同時に、クリックされたノードとしてリストに保持する
    #color_node(node, color) {
        node.style('background-color', color);
        this.#clicked_node_list.push(node);
    };

    // 全てのノードの色を元に戻し、リストも空にする
    #decolor_all_nodes() {
        while(this.#clicked_node_list.length !== 0) {
            const node = this.#clicked_node_list.pop();
            node.removeStyle();
        }
    };

    // ノードのリストからidのリストを生成する
    #create_id_list() {
        const id_list = [];
        for(let i = 0; i < this.#clicked_node_list.length; i++) {  // for in構文を使うとなぜか要素を取り出せず、node.id()でエラーが出る
            const node = this.#clicked_node_list[i]
            id_list.push(node.id());
        }
        return id_list;
    };

    #settings_when_node_clicked() {
        this.#cy.on('tap', 'node', function(evt){
            const node = evt.target;
            if(this.#now_mode === this.#modes.normal) {

                // idの一致するノードを線形探索し、記事を表示する
                for(let i = 0; i < articles.length; i++) {
                    if(node.id() === articles[i].uid) {
                        document.getElementById('article-title').text(articles[i].title);
                        document.getElementById('article-body').text(articles[i].body);
                        break;
                    }
                }
                document.getElementById('article-detail').style.display = 'none';
                
                // ノードに色を付ける
                this.#decolor_all_nodes();
                this.#color_node(node, this.#node_color);
            }
            else {  // 以下、途中までcreateモードとdeleteモードの共通処理

                // クリックされたノードが既にリスト内に存在するかチェック
                let is_node_in_list = false;
                let node_idx;
                for(let i = 0; i < this.#clicked_node_list.length; i++) {
                    if(node === this.#clicked_node_list[i]) {
                        is_node_in_list = true;
                        node_idx = i;
                        break;
                    }
                }

                // クリックしたノードが色無しなら色を付け、色付きなら色を無くす処理
                if(is_node_in_list) {
                    const del_node_list = this.#clicked_node_list.splice(node_idx, 1);
                    
                    for(let i = 0; i < del_node_list.length; i++) {
                        del_node_list[i].removeStyle();
                    }
                }
                else {
                    this.#color_node(node, this.#node_color);
                }                 
                
                if(this.#now_mode === this.#modes.create) {
                    const ref_list = create_id_list();
                    document.getElementById('references').text(ref_list);
                }
                else {  // deleteモードの時
                    const del_list = create_id_list();
                    document.getElementById('delnodes').text(del_list);
                }                    
            }

            // フォームの二重送信防止
            document.getElementsByTagName('form').on('submit', function() {
                document.getElementsByClassName('submit-button').prop('disabled', true);
            });            
        });
    }

    #settings_when_background_clicked() {
        this.#cy.on('tap', function(event){                
            const evtTarget = event.target;

            // 背景をクリックしたとき
            if( evtTarget === this.#cy ){
                if(this.#now_mode === this.#modes.normal) {
                    document.getElementById('article-detail').style.display = 'block';
                    this.#decolor_all_nodes();
                }
            }
        });
    }
}

export default CytoscapeSettings;
