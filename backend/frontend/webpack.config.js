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
module.exports = {
    module: {
      rules: [
        {
          test: /\.s(c|a)ss$/,
          use: [
            'vue-style-loader',
            'css-loader',
            {
              loader: 'sass-loader',
              // Requires sass-loader@^7.0.0
              options: {
                implementation: require('sass'),
                indentedSyntax: true // optional
              },
              // Requires >= sass-loader@^8.0.0
              options: {
                implementation: require('sass'),
                sassOptions: {
                  indentedSyntax: true // optional
                },
              },
            },
          ],
        },
      ],
    }
  }