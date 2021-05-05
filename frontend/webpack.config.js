module.exports = {
    module: {
      rules: [
        {
          test: /\.css$/i,
          use: ['style-loader', 'css-loader'],
        },
      ],
    },
    
const webpack = require('webpack')

plugins: [
  new webpack.ProvidePlugin({
    mapboxgl: 'mapbox-gl',
  }),
]