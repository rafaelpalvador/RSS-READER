// Define a versão do app a partir do número da build do GitHub Actions (ex.: 0.1.42)
import fs from 'node:fs';
const v = process.argv[2];
const f = 'src-tauri/tauri.conf.json';
const c = JSON.parse(fs.readFileSync(f, 'utf8'));
c.version = v;
fs.writeFileSync(f, JSON.stringify(c, null, 2));
console.log('Versão:', v);
