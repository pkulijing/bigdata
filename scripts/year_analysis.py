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
  return join(figure_dir, 'year', name + '.png')

def main():
  logging.basicConfig(format=log_format, level=logging.INFO)

  companies_path = join(generated_data_dir, 'companies.csv')
  ipos_path = join(original_data_dir, 'ipos.csv')
  acquisitions_path = join(original_data_dir, 'acquisitions.csv')

  companies = pd.read_csv(companies_path)
  companies['founded_year'] = companies['founded_at'].map(lambda s: int(str(s)[0:4]))
  ipos = pd.read_csv(ipos_path)
  acquisitions = pd.read_csv(acquisitions_path)

  ipo_companies = pd.merge(companies, ipos, left_on="id", right_on="object_id")
  acquisition_companies = pd.merge(companies, acquisitions, left_on="id", right_on="acquired_object_id")

  funding_rounds_path = join(original_data_dir, 'funding_rounds.csv')
  funding_rounds = pd.read_csv(funding_rounds_path)
  funding_rounds = funding_rounds.loc[funding_rounds.funded_at.apply(lambda s: not pd.isnull(s) and int(str(s)[0:4]) > 1990), :]

  funding_rounds['funded_year'] = funding_rounds.funded_at.map(lambda s : int(str(s)[0:4]))

  amounts_by_year = funding_rounds.groupby('funded_year')['raised_amount_usd'].sum() / 1000000

  figure_path = join(figure_dir, 'year', 'funding_amount.png')
  amounts_by_year.plot(kind='bar')
  plt.savefig(figure_path, bbox_inches='tight')
  plt.close()


if __name__ == '__main__':
  main()