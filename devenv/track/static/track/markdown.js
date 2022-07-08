marked.setOptions({
    breaks: true,
    gfm: true,
    langPrefix: '',
    headerIds: false,
});

// TODO: ReDoS攻撃を避けるためにWorkerを導入する？（ドキュメント参照）
const markdown_to_sanitized_html = (dirty_text) => {
    const dirty_markdown = marked.parse(dirty_text);
    const sanitized_html = DOMPurify.sanitize(dirty_markdown);
    return sanitized_html;
};

// 新規作成ページでのコードブロックのハイライト機能
document.getElementById('add-body').oninput = (e) => {
    document.getElementById('create-preview').innerHTML = markdown_to_sanitized_html(e.target.value);
    document.querySelectorAll('pre, code').forEach((el) => {
        hljs.highlightElement(el);
    });
};