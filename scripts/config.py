from os.path import dirname, join

data_dir = join(dirname(__file__), '../data')
original_data_dir = join(data_dir, 'original')
generated_data_dir = join(data_dir, 'generated')
figure_dir = join(data_dir, 'figure')

log_format = "%(asctime)s %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"