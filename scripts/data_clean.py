import logging

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os.path import join

from config import original_data_dir, generated_data_dir, log_format, figure_dir

logger = logging.getLogger(__name__)

def main():
  logging.basicConfig(format=log_format, level=logging.INFO)

  object_path = join(original_data_dir, 'objects.csv')
  objects = pd.read_csv(object_path)

  companies = objects[objects['entity_type'] == 'Company'].loc[:, ['id','name', 
    'category_code','status','founded_at','closed_at','tag_list','country_code',
    'first_funding_at','last_funding_at','funding_rounds','funding_total_usd']]

  # only consider companies funded after 1990
  companies = companies.loc[companies.founded_at.apply(lambda s: not pd.isnull(s) and int(str(s)[0:4]) > 1990), :]
  company_path = join(generated_data_dir, 'companies.csv')
  companies.to_csv(company_path, index=False)

  # ipo_path = join(original_data_dir, 'ipos.csv')
  # ipos = pd.read_csv(ipo_path)

  # ipos = ipos.loc[ipos.public_at.apply(lambda s: not pd.isnull(s)), :]
  # ipo_new_path = join(generated_data_dir, 'ipos.csv')
  # ipos.to_csv(ipo_new_path, index=False)

  # acquisition_path = join(original_data_dir, 'acquisitions.csv')
  # acquisitions = pd.read_csv(acquisition_path)

  # acquisitions = acquisitions.loc[acquisitions.acquired_at.apply(lambda s: not pd.isnull(s)), :]
  # acquisition_new_path = join(generated_data_dir, 'acquisitions.csv')
  # acquisitions.to_csv(acquisition_new_path, index=False)

if __name__ == '__main__':
  main()