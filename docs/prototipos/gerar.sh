#!/usr/bin/env bash
# Exporta cada wireframe .html para .png, que é o formato que entra no
# documento. Precisa de um Chromium ou Chrome e do ImageMagick no PATH.
#
#   ./gerar.sh
#
# Editar sempre o .html, nunca o .png: o .png é gerado.
set -euo pipefail
cd "$(dirname "$0")"

navegador=$(command -v chromium || command -v chromium-browser || command -v google-chrome-stable || true)
[ -n "$navegador" ] || { echo "faltando: chromium" >&2; exit 1; }
command -v magick >/dev/null || { echo "faltando: magick" >&2; exit 1; }

for html in listagem leitura cadastro editor meus-textos; do
    # Janela alta demais de propósito: o corte tira a sobra depois, e assim
    # nenhuma tela precisa de altura própria escrita à mão.
    "$navegador" --headless --disable-gpu --hide-scrollbars \
        --screenshot="$html.png" --window-size=1040,1600 \
        --virtual-time-budget=2000 "file://$PWD/$html.html" 2>/dev/null

    magick "$html.png" -bordercolor white -border 10 -trim +repage "$html.png"
    echo "$html.png"
done
