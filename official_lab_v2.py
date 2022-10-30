# Học thêm tại: https://dash.plotly.com/

# Run this app with `python app.py` and

# visit http://127.0.0.1:8050/ in your web browser.

# BẤM CTRL '+' C ĐỂ TẮT APP ĐANG CHẠY

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# TẢI DỮ LIỆU TỪ FIRESTORE
cred = credentials.Certificate("./huynh-tan-dat-firebase-adminsdk-wb8f1-f9d176e7d4.json")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'tbl-20073701').where(u'DEALSIZE', u'==', 'Large').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)

df["YEAR_ID"] = df["YEAR_ID"].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("str")

# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = Dash(__name__)

app.title = "Finance Data Analysis"

figSoLuongSanPham = px.histogram(df, x="YEAR_ID", y="QUANTITYORDERED", 
barmode="group", color="QTR_ID", title='Tổng số lượng sản phẩm theo quý và năm', histfunc = "sum",
labels={'YEAR_ID':'Từ năm 2003, 2004 và 2005', 'QTR_ID': 'Quý trong năm', 'Sum':'Tổng số lượng sản phẩm'})

figDoanhSo = px.pie(df, values='SALES', names='YEAR_ID',
labels={'YEAR_ID':'Năm','SumSaleQTRYEAR':'Doanh số'},
title='Tổng doanh số theo năm')

figSoLuongHoaDon = px.sunburst(df, path=['YEAR_ID', 'QTR_ID'], values='QUANTITYORDERED',
color='QUANTITYORDERED',
labels={'parent':'Năm', 'labels':'Quý','QUANTITYORDERED':'Số lượng sản phẩm'},
title='Tỉ lệ số lượng sản phẩm theo quý và năm')

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="DATA DASHBOARD", className="header-title"
                )],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H2(
                            children="REVENUE: CURRENT MONTH", className="general-header-title"
                        ),
                        html.H3(
                            children="Descriptions", className="general-header-description"
                        )
                    ],
                    className="general-header-item"
                ),
                html.Div(
                    children=[
                        html.H2(
                            children="HIGHEST SIGNUPS", className="general-header-title"
                        ),
                        html.H3(
                            children="Descriptions", className="general-header-description"
                        )
                    ],
                    className="general-header-item"
                ),
                html.Div(
                    children=[
                        html.H2(
                            children="TOP MARKETING STRATEGY", className="general-header-title"
                        ),
                        html.H3(
                            children="Descriptions", className="general-header-description"
                        )
                    ],
                    className="general-header-item"
                ),
                html.Div(
                    children=[
                        html.H2(
                            children="MAX TEMP: CAMBRIDGE", className="general-header-title"
                        ),
                        html.H3(
                            children="Descriptions", className="general-header-description"
                        )
                    ],
                    className="general-header-item"
                )
            ],
            className="general-header"
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                    id='soluong-graph',
                    figure=figSoLuongSanPham),
                    className="card"
                ),
                html.Div(
                    children=dcc.Graph(
                    id='doanhso-graph',
                    figure=figDoanhSo),
                    className="card"
                ),
                html.Div(
                    children=dcc.Graph(
                    id='soluongdonhang-graph',
                    figure=figSoLuongHoaDon),
                    className="card"
                ),
                html.Div(
                    children=dcc.Graph(
                    id='soluongdonhang-graph2',
                    figure=figSoLuongHoaDon),
                    className="card"
                )
            ], className="wrapper")
    ])

figSoLuongSanPham.update_layout(title='<b>Tổng số lượng sản phẩm theo quý và năm</b>',title_x=0.5, title_font_size=20)
figDoanhSo.update_layout(title='<b>Tổng doanh số theo năm</b>',title_x=0.5, title_font_size=20)
figSoLuongHoaDon.update_layout(title='<b>Tỉ lệ số lượng sản phẩm theo quý và năm</b>',title_x=0.5, title_font_size=20)
# figSoLuongSanPham.update_layout(title_x=0.5)

if __name__ == '__main__':
    app.run_server(debug=True, port=8090)