import os, shutil
import streamlit as st
from pathlib import Path
import playground as playground
from video_processing.video import Video
from zipfile import ZipFile
from os.path import basename
from PIL import Image

cur_path = os.path.dirname(__file__)
new_path = cur_path + '/video'

video_file = st.file_uploader(label = "Adicione um Vídeo", type=["avi"], accept_multiple_files=False)

if video_file:
    bytes_data = video_file.read()
    save_folder = os.path.realpath(__file__)[:-9] + 'video'
    save_path = Path(save_folder, 'video.avi')

    with open(save_path, mode='wb') as w:
        w.write(bytes_data)
    if save_path.exists():
        st.success(f'Arquivo {video_file.name} foi salvo com sucesso!')

number_of_components = st.number_input('Número de Componentes da Análise Modal', step = 1, format = "%i")
st.write('Número de Componentes: ', number_of_components)


if st.button('Comprimir Vídeo'):
    with st.spinner('Comprimindo Vídeo, por favor aguarde...'):
        folder = cur_path + '/binary_files'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        playground.video_compression(new_path + '/video.avi', number_of_components)

        with ZipFile('resultados.zip', 'w') as zipObj:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk('binary_files'):
                for filename in filenames:
                    # create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(filePath, basename(filePath))

        with open("resultados.zip", "rb") as fp:
            st.download_button(
                label="Baixar arquivos binários em Zip",
                data=fp,
                file_name="resultados.zip",
                mime="application/zip"
            )

        st.text(" ")
        st.text(" ")
        st.text(" ")

        image2 = Image.open('figures/sources.png')

        st.image(image2, caption='Fontes')

        image = Image.open('figures/modal coordinates.png')

        st.image(image, caption='Coordenadas Modais')



