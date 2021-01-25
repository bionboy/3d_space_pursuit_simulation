const path = require('path');

module.exports = {
    mode: 'development',
    entry: './src/index.ts',
    cache: true,
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                include: path.resolve(__dirname, 'src')
            },
        ],
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },
    devtool: "source-map",
    output: {
        filename: 'main.js',
        path: path.resolve(__dirname, 'out'),
    },
};