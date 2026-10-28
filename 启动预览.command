#!/bin/zsh
cd "${0:A:h}"
if command -v node >/dev/null 2>&1; then
  node node_modules/vite/bin/vite.js --host 127.0.0.1
else
  "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node" node_modules/vite/bin/vite.js --host 127.0.0.1
fi
