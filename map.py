import folium
import folium.map
from folium.plugins import HeatMap
import pandas as pd
import webbrowser

from tratar_dados import TratarCidadesBrasil

dados_brasil = TratarCidadesBrasil()

dados_alunos = pd.read_csv("user.csv", usecols=[
    "username",
    "firstname",
    "city",
    "profile_field_instituicao",
    "profile_field_naturalidade"
    ])

dados_alunos = dados_alunos.dropna(subset=['city'])

cidades_do_brasil = dados_brasil.listar_cidades()

dados_alunos['city'] = dados_alunos['city'].apply(
    lambda city: dados_brasil.tratar_cidade(cidades_do_brasil, str(city))
    )

alunos_por_cidade = dados_alunos['city'].value_counts()
alunos_por_cidade = alunos_por_cidade.reset_index()
alunos_por_cidade.columns = ['nome', 'count']

alunos_por_cidade['latitude'] = alunos_por_cidade['nome'].map(lambda cidade: dados_brasil.pesquisar_latitude(cidade))
alunos_por_cidade['longitude'] = alunos_por_cidade['nome'].map(lambda cidade: dados_brasil.pesquisar_longitude(cidade))

cidades_em_manaus = []
quantidade = 0
df_auxiliar = alunos_por_cidade
for index, nome in enumerate(alunos_por_cidade['nome']):

    latitude = alunos_por_cidade.iloc[index]['latitude'].item()
    longitude = alunos_por_cidade.iloc[index]['longitude'].item()

    if (float(latitude) == -3.11866) and (float(longitude) == -60.0212):
        cidades_em_manaus.append(nome)
        quantidade += alunos_por_cidade.iloc[index]['count']
        df_auxiliar = df_auxiliar.drop(index)

cidades_em_manaus = ", ".join(cidades_em_manaus)

nova_linha = {
    'nome': cidades_em_manaus,
    'count': quantidade,
    'latitude': -3.11866,
    'longitude': -60.0212
}

df_nova_linha = pd.DataFrame([nova_linha])

alunos_por_cidade = pd.concat([df_auxiliar, df_nova_linha], ignore_index=True)

coordenadas = alunos_por_cidade[['latitude','longitude','count']].values.tolist()

baseMap = folium.Map(
    width ='100%',
    height ='100%',
    location=[-15.788497, -47.899873],
    zoom_start = 5
)
HeatMap(coordenadas, radius=15).add_to(baseMap)

for i in range(0, len(alunos_por_cidade)):
    folium.Circle(
        location=[alunos_por_cidade.iloc[i]['latitude'], alunos_por_cidade.iloc[i]['longitude']], 
        color='#000000',
        fill='#00000',
        tooltip='<li><bold> Cidade: '+str(alunos_por_cidade.iloc[i]['nome'])+
        '<li><bold> Quantidade: '+str(alunos_por_cidade.iloc[i]['count']),
        radius=100
    ).add_to(baseMap)

baseMap.save("map.html")
webbrowser.open("map.html")