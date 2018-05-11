var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

const paths = {
    ASSETS: path.resolve(__dirname, 'assets/bundles'),
    JS: path.resolve(__dirname, 'assets/js')
}


module.exports = {
    context: __dirname,
    entry : path.join(paths.JS, 'index.js'),
    output: {
        path: path.resolve(__dirname, 'assets/bundles'),
        filename: 'bundle.js',
    },
    plugins: [
        new BundleTracker({ filename: 'webpack-stats.json' }),
        //makes jQuery available in every module
        // new webpack.ProvidePlugin({
        //     $: 'jquery',
        //     jQuery: 'jquery',
        //     'window.jQuery': 'jquery'
        // })
    ], 

    module: {
        rules: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                use: 'babel-loader',
                // query: {
                //     presets: ['react']
                // }
            },
            { 
                test: /\.css$/, 
                use: [ 'style-loader', 'css-loader']
            }
        ]
    },
    resolve: {
        // moduleDirectories: ['node_modules'],
        extensions: ['.js', '.jsx', '.css']
    }
}