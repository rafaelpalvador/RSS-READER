# Leitura

Leitor de RSS pessoal: junta os feeds que sigo, ordena-os pelo que me interessa e resume cada artigo.

- **Hoje** — artigo escolhido para mim, sugestões e o feed agrupado por relevância, data ou país.
- **Feeds** — diretório de jornais por país, região, língua e tema (com destaque para o Brasil e a Europa), "joias escondidas", pesquisa de sites na web e feeds de temas ao estilo Google News.
- **Interesses** — temas e perguntas que definem o que aparece primeiro; palavras silenciadas.
- **Biblioteca** — artigos guardados e destaques, exportáveis em Markdown para o Marginália.

Feito com [Tauri 2](https://tauri.app). O app inteiro está em `src/index.html`.

## Instalar

- **Android (Obtainium):** adicionar `https://github.com/rafaelpalvador/rss-reader`. Só existe sempre uma versão publicada, a mais recente.
- **Windows:** descarregar o `.exe` em [Releases](https://github.com/rafaelpalvador/rss-reader/releases/latest).

Cada `push` para `main` gera uma versão nova (`0.1.<n.º da build>`) através do GitHub Actions.

## Assinatura do Android

A APK é assinada com `keystore/leitura.jks`, para que as atualizações instalem por cima da versão anterior.
Para maior segurança, pode-se mudar para segredos do GitHub (`ANDROID_KEYSTORE_BASE64`, `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`) — o workflow usa-os automaticamente quando existem. **Usar sempre a mesma chave**, senão o Android recusa a atualização.

## Desenvolver no PC

```bash
npm install
npx tauri icon app-icon.png
npx tauri dev
```
