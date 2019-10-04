const path = require('path')
const each = require('lodash/fp/each')
const BundleTrackerPlugin = require('webpack-bundle-tracker');

// https://github.com/ezhome/webpack-bundle-tracker/issues/25
class RelativeBundleTrackerPlugin extends BundleTrackerPlugin {
	convertPathChunks(chunks){
		each(each(chunk => {
			chunk.path = path.relative(this.options.path, chunk.path)
		}))(chunks)
	}
	writeOutput(compiler, contents) {
		if (contents.status === 'done')  {
			this.convertPathChunks(contents.chunks)
		}

		super.writeOutput(compiler, contents)
	}
}

module.exports = {
	webpack: (config, env) => {
		config.optimization.splitChunks.name = 'vendors';
		
		if (env === 'development') {
			config.output.publicPath = 'http://localhost:3000/';
			
			config.plugins.push(
				new BundleTrackerPlugin({
					path: __dirname,
					filename: 'webpack-stats.dev.json',
				}),
			);
			
			config.entry = config.entry.filter(x => !x.includes('webpackHotDevClient'));
			config.entry.push(require.resolve('webpack-dev-server/client') + '?http://localhost:3000');
			config.entry.push(require.resolve('webpack/hot/dev-server'));
		} else if (env === 'production') {
			config.plugins.push(
				new RelativeBundleTrackerPlugin({
					path: __dirname,
					filename: 'webpack-stats.prod.json',
				}),
			);
		}

		return config;
	},
	devServer: function(configFunction) {
		return function(proxy, allowedHost) {
			const config = configFunction(proxy, allowedHost);
			config.headers = {'Access-Control-Allow-Origin': '*'};
			return config;
		};
	},
};
