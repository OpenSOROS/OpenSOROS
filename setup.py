from setuptools import setup, find_packages

setup(name='opensoros',
      version='0.1',
      packages=find_packages(),
      install_requires=['numpy', 'scipy', 'scikit-learn',  'joblib', 'pandas', 'requests', 'gensim', 'matplotlib', 'tweepy', 'praw'])