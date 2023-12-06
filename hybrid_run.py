#!/usr/bin/env python
# coding: utf-8

#import packages
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json
import gzip
from datetime import datetime
import warnings; warnings.simplefilter('ignore')

#read in datasets
#reading in data as pd dataframe
def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield json.loads(l)
def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')

df = getDF('Appliances.json.gz')

#extract relevant col from df
def simplify_df(df):
    columns_to_keep=['asin','reviewerID','overall']
    simple_df=df[columns_to_keep]
    return simple_df

#prepare item_to_users dataframe
def item_to_users_group(product_id, simple_df):
    #find all users who bought the product
    item_to_users=simple_df[simple_df['asin']==product_id]
    #only keep users who gave an overall of 5 and return list of user ids
    item_to_users=item_to_users[item_to_users['overall']==5]['reviewerID']
    return item_to_users

#prepare user_to_items dataframe
def user_to_items_group(user_id, simple_df):
    #find all prodcuts bought by the user
    user_to_items=simple_df[simple_df['reviewerID']==user_id]
    #only keep the product with overall of 5 and return list of product ids
    user_to_items=user_to_items[user_to_items['overall']==5]['asin']
    return user_to_items

#prepare popular product list
def popular_items(df):
    col_to_select=['asin','overall','unixReviewTime']
    popular_items_list=df[col_to_select]
    popular_items_list=popular_items_list[popular_items_list['overall']==5]
    popular_items_list['date'] = popular_items_list['unixReviewTime'].apply(lambda x: datetime.fromtimestamp(x))
    popular_items_list=popular_items_list[popular_items_list['date']>='2018-01-01']
    popular_items_list=popular_items_list.groupby('asin').filter(lambda x:x['overall'].count() >=50) #only keep the item with over 50 reviews
    popular_items_list=popular_items_list['asin']
    return popular_items_list

#loop function
def loop_item_based(product_id, item_to_users, simple_df, recommendation):
    for loop in range(len(item_to_users)):
        random_user=item_to_users.sample(n=1).iloc[0] #randomly select 1 user from the user pool
        user_to_items=user_to_items_group(random_user, simple_df) #find group of products to select 1 from
        if len(user_to_items)!=0: #select 1 product from the product pool
            random_product_recommend=user_to_items.sample(n=1).iloc[0]
            if ((random_product_recommend not in recommendation)&(random_product_recommend!=product_id)):
                recommendation.append(random_product_recommend)
        if len(recommendation)==5:
            break
    return recommendation

#recommend from populart items
def loop_popularity_based(popular_items_list, num_to_output):
    popular_item_recommended=[]
    popular_item_recommended=popular_items_list.sample(n=num_to_output).tolist()
    return popular_item_recommended

#loop the process & save in a list
def product_recommend(df, product_id):
    recommendation=[] #create the result df
    simple_df=simplify_df(df) #simplify the original df
    item_to_users=item_to_users_group(product_id, simple_df) #output relevant users based on the product input
    recommendation=loop_item_based(product_id, item_to_users, simple_df, recommendation) #loop to output recommendations
    
    if len(recommendation)<5: #loop if recommendation list is less than 5:
        popular_items_list=popular_items(df) #prepare popular item groups
        num_to_output=5-len(recommendation) #determine how many to output
        popular_item_recommended=loop_popularity_based(popular_items_list, num_to_output) #output products
        recommendation+=popular_item_recommended

    return recommendation

def main():
    # Read product_id from command line
    product_id = input("Enter product ID: ")
    # Call the product_recommend function
    result = product_recommend(df, product_id)
    print("Recommendations: ", result)
if __name__ == '__main__':
    main()




