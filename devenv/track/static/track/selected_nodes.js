
// // export はdjangoでは厳しそうな感じだった。

// // const nodes = [];

// // const SelectedNodes = {
    
// //     push(node, color) {
// //         nodes.push( { 'node': node, 'id': node.id() } );
// //         node.style('background-color', color);
// //     },

// //     pop() {
// //         nodes.pop().removeStyle();
// //     },

// //     clear() {
// //         while(nodes.length !== 0) {
// //             nodes.pop().removeStyle();
// //         }
// //     }
// // };

// // Object.freeze(SelectedNodes);

// class SelectedNodes {
//     #nodes = [];

//     constructor() {}

//     push_and_color(node, color) {
//         // TODO: nodeがnode型じゃなかったらエラー
//         this.#nodes.push( { 'node': node, 'id': node.id() } );
//         node.style('background-color', color);
//         // console.log(this.#nodes);
//     }

//     pop_and_decolor() {
//         // TODO: popしたものがnullだったらエラー？エラー処理必要ないかも？
//         if(this.#nodes.length > 0) {
//             // console.log(this.#nodes);
//             this.#nodes.pop()['node'].removeStyle();
//         }
//     }

//     clear_and_decolor() {
//         while(this.#nodes.length !== 0) {
//             this.#nodes.pop()['node'].removeStyle();
//         }
//     }

//     get get_nodes() {
//         return this.#nodes;
//     }
// }