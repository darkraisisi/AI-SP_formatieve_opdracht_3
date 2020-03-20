import psycopg2
import csv
from datetime import datetime

connection = psycopg2.connect(user="postgres",
                                password="root",
                                host="localhost",
                                port="5432",
                                database="OpisOp")

cursor = connection.cursor()

def run():
    collab_recommendations(
        ['BOUNCER','JUDGER','LEAVER','BUYER','BROWSER','COMPARER','FUN_SHOPPER'],
        ['familie'])
    content_recommendations()

    connection.commit()
    cursor.close()
    connection.close()

def collab_recommendations(segmentList,targetAudienceList):
    # Er bleek nog een probleem te zitten in mijn database ik had geen gender/target audience nog, als placeholder doe ik het type persoon
    # SELECT cart.products_id, cart.sessions_profiles_id, sessions.segment FROM cart
    # INNER JOIN sessions ON cart.sessions_profiles_id = sessions.browser_id
    # WHERE sessions.segment = 'BOUNCER' 
    # -- AND sessions.target_audience = 'familie'
    # AND sessions.segment IS NOT NULL
    for segment in segmentList:
        for target in targetAudienceList:
            sql = f"""SELECT DISTINCT cart.products_id, cart.sessions_profiles_id, sessions.segment FROM cart
            INNER JOIN sessions ON cart.sessions_profiles_id = sessions.browser_id
            WHERE sessions.segment = '{segment}' 
            -- AND sessions.target_audience = '{target}'
            AND sessions.segment IS NOT NULL
            ORDER BY cart.products_id ASC"""
            cursor.execute(sql)
            allSimilarBuyersAndProducts = cursor.fetchall()
            used = []
            recommendList = []
            for buyerTypeAndProduct in allSimilarBuyersAndProducts:
                if buyerTypeAndProduct[0] in used:
                    continue
                else:
                    used.append(buyerTypeAndProduct[0])
                    recommendList.append(buyerTypeAndProduct[0])
                    if len(recommendList) == 4:
                        # Sorry voor de string manipulation
                        listString = str(recommendList).replace('[','{').replace(']','}').replace('\'','"')
                        insertSql = f"""INSERT INTO collab_recommendations 
                            (segment,target_audience,product_recommendation)
                            VALUES ('{segment}','{target}','{listString}')"""
                        cursor.execute(insertSql)
                        recommendList = []
    


def content_recommendations():
    sql = """SELECT p.id,p.name,p.category,p.sub_category,p.sub_sub_category, COUNT (cart.products_id) AS WOW
            FROM products AS p
            FULL OUTER JOIN cart ON p.id = cart.products_id
            GROUP BY p.id,p.name,p.category,p.sub_category,p.sub_sub_category,cart.bought
            ORDER BY p.category,p.sub_category,p.sub_sub_category, COUNT(cart.products_id) DESC"""
    cursor.execute(sql)
    similarProducts = cursor.fetchall() #groupedby amount bought in order of category importance
# [('36344-Purple Party', 'Saffron Glitter Nagellak Purple Party', "['Make-up & geuren', 'Make-up', 'Nagellak']", None, None, 0), ('45647', 'Ijsblokjes Zakjes 38x17cm 10st', '50% korting', None, None, 1), ('45708', 'Waterzone Watergun 33x4cm 2ass', '50% korting', None, None, 0), ('45710', 'Lifetime Garden Zonnescherm 3.6x3.6x3.6m', '50% korting', None, None, 0), ('45712', 'Bier Pong-Spel', '50% korting', None, None, 0), ('45714', 'Drinkfles Met Infuser 600ml 4ass', '50% korting', None, None, 0), ('45707', 'Ijsblokjes Vorm 6ass', '50% korting', None, None, 0), ('45715', 'Vliegenkap Food Cover 32x32cm 2ass', '50% korting', None, None, 0), ('45716', 'Zwembril pro racer 3ass PL', '50% korting', None, None, 0), ('45697', 'Isoleerkan 1Liter 6ass', '50% korting', None, None, 0)]
    recommendList = []
    for product in similarProducts:
        if product[4]: #category
            category = product[4]
            if product[3]: #sub_category
                category = product[3]
                if product[2]: #sub_sub_category
                    category = product[2]
                    recommendList.append(product[0])

        if len(recommendList) == 4:
            # Sorry voor de string manipulation
            listString = str(recommendList).replace('[','{').replace(']','}').replace('\'','"')
            insertSql = f"""INSERT INTO content_recommendations 
                (category,product_recommendation)
                VALUES ('{category}','{listString}')"""
            recommendList = []
            cursor.execute(insertSql)