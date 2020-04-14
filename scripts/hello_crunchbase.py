'''Let's say hello to our dataset'''

from csv import DictReader, DictWriter
from os.path import join
from os import listdir
import logging

from config import original_data_dir, generated_data_dir, log_format

logger = logging.getLogger(__name__)

def first_glance():
  '''First glance of the dataset

  Print the first row and count number of lines for each csv file.
  '''
  file_names = listdir(original_data_dir)
  logger.info(file_names)

  for file_name in file_names:
    line_count = 0
    file_path = join(original_data_dir, file_name)
    with open(file_path, 'r') as f:
      csv_reader = DictReader(f)
      first_row = next(csv_reader)

      for _ in csv_reader:
        line_count += 1
      logger.info('{} {} {}'.format(file_name, line_count, first_row))

def objects_overall():
  '''Overall information of objects.
  
  1. entity_types: what types of objects are included
  2. category_codes: what do the startups do
  '''
  objects_file_path = join(original_data_dir, 'objects.csv')
  with open(objects_file_path, 'r') as f:
    objects_reader = DictReader(f)
    entity_type_counts = {}
    category_code_counts = {}
    for row in objects_reader:
      entity_type_counts[row['entity_type']] = entity_type_counts.setdefault(row['entity_type'], 0) + 1  
      category_code_counts[row['category_code']] = category_code_counts.setdefault(row['category_code'], 0) + 1
  
  logger.info(entity_type_counts)
  logger.info(category_code_counts)

  return entity_type_counts, category_code_counts

def funding_overall():
  '''Overall information of startups funding
  '''
  funding_file_path = join(original_data_dir, 'funding_rounds.csv')

  with open(funding_file_path, 'r') as f:
    funding_reader = DictReader(f)
    funding_round_code_counts = {}
    funding_round_type_counts = {}
    for row in funding_reader:
      funding_round_code_counts[row['funding_round_code']] = funding_round_code_counts.setdefault(row['funding_round_code'], 0) + 1
      funding_round_type_counts[row['funding_round_type']] = funding_round_type_counts.setdefault(row['funding_round_type'], 0) + 1
 
  logger.info(funding_round_code_counts)
  logger.info(funding_round_type_counts)

  return funding_round_code_counts, funding_round_type_counts

def milestones_overall():
  '''Overall information of milestones

  Nothing interesting was found
  '''
  milestones_file_path = join(original_data_dir, 'milestones.csv')

  with open(milestones_file_path, 'r') as f:
    milestones_reader = DictReader(f)
    milestone_codes = set()
    for row in milestones_reader:
      milestone_codes.add(row['milestone_code'])
      
  logger.info(milestone_codes)

  return milestone_codes

def offices_overall():
  '''Overall information of startup offices
  '''
  offices_file_path = join(original_data_dir, 'offices.csv')

  with open(offices_file_path, 'r') as f:
    offices_reader = DictReader(f)
    country_counts = {}
    for row in offices_reader:
      country_counts[row['country_code']] = country_counts.setdefault(row['country_code'], 0) + 1
      
  logger.info(country_counts)

  return country_counts

def main():
  logging.basicConfig(format=log_format, level=logging.INFO)

  first_glance()
  objects_overall()
  funding_overall()
  milestones_overall()
  offices_overall() 

if __name__ == '__main__':
  main()