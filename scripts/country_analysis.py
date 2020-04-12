import logging

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os.path import join

from config import original_data_dir, generated_data_dir, log_format, figure_dir

logger = logging.getLogger(__name__)

def plot_bar(series, figure_path):
  series.plot(kind='bar')
  plt.savefig(figure_path, bbox_inches='tight')
  plt.close()

def category_analysis(df, figure_path):
  counts = df['country_code'].value_counts()
  plot_bar(counts, figure_path)
  return counts

def figure_path(name):
  return join(figure_dir, 'country', name + '.png')

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

  # Too many countries. Only consider top N.
  
  considered_countries = companies['country_code'].value_counts().nlargest(40).index.to_list()

  considered_companies = companies[companies['country_code'].isin(considered_countries)]
  considered_ipo_copmanies = ipo_companies[ipo_companies['country_code'].isin(considered_countries)]
  considered_acquisition_companies = acquisition_companies[acquisition_companies['country_code'].isin(considered_countries)]

  all_counts = category_analysis(considered_companies, figure_path('count_company'))
  ipo_counts = category_analysis(considered_ipo_copmanies, figure_path('count_ipo'))
  acquisition_counts = category_analysis(considered_acquisition_companies, figure_path('count_acquisition'))

  success_counts = ipo_counts.add(acquisition_counts, fill_value=0).astype('int64').sort_values(ascending=False)
  plot_bar(success_counts, figure_path('count_success'))

  combine_counts = pd.concat(
    [ipo_counts, acquisition_counts, success_counts, all_counts], 
    axis=1)
  combine_counts.columns = ['ipo', 'acquisition', 'success', 'all']
  plot_bar(combine_counts, figure_path('count_combine'))

  ipo_rate = ipo_counts.divide(all_counts, fill_value=0).sort_values(ascending=False)
  acquisition_rate = acquisition_counts.divide(all_counts, fill_value=0).sort_values(ascending=False)
  success_rate = success_counts.divide(all_counts, fill_value=0).sort_values(ascending=False)
  plot_bar(ipo_rate, figure_path('rate_ipo'))
  plot_bar(acquisition_rate, figure_path('rate_acquisition'))
  plot_bar(success_rate, figure_path('rate_success'))

if __name__ == '__main__':
  main()