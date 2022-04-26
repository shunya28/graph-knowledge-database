const nodes = [];

const SelectedNodes = {
    
    push(node, color) {
        nodes.push( { 'node': node, 'id': node.id() } );
        node.style('background-color', color);
    },

    pop() {
        nodes.pop().removeStyle();
    },

    clear() {
        while(nodes.length !== 0) {
            nodes.pop().removeStyle();
        }
    }
};

Object.freeze(SelectedNodes);
