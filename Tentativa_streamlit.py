# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 14:15:35 2024

@author: user
"""

#cd Downloads
#teste\Scripts\activate
#cd Streamlit
#streamlit run Tentativa_streamlit.py

import streamlit as st
import os

from yt_dlp import YoutubeDL


st.set_page_config(layout = "centered")

st.title("Conversor de vídeo de youtube em Mp3 e Mp4")

URL = st.text_input(label = "URL do Youtube:",
                    placeholder = "https://www.youtube.com/watch?v=URL",
                    )

butao_MP3 = st.button(label = "Processar vídeo",
                      help = "Pressione para preparar a URL colocada para download")

def my_hook(d):
    if d['status'] == 'downloading':
        # Check if 'total_bytes' exists to avoid KeyError
        if 'total_bytes' in d and d['total_bytes'] is not None:
            progress = round(float(d['downloaded_bytes']) / float(d['total_bytes']) * 100, 1)
            st.write("Baixando... " + str(progress) + "%")
        else:
            # Fallback if total_bytes is unavailable
            st.write("Baixando... " + str(d['downloaded_bytes']) + " bytes")

    
def download_audio(link):
  with YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': 'resultado.mp3','progress_hooks': [my_hook]}) as video:
    info_dict = video.extract_info(link, download = True)
    video_title = info_dict['title']
    video.download(link)
    
    
    return("resultado.mp3",video_title)

def download_video(link):
  with YoutubeDL({'extract_audio': True,"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",'outtmpl': 'resultado.mp4','progress_hooks': [my_hook]}) as video:
    info_dict = video.extract_info(link, download = True)
    video_title = info_dict['title']
    video.download(link)
    
    return("resultado.mp4",video_title)

if "https://www.youtube.com" in URL and butao_MP3:
    
    #st.write(os.listdir(os.path.abspath(os.getcwd())))
    
    #removendo os arquivos anteriores
    arquivos = os.listdir(os.path.abspath(os.getcwd()))
    for i in arquivos:
        if ".mp3" in i or ".mp4" in i:
            os.remove(os.path.abspath(os.getcwd() +"/" +i))
    
    with st.empty():
    
        carregando = st.write("Processando vídeo...")
        
        d1,t = download_audio(URL)
        
        d2,t = download_video(URL)
        
        download = [d1,d2,t]
         
        carregando = st.write(f"Escolha como quer baixar o vídeo: {download[2]}")
        
    arquivos = os.listdir(os.path.abspath(os.getcwd()))
    
    #print("\n\n",os.listdir(os.path.abspath(os.getcwd())))
    
    if type(download) == type([]): 
    
        col1,col2 = st.columns([1,1])
        
        with open(download[0],"rb") as file:
            col1.download_button("Download Mp3",
                               data = file,
                               file_name = download[2] + ".mp3"
                               )
            
        with open(download[1],"rb") as file:
            col2.download_button("Download Mp4",
                               data = file,
                               file_name = download[2] + ".mp4"
                               )
        
        #removendo os arquivos feitos
        for i in arquivos:
            if ".mp3" in i or ".mp4" in i:
                os.remove(os.path.abspath(os.getcwd() +"/" +i))
        
        
        
    else:
        st.write("Ocorreu um erro, verifique se a URL está correta!")