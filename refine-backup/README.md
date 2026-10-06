# 1luv - Megacrew

Página WordPress 11345, em rascunho. Implementação no widget HTML Elementor `e664712`, container `b48269b`.

Referência: frame MEGACREW-REFORMA do arquivo Figma MEGA-CREW-26. Desktop com geometria original de 1440 × 12045 px; mobile e tablet com conteúdo reorganizado até 900 px.

## Arquivos

- `build_page.py`: gera o HTML a partir dos dados originais do Figma.
- `page.css` e `page.js`: estilos responsivos e interações.
- `megacrew.html`: conteúdo salvo no Elementor.
- `media-map.json`: URLs e IDs dos 61 assets importados no WordPress.
- `assets/`: assets WebP exportados do Figma e fontes Ageo/Katl em WOFF.
- `previous-page.json`: backup da estrutura anterior.
- `megacrew-metadata-v2.json`: dados originais dos elementos e textos.

## Destinos pendentes

- Inscrição: os CTAs direcionam provisoriamente à seção de valor.
- Vídeo de apresentação: o frame e o ícone de play foram preservados; vídeo ainda não conectado.
- TikTok: rótulo preservado, sem destino até confirmação da URL.

O WhatsApp usa o canal público de comunidade indicado no site Dunamis Movement. Instagram e YouTube usam os perfis do Dunamis 1Luv.

Para regenerar o arquivo: `python3 build_page.py` (fontTools e fontes originais locais necessários). A atualização no Elementor deve enviar `megacrew.html` para o widget existente.
