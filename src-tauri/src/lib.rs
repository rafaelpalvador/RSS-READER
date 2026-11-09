use tauri::Manager;

/// Guarda os títulos para o widget do Android (o widget lê este ficheiro).
#[tauri::command]
fn update_widget(app: tauri::AppHandle, json: String) -> Result<(), String> {
    let dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    std::fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    std::fs::write(dir.join("widget.json"), json).map_err(|e| e.to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        // HTTP: permite ir buscar os feeds RSS sem bloqueios de CORS
        .plugin(tauri_plugin_http::init())
        // Opener: abre os links dos artigos no navegador do sistema
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![update_widget])
        .run(tauri::generate_context!())
        .expect("erro ao iniciar o Leitura");
}
