module.exports = {
    configureWebpack: {
        devServer: {
            https: true,
            proxy: {
                '/api': {target: 'http://localhost:5000'},
                '/swaggerui': {target: 'http://localhost:5000'}
            }
        }
    }
}