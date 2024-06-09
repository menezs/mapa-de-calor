import pandas as pd
import unicodedata
import re

DEFAULT = 'https://raw.githubusercontent.com/kelvins/municipios-brasileiros/main/csv/municipios.csv'

class TratarCidadesBrasil:

    def __init__(self, path_cidades_info=DEFAULT):

        self.cidades_info = pd.read_csv(path_cidades_info)
        """
        DataFrame contendo 'nome', 'latitude' e 'longitude'
        das cidades do Brasil.
        """        
        
    def listar_cidades(self):
        """
        Lista o nome de Todos os Municipios do Brasil
        com a primeira letra do nome em Maiusculo.

        Returns:
            list: Nome dos municipios do Brasil
        """        

        self.cidades_info['nome'] = self.cidades_info['nome'].apply(lambda city: str(city).capitalize())
        self.cidades_info['nome'] = self.cidades_info['nome'].apply(lambda city: self.remover_acentuacao(str(city)))

        cidades_do_brasil = self.cidades_info['nome'].to_list()

        return cidades_do_brasil
    
    def remover_acentuacao(self, texto):
        """
        Normaliza um texto de entrada para uma versão
        sem acentuação.

        Args:
            texto (string): Texto com Acentuação

        Returns:
            string: Texto sem acentuação
        """        
    
        texto_normalizado = unicodedata.normalize('NFD', texto)
        
        texto_sem_acento = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')
        
        return texto_sem_acento

    def tratar_cidade(self, nome_cidades_do_brasil, cidade):
        """
        Verifica e Padroniza o nome de uma Cidade
        para o mesmo padrão da Base DEFAULT.

        Args:
            nome_cidades_do_brasil (list): Lista com o Municipios do Brasil
            cidade (string): Nome de uma possível cidade do Brasil

        Returns:
            string: Nome Padronizado
        """

        cidade = cidade.split('-')[0]
        cidade = re.sub(r'\d+|\|', '', cidade)
        cidade = self.remover_acentuacao(cidade)
        
        if ("/" in cidade) or ("," in cidade):
            
            cidade_split = cidade.split("/")
            if len(cidade_split) < 2:
                cidade_split = cidade.split(",")
            
            cidade = cidade_split[1].strip().capitalize()
            
            if cidade not in nome_cidades_do_brasil:
                cidade = cidade_split[0].strip().capitalize()
                
        cidade = cidade.strip().capitalize()
    
        return cidade

    def pesquisar_latitude(self, cidade):
        """
        Pesquisa a latitude de uma cidade na Base DEFAULT.

        Args:
            cidade (string): Nome de uma determinada Cidade.

        Returns:
            float: Latitude de uma cidade
        """
        latitude = self.cidades_info[self.cidades_info['nome'] == "Manaus"]['latitude']
        
        nomes_cidades_do_brasil = self.cidades_info['nome'].apply(lambda city: str(city).capitalize()).to_list()
            
        if cidade in nomes_cidades_do_brasil:

            latitude = self.cidades_info[self.cidades_info['nome'] == cidade].iloc[0]['latitude']

        return latitude
    
    def pesquisar_longitude(self, cidade):
        """
        Pesquisa a Longitude de uma cidade na Base DEFAULT.

        Args:
            cidade (string): Nome de uma determinada Cidade.

        Returns:
            float: Longitude de uma cidade
        """

        longitude = self.cidades_info[self.cidades_info['nome'] == "Manaus"]['longitude']
        
        nomes_cidades_do_brasil = self.cidades_info['nome'].apply(lambda city: str(city).capitalize()).to_list()
            
        if cidade in nomes_cidades_do_brasil:

            longitude = self.cidades_info[self.cidades_info['nome'] == cidade].iloc[0]['longitude']

        return longitude