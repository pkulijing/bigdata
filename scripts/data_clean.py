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
  objects = pd.read_csv(object_path, usecols=['id','name', 'entity_type', 
    'category_code','status','founded_at','closed_at','tag_list','country_code', 'state_code',
    'first_funding_at','last_funding_at','funding_rounds','funding_total_usd'])

  companies = objects[objects['entity_type'] == 'Company']

  # only consider companies founded after 1990 and before 2014 (because the data was generated in 2013)
  companies = companies.loc[companies.founded_at.apply(lambda s: not pd.isnull(s)), :]
  companies['founded_year'] = companies['founded_at'].map(lambda s: int(str(s)[0:4]))
  companies = companies.loc[companies.founded_year.apply(lambda y : y > 1990 and y < 2014), :]
  
  company_path = join(generated_data_dir, 'companies.csv')
  companies.to_csv(company_path, index=False)

if __name__ == '__main__':
  main()