user3 = feature3[['user_id','merchant_id','coupon_id','discount_rate','distance','date_received','date']]

t = user3[['user_id']]
t.drop_duplicates(inplace=True)

t1 = user3[user3.date!='null'][['user_id','merchant_id']]
t1.drop_duplicates(inplace=True)
t1.merchant_id = 1
t1 = t1.groupby('user_id').agg('sum').reset_index()
t1.rename(columns={'merchant_id':'count_merchant'},inplace=True)

t2 = user3[(user3.date!='null')&(user3.coupon_id!='null')][['user_id','distance']]
t2.replace('null',-1,inplace=True)
t2.distance = t2.distance.astype('int')
t2.replace(-1,np.nan,inplace=True)
t3 = t2.groupby('user_id').agg('min').reset_index()
t3.rename(columns={'distance':'user_min_distance'},inplace=True)

t4 = t2.groupby('user_id').agg('max').reset_index()
t4.rename(columns={'distance':'user_max_distance'},inplace=True)

t5 = t2.groupby('user_id').agg('mean').reset_index()
t5.rename(columns={'distance':'user_mean_distance'},inplace=True)

t6 = t2.groupby('user_id').agg('median').reset_index()
t6.rename(columns={'distance':'user_median_distance'},inplace=True)

t7 = user3[(user3.date!='null')&(user3.coupon_id!='null')][['user_id']]
t7['buy_use_coupon'] = 1
t7 = t7.groupby('user_id').agg('sum').reset_index()

t8 = user3[user3.date!='null'][['user_id']]
t8['buy_total'] = 1
t8 = t8.groupby('user_id').agg('sum').reset_index()

t9 = user3[user3.coupon_id!='null'][['user_id']]
t9['coupon_received'] = 1
t9 = t9.groupby('user_id').agg('sum').reset_index()

t10 = user3[(user3.date_received!='null')&(user3.date!='null')][['user_id','date_received','date']]
t10['user_date_datereceived_gap'] = t10.date + ':' + t10.date_received
t10.user_date_datereceived_gap = t10.user_date_datereceived_gap.apply(get_user_date_datereceived_gap)
t10 = t10[['user_id','user_date_datereceived_gap']]

t11 = t10.groupby('user_id').agg('mean').reset_index()
t11.rename(columns={'user_date_datereceived_gap':'avg_user_date_datereceived_gap'},inplace=True)
t12 = t10.groupby('user_id').agg('min').reset_index()
t12.rename(columns={'user_date_datereceived_gap':'min_user_date_datereceived_gap'},inplace=True)
t13 = t10.groupby('user_id').agg('max').reset_index()
t13.rename(columns={'user_date_datereceived_gap':'max_user_date_datereceived_gap'},inplace=True)


user3_feature = pd.merge(t,t1,on='user_id',how='left')
user3_feature = pd.merge(user3_feature,t3,on='user_id',how='left')
user3_feature = pd.merge(user3_feature,t4,on='user_id',how='left')
user3_feature = pd.merge(user3_feature,t5,on='user_id',how='left')
user3_feature = pd.merge(user3_feature,t6,on='user_id',how='left')
user3_feature = pd.merge(user3_feature,t7,on='user_id',how='left')
user3_feature = pd.merge(user3_feature,t8,on='user_id',how='left')
user3_feature = pd.merge(user3_feature,t9,on='user_id',how='left')
user3_feature = pd.merge(user3_feature,t11,on='user_id',how='left')
user3_feature = pd.merge(user3_feature,t12,on='user_id',how='left')
user3_feature = pd.merge(user3_feature,t13,on='user_id',how='left')
user3_feature.count_merchant = user3_feature.count_merchant.replace(np.nan,0)
user3_feature.buy_use_coupon = user3_feature.buy_use_coupon.replace(np.nan,0)
user3_feature['buy_use_coupon_rate'] = user3_feature.buy_use_coupon.astype('float') / user3_feature.buy_total.astype('float')
user3_feature['user_coupon_transfer_rate'] = user3_feature.buy_use_coupon.astype('float') / user3_feature.coupon_received.astype('float')
user3_feature.buy_total = user3_feature.buy_total.replace(np.nan,0)
user3_feature.coupon_received = user3_feature.coupon_received.replace(np.nan,0)
user3_feature.to_csv('data/user3_feature.csv',index=None)
