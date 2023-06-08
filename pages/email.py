# -*- coding: utf-8 -*-

import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st
import pandas as pd
from RFM import create_rfm_dataset, rfm_segmentation, segmentation_map

st.sidebar.title("Рассылка")
st.title("RFM группы клиентов")


def send_email(to_address, subject, message, from_address, from_password):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, from_password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()


def load_data():
    text_file = st.sidebar.file_uploader("Загрузите датасет",
                                         type=["xlsx", "xls"])
    num_rows = st.sidebar.number_input(
        "Количество строк для загрузки", min_value=1, max_value=100000, value=5000, step=1000)  # 4372
    global df, rfm
    df = None
    if text_file is None:
        st.sidebar.warning("Датасет не загружен")
    else:
        try:
            df = pd.read_excel(text_file, nrows=num_rows)
            df = df[df['Quantity'] > 0]

            rfm = create_rfm_dataset(df)
            rfm = rfm_segmentation(rfm)
            rfm = segmentation_map(rfm)

            rfm = rfm.dropna()

        except ValueError as e:
            st.write(e)


load_data()

rfm = globals().get('rfm')
df = globals().get('df')

if df is None:
    st.error("Для работы загрузите датасет")
    sys.exit(1)

head_num = 7
clients_types = rfm['Segment'].unique()
for client_type in clients_types:
    st.write(f"Записи группы {client_type}")
    st.dataframe(rfm[rfm['Segment'] == client_type])



client_type = st.sidebar.selectbox("Выберите группу клиентов для рассылки", clients_types)

from_address = st.sidebar.text_input('Gmail от кого будет рассылка')
from_password = st.sidebar.text_input('Gmail пароль исходящей почты')
subject = st.sidebar.text_input('Тема сообщения')
message = st.sidebar.text_area('Текст сообщения')

if st.sidebar.button('Разослать'):
    rfm = rfm[rfm['Segment'] == client_type]
    for customer_id in rfm.index:
        email = df[df['CustomerID'] == customer_id]['Email'].values[0]
        send_email(email, subject, message, from_address=from_address, from_password=from_password)