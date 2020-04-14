import logging

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os.path import join
from wordcloud import WordCloud

from config import original_data_dir, generated_data_dir, log_format, figure_dir

logger = logging.getLogger(__name__)

def figure_path(name):
  return join(figure_dir, 'tag', name + '.png')

def generate_world_cloud(all_tag_list: pd.Series, figure_name):
  frequencies = {}
  for _, tag_list in all_tag_list.items():
    if pd.isnull(tag_list):
      continue
    words = str(tag_list).replace(', ', ',').split(',')
    for w in words:
      frequencies[w] = frequencies.setdefault(w, 0) + 1
  
  word_cloud = WordCloud(width=4000, height=3000, background_color='white', max_words=100)
  word_cloud.generate_from_frequencies(frequencies=frequencies)
  word_cloud.to_file(figure_path(figure_name))

def main():
  logging.basicConfig(format=log_format, level=logging.INFO)

  companies_path = join(generated_data_dir, 'companies.csv')
  ipos_path = join(original_data_dir, 'ipos.csv')
  acquisitions_path = join(original_data_dir, 'acquisitions.csv')

  companies = pd.read_csv(companies_path)
  ipos = pd.read_csv(ipos_path)
  acquisitions = pd.read_csv(acquisitions_path)
  
  ipo_companies = pd.merge(companies, ipos, left_on="id", right_on="object_id")
  acquisition_companies = pd.merge(companies, acquisitions, left_on="id", right_on="acquired_object_id")
  success_companies = pd.concat([ipo_companies[['id_x', 'tag_list']], acquisition_companies[['id_x', 'tag_list']]])

  # generate_world_cloud(companies['tag_list'], 'all')
  # generate_world_cloud(ipo_companies['tag_list'], 'ipo')
  # generate_world_cloud(acquisition_companies['tag_list'], 'acquisition')
  # generate_world_cloud(success_companies['tag_list'], 'success')

  tag_freq = {}

  for index, company in companies.iterrows():
    if pd.isnull(company['tag_list']):
      continue
    year = company['founded_year']
    if year not in tag_freq:
      tag_freq[year] = {}
    for tag in str(company['tag_list']).replace(', ', ',').split(','):
      if tag not in tag_freq[year]:
        tag_freq[year][tag] = 0
      tag_freq[year][tag] += 1

  # only take top 20 to speed up 
  for year, year_freq in tag_freq.items():
    tag_freq[year] = {
      k:v for k, v in sorted(year_freq.items(), key=lambda p : p[1], reverse=True)[0:20]
    }

  tag_freq = {
    year:year_freq for year, year_freq in sorted(tag_freq.items(), key=lambda p: p[0])
  }

  tag_by_year = pd.DataFrame.from_dict({(i, j) : tag_freq[i][j]
      for i in tag_freq.keys()
      for j in tag_freq[i].keys()}, 
    orient='index', columns=['value'])

  tag_by_year = pd.DataFrame({
    'name': [tag for year, tag in tag_by_year.index.values],
    'type': ['' for _ in tag_by_year.values],
    'value':[v[0] for v in tag_by_year.values],
    'date': [year for year, tag in tag_by_year.index.values]
  })
  tag_by_year.to_csv(join(generated_data_dir, 'tag_by_year.csv'), index=False)

if __name__ == '__main__':
  main()