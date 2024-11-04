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
from pytubefix import YouTube
import moviepy.editor
import os


st.set_page_config(layout = "centered")

st.title("Conversor de vídeo de youtube em Mp3 e Mp4")

URL = st.text_input(label = "URL do Youtube:",
                    placeholder = "https://www.youtube.com/watch?v=URL",
                    )

butao_MP3 = st.button(label = "Processar vídeo",
                      help = "Pressione para preparar a URL colocada para download")


def url_to_Mp3(url):
    
    try:

        vd = YouTube(url)
    except:
        return("ERRO")


    video = vd.streams.get_highest_resolution()
        
    path_p = video.download()
    
    base, ext = os.path.splitext(path_p) 
    new_file = base + '.mp4'
    os.rename(path_p, new_file)
    
    video = moviepy.editor.VideoFileClip(base + '.mp4')
    
    video.audio.write_audiofile(base + '.mp3')
    
    video.close()
    
    nome = base[base.find("Streamlit") + 10:]
    
    return([base + '.mp3', base + ".mp4",nome])
    

if "https://www.youtube.com" in URL and butao_MP3:
    
    with st.empty():
    
        carregando = st.write("Processando vídeo...")
    
        download = url_to_Mp3(URL)
         
        carregando = st.write(f"Escolha como quer baixar o vídeo: {download[2]}")
        
    
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
    else:
        st.write("Ocorreu um erro, verifique se a URL está correta!")
