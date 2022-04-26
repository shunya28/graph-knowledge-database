function show_create_page() {
    $('#article-detail').hide();
    $('#article-delete').hide();
    $('#article-create').show();

    if(colored_nodes.length !== 0) {
        colored_nodes.shift().removeStyle();
    }
}

function show_delete_page() {
    $('#article-detail').hide();
    $('#article-create').hide();
    $('#article-delete').show();

    if(colored_nodes.length !== 0) {
        colored_nodes.shift().removeStyle();
    }
}

function hide_article_page() {
    // 一つ前にクリックされたノードの色をデフォルトに戻す
    if(colored_nodes !== 0) {
        colored_nodes.shift().removeStyle();
    }
    $('#article-detail').hide();
}

function hide_create_page() {
    reference_list.length = 0;
    $('#references').text(reference_list);

    // 色付けされたノードを全て元の色に戻す
    while(colored_nodes.length !== 0) {
        colored_nodes.shift().removeStyle();
    }

    $('#article-create').hide();
}

function hide_delete_page() {

    $('#article-delete').hide();
}