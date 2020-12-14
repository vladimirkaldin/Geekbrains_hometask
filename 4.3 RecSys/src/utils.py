

def prefilter_items(data, data_train):
    # Уберем самые популярные товары (их и так купят)
    popularity = data_train.groupby('item_id')['user_id'].nunique().reset_index() / data_train['user_id'].nunique()
    popularity.rename(columns={'user_id': 'share_unique_users'}, inplace=True)
    
    top_popular = popularity[popularity['share_unique_users'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]
    
    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['share_unique_users'] < 0.01].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]
    
    print(data.shape[0])
    
    return data
    


def postfilter_items(user_id, recommednations):
    pass


def get_similar_items_recommendation(user, model, item, N=5):
    '''Рекомендуем товары, похожие на топ-N купленных юзером товаров'''
    res = [id_to_itemid[rec[0]] for rec in model.similar_items(itemid_to_id[item], N=N)]
    return res
    


def get_similar_users_recommendation(user, model, sparse_user_item, item, N=5):
    '''Рекомендуем топ-N товаров'''

    res = [id_to_itemid[rec[0]] for rec in 
                    model.recommend(userid=userid_to_id[user], 
                                    user_items=sparse_user_item,   # на вход user-item matrix
                                    N=N, 
                                    filter_already_liked_items=False, 
                                    filter_items=[itemid_to_id[item]],  
                                    recalculate_user=True)]
    return res
        
