(function (modules) {
  var installedModules = {};
  function __webpack_require__(moduleId) {
    if (installedModules[moduleId]) {
      return installedModules[moduleId].exports;
    }
    var module = (installedModules[moduleId] = { exports: {} });
    modules[moduleId](module, module.exports, __webpack_require__);
    return module.exports;
  }
  __osdBundles__.define('plugin/wazuhAiSoc/public', __webpack_require__, 0);
})([
  function (module, exports) {
    'use strict';

    function WazuhAiSocPlugin() {}

    WazuhAiSocPlugin.prototype.setup = function (core) {
      core.application.register({
        id: 'wazuhAiSoc',
        title: 'AI SOC Investigations',
        euiIconType: 'securitySignal',
        category: {
          id: 'wazuh',
          label: 'Wazuh',
          order: 1000,
        },
        order: 9100,
        mount: function (params) {
          var el = params.element;
          el.innerHTML = '';
          el.style.cssText =
            'width:100%;height:100%;display:flex;flex-direction:column;background:#1a1b1e;';

          var header = document.createElement('div');
          header.style.cssText =
            'background:#1D2937;padding:12px 24px;display:flex;align-items:center;gap:12px;border-bottom:2px solid #00BFB3;flex-shrink:0;';

          var icon = document.createElement('span');
          icon.textContent = '\u{1F6E1}\u{FE0F}';
          icon.style.fontSize = '22px';

          var title = document.createElement('span');
          title.textContent = 'AI SOC Investigations';
          title.style.cssText =
            'color:#ffffff;font-size:18px;font-weight:700;font-family:Inter,sans-serif;';

          var badge = document.createElement('span');
          badge.textContent = 'LIVE';
          badge.style.cssText =
            'background:#00BFB3;color:#000;font-size:10px;font-weight:700;padding:2px 8px;border-radius:10px;margin-left:8px;letter-spacing:1px;';

          var refreshBtn = document.createElement('button');
          refreshBtn.textContent = '\u27F3 Refresh';
          refreshBtn.style.cssText =
            'margin-left:auto;background:#00BFB3;color:#000;border:none;padding:6px 16px;border-radius:4px;cursor:pointer;font-weight:600;font-size:13px;';
          refreshBtn.onclick = function () {
            var iframe = el.querySelector('iframe');
            if (iframe) {
              iframe.src = iframe.src;
            }
          };

          header.appendChild(icon);
          header.appendChild(title);
          header.appendChild(badge);
          header.appendChild(refreshBtn);

          var statsBar = document.createElement('div');
          statsBar.style.cssText =
            'background:#161b22;padding:8px 24px;display:flex;gap:32px;flex-shrink:0;border-bottom:1px solid #2d333b;';

          var stats = [
            { label: 'AI Model', value: 'Mistral 7B (Local)' },
            { label: 'Threat Intel', value: 'VirusTotal + AbuseIPDB' },
            { label: 'Auto-Action', value: 'AWS Lambda IP Block' },
          ];

          stats.forEach(function (s) {
            var stat = document.createElement('div');
            stat.style.cssText = 'display:flex;flex-direction:column;';
            var lbl = document.createElement('span');
            lbl.textContent = s.label;
            lbl.style.cssText =
              'color:#8b949e;font-size:10px;text-transform:uppercase;letter-spacing:1px;';
            var val = document.createElement('span');
            val.textContent = s.value;
            val.style.cssText = 'color:#00BFB3;font-size:12px;font-weight:600;';
            stat.appendChild(lbl);
            stat.appendChild(val);
            statsBar.appendChild(stat);
          });

          var iframe = document.createElement('iframe');
          iframe.style.cssText = 'flex:1;width:100%;height:100%;min-height:600px;border:none;';
          iframe.src =
            '/app/dashboards#/view/a79805c0-a04d-11f1-aecc-29fd3dbb7b66?_g=(time:(from:now-7d,to:now))';
          iframe.setAttribute('allowfullscreen', 'true');

          el.appendChild(header);
          el.appendChild(statsBar);
          el.appendChild(iframe);

          return function () {
            el.innerHTML = '';
          };
        },
      });
      return {};
    };

    WazuhAiSocPlugin.prototype.start = function (core) {
      return {};
    };

    WazuhAiSocPlugin.prototype.stop = function () {};

    exports.plugin = function () {
      return new WazuhAiSocPlugin();
    };
  },
]);
