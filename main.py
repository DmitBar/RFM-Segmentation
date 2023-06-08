import streamlit as st
import pandas as pd
# from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
# kneed
from kneed import KneeLocator
from sklearn.preprocessing import StandardScaler
from KmeansCustom import optimal_number_cluster_kmeans
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import sys
import plotly.express as px
from RFM import create_rfm_dataset, rfm_segmentation, segmentation_map

st.title("RFM сегментация")  # заголовок
st.sidebar.title("RFM сегментация")


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


def main():
    load_data()
    rfm = globals().get('rfm')
    df = globals().get('df')

    head_num = 10

    if df is not None:
        st.write(f'Первые {head_num} записей загруженного датасета')
        st.dataframe(df.head(head_num))
    else:
        st.error("Для работы загрузите датасет")
        sys.exit(1)

    st.write(f'Первые {head_num} записей RFM конвертированного датасета')
    st.dataframe(rfm.head(head_num))


    columns = ['Frequency', 'Monetary']

    rfm['CustomerID'] = rfm.index

    fig = px.scatter(rfm, x=columns[0], y=columns[1],
        color="Segment", title='RFM сегментация',
        hover_data=['CustomerID', 'Segment', 'Frequency', 'Monetary'],
        labels={
                 "Monetary": "Выручка с клиента",
                 "Frequency": "Частота покупок"
             },
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    st.plotly_chart(fig)

    type_file = st.selectbox('Выберите тип файла', ['csv', 'xlsx', 'xls'])
    if st.button('Сохранить датасет'):
        if type_file == "csv":
            rfm.to_csv(f"rfm.csv", index=False)
        elif type_file in ("xlsx", "xls"):
            rfm.to_excel(f"rfm.xlsx", index=False)
        else:
            raise ValueError("Неверный тип файла.")

        st.write("Датасет успешно сохранен.")



if __name__ == "__main__":
    main()






