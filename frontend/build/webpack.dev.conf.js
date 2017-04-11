var utils = require('./utils')
var webpack = require('webpack')
var config = require('../config')
var merge = require('webpack-merge')
var baseWebpackConfig = require('./webpack.base.conf')
var FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin')
var BundleTracker = require('webpack-bundle-tracker');


module.exports = merge(baseWebpackConfig, {
  output: {
      publicPath: 'http://' + config.dev.serverAddr + ':' + config.dev.serverPort + config.dev.assetsPublicPath
  },
  module: {
    rules: utils.styleLoaders({ sourceMap: config.dev.cssSourceMap })
  },
  // cheap-module-eval-source-map is faster for development
  devtool: '#cheap-module-eval-source-map',
  devServer: {
      historyApiFallback: true,
      noInfo: true
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': config.dev.env
    }),
    new BundleTracker({filename: './webpack-stats.json'}),
    // https://github.com/glenjamin/webpack-hot-middleware#installation--usage
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoEmitOnErrorsPlugin(),
    new FriendlyErrorsPlugin()
  ]
})

module.exports.entry.app = [
    'webpack-dev-server/client?http://' + config.dev.serverAddr + ':' + config.dev.serverPort,
    'webpack/hot/only-dev-server'
].concat(module.exports.entry.app)
