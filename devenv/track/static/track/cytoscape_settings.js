// TODO: シングルトンにする？
class CytoscapeSettings {
    
    constructor(graph_data) {
        this.graph_data = graph_data;
        this.cy = this.init_settings();  // TODO: 定数にしたい
    }

    init_settings() {
        const _cy = cytoscape({

            container: document.getElementById('cy'),
            
            elements: this.graph_data,

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
    }
}