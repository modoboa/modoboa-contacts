var webpack = require('webpack');
var WebpackDevServer = require('webpack-dev-server');
var config = require('./webpack.dev.conf');

// Dev server address specified in webpack.config.js
var listenAddr = 'localhost';
// Dev server port specified in webpack.config.js
var listenPort = 8001;

new WebpackDevServer(webpack(config), {
    publicPath: config.output.publicPath,
    hot: true,
    inline: true,
    historyApiFallback: true
}).listen(listenPort, listenAddr, function (err, result) {
    if (err) {
        console.log(err);
    }
    console.log('Listening at ' + listenAddr + ':' + listenPort);
});
