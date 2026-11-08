// Esconde a consola no Windows em modo release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    rss_reader_lib::run()
}
