'use strict';
Object.defineProperty(exports, '__esModule', { value: true });
const plugin_1 = require('./plugin');
function plugin(initializerContext) {
  return new plugin_1.WazuhAiSocPlugin(initializerContext);
}
exports.plugin = plugin;
