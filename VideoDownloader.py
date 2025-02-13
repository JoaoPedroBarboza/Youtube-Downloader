import flet as ft 
import yt_dlp
import os
import subprocess

def download_video(url, page, open_folder_button):
    if not url:
        page.snack_bar = ft.SnackBar(ft.Text("Por favor, insira uma URL válida."))
        page.snack_bar.open = True
        page.update()
        return
    
    page.controls[2].value = "Baixando..."
    page.update()
    
    ydl_opts = {'format': 'best', 'outtmpl': f"%(title)s.%(ext)s"}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = os.path.abspath(f"{info['title']}.{info['ext']}")
        page.controls[2].value = "Download concluído!"
        open_folder_button.visible = True
        open_folder_button.data = os.path.dirname(file_path)
    except Exception as e:
        page.controls[2].value = "Erro no download."
    
    page.update()

def open_folder(e):
    folder_path = e.control.data
    if folder_path:
        subprocess.Popen(f'explorer "{folder_path}"' if os.name == 'nt' else ['xdg-open', folder_path])

def download_audio(url, page, open_folder_button_audio):
    if not url:
        page.snack_bar = ft.SnackBar(ft.Text("Por favor, insira uma URL válida."))
        page.snack_bar.open = True
        page.update()
        return

    page.controls[6].value = "Baixando áudio..."  # Índice ajustado
    page.update()

    ydl_opts = {
        'format': 'bestaudio/best',  # Seleciona o melhor áudio disponível
        'outtmpl': f"%(title)s.%(ext)s",
        'extract_flat': True # evita criar subdiretórios
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = os.path.abspath(f"{info['title']}.{info['ext']}")
        page.controls[6].value = "Download de áudio concluído!" # Índice ajustado
        open_folder_button_audio.visible = True
        open_folder_button_audio.data = os.path.dirname(file_path)
    except Exception as e:
        page.controls[6].value = f"Erro no download do áudio: {e}" # Índice ajustado

    page.update()


def open_folder(e):
    folder_path = e.control.data
    if folder_path:
        subprocess.Popen(f'explorer "{folder_path}"' if os.name == 'nt' else ['xdg-open', folder_path])

def main(page: ft.Page):
    page.title = "YouTube Video Downloader"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#1e1e2e"

    title = ft.Text("Baixar Videos/Áudios do YouTube", size=30, color="white", weight=ft.FontWeight.BOLD)
    url_input = ft.TextField(hint_text="Insira a URL", width=400, bgcolor="#2e2e3e", color="white")
    status_text_video = ft.Text("", color="white")
    download_button_video = ft.ElevatedButton("Baixar Vídeo", on_click=lambda _: download_video(url_input.value, page, open_folder_button_video), bgcolor="#ff5555", color="white")
    open_folder_button_video = ft.ElevatedButton("Abrir Pasta (Vídeo)", on_click=open_folder, visible=False, bgcolor="#ff5555", color="white")

    # Novos controles para download de áudio
    status_text_audio = ft.Text("", color="white")
    download_button_audio = ft.ElevatedButton("Baixar Áudio", on_click=lambda _: download_audio(url_input.value, page, open_folder_button_audio), bgcolor="#ff5555", color="white")
    open_folder_button_audio = ft.ElevatedButton("Abrir Pasta (Áudio)", on_click=open_folder, visible=False, bgcolor="#ff5555", color="white")


    page.add(
        title, 
        url_input, 
        status_text_video, 
        download_button_video, 
        open_folder_button_video,
        status_text_audio, # Adicionado o status do audio
        download_button_audio, # Botão de download de áudio
        open_folder_button_audio # Botão de abrir pasta de áudio
    )

ft.app(target=main)

