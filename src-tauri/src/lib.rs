#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        // HTTP: permite ir buscar os feeds RSS sem bloqueios de CORS
        .plugin(tauri_plugin_http::init())
        // Opener: abre os links dos artigos no navegador do sistema
        .plugin(tauri_plugin_opener::init())
        .run(tauri::generate_context!())
        .expect("erro ao iniciar o Leitura");
}
