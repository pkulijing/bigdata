import logging

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from string import punctuation
from os.path import join
from wordcloud import WordCloud
from unidecode import unidecode

from config import original_data_dir, generated_data_dir, log_format, figure_dir

logger = logging.getLogger(__name__)

def degree_code(degree):
  ''' Denote degree with a code. It's also the mark we use for calculating 
  average degree.
  Unknown: 0
  Below bachelor: 1
  Bachelor: 2
  Master: 3
  PhD: 4
  '''
  table = str.maketrans("", "", punctuation)
  degree = unidecode(str(degree)).translate(table).upper().replace(' ', '')
  if degree in ['AS', 'AA', 'AAS'] or any(s in degree for s in ['HS', 'HIGHSCHOOL', 'INCOMPLETE', 'PRIMARY', 'SECONDARY', 'MIDDLESCHOOL']):
    return 1
  elif degree.startswith('B') or any(s in degree for s in ['UNDERGRAD', 'BACHELOR', 'SB', 'LLB', 'AB', 'SCB', 'BSC']):
    return 2
  elif degree.startswith('M') or any(s in degree for s in['GRADUATE', 'INGENIE', 'MBA', 'MASTER', 'LLM', 'MSC', 'DIPLING', 'ENGINEER', 'SM', 'EXECUTIVE', 'MS']):
    return 3
  elif any(s in degree for s in ['PHD', 'JD', 'DOCTOR', 'POSTDOC', 'POSTGRADUATE', 'PDENG']):
    return 4
  else:
    return 0

def figure_path(name):
  return join(figure_dir, 'degree', name + '.png')

def main():
  logging.basicConfig(format=log_format, level=logging.INFO)

  degrees_path = join(original_data_dir, 'degrees.csv')
  relationships_path = join(original_data_dir, 'relationships.csv')
  companies_path = join(generated_data_dir, 'companies.csv')
  
  degrees = pd.read_csv(degrees_path)
  relationships = pd.read_csv(relationships_path)
  companies = pd.read_csv(companies_path)

  degree_relationship = pd.merge(degrees, relationships, left_on='object_id', right_on='person_object_id')
  degree_company = pd.merge(degree_relationship, companies, left_on='relationship_object_id', right_on='id')

  degree_company['degree_code'] = degree_company['degree_type'].map(degree_code)

  degree_company['degree_code'].value_counts().sort_index().plot(kind='pie', 
    title='Degree Distribution', labels=['Unknown', 'Lower than Bachelor', 'Bachelor', 'Master', 'PhD'],
    autopct='%d%%')
  plt.savefig(figure_path('degree_distribution'), bbox_inches='tight')
  plt.close()

  # print(degree_company[degree_company['degree_code'] == 0]['degree_type'].value_counts().head(40))
  # exclude people whose degree level is not clear
  degree_company = degree_company[degree_company['degree_code'] != 0]

  avg_degree_category = degree_company.groupby('category_code')['degree_code'].mean().sort_values(ascending=False)
  avg_degree_category.plot(kind='bar')
  plt.savefig(figure_path('average_degree_category'), bbox_inches='tight')
  plt.close()

  avg_degree_all = degree_company['degree_code'].mean()

  ipo_path = join(original_data_dir, 'ipos.csv')
  acquisition_path = join(original_data_dir, 'acquisitions.csv')

  ipos = pd.read_csv(ipo_path)
  acquisitions = pd.read_csv(acquisition_path)

  avg_degree_ipo = pd.merge(degree_company, ipos, left_on='relationship_object_id', right_on='object_id')['degree_code'].mean()
  avg_degree_acquisition = pd.merge(degree_company, acquisitions, left_on='relationship_object_id', right_on='acquired_object_id')['degree_code'].mean()
  
  avg_compare = pd.Series([avg_degree_all, avg_degree_ipo, avg_degree_acquisition], index=['All', 'IPO', 'Acquired'])
  avg_compare.plot(kind='bar')
  plt.savefig(figure_path('avg_degree_compare'), bbox_inches='tight')
  plt.close()



if __name__ == '__main__':
  main()