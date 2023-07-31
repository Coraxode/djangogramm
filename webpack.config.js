const path = require('path');

module.exports = {
    entry: './static/assets/scripts/index.js',
    output: {
        path: path.resolve(__dirname, 'static'),
        filename: 'bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            }
        ]
    }
};
