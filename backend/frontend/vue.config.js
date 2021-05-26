 
// # ============= COMP90024 - Assignment 2 ============= #
// #                               
// # The University of Melbourne           
// # Team 37
// #
// # ** Authors: **
// # 
// # JJ Burke              1048105
// # Janelle Tang          694209
// # Shuang Qiu            980433
// # Declan Baird-Watson   640975
// # Avinash Rao           1024577 
// # 
// # Location: Melbourne
// # ==================================================== #
const BundleTracker = require("webpack-bundle-tracker");


module.exports = {
    // on Windows you might want to set publicPath: "http://127.0.0.1:8080/" 
    publicPath: "http://172.26.134.122/", 
    outputDir: './dist/',
    
    chainWebpack: config => {

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{filename: './webpack-stats.json'}])

        config.output
            .filename('bundle.js')

        config.optimization
        	.splitChunks(false)

        config.resolve.alias
            .set('__STATIC__', 'static')

        config.devServer
            // the first 3 lines of the following code have been added to the configuration
            .public('http://127.0.0.1:8080')    
            .host('127.0.0.1')    
            .port(8080)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .disableHostCheck(true)
            .headers({"Access-Control-Allow-Origin": ["\*"]})

    configureWebpack: {
        module: {
            rules: [
            {
                test: /\.geojson$/,
                loader: 'json-loader'
            }
            ]
        }
        }
},

    // uncomment before executing 'npm run build' 
    css: {
        extract: {
          filename: 'bundle.css',
          chunkFilename: 'bundle.css',
        },
    }

};