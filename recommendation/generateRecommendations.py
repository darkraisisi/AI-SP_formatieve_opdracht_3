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
            for buyerTypeAndProduct in allSimilarBuyersAndProducts[:100]:
                if buyerTypeAndProduct[0] in used:
                    continue
                else:
                    used.append(buyerTypeAndProduct[0])
                    recommendList.append(buyerTypeAndProduct[0])
                    if len(recommendList) == 4:
                        # Sorry voor de string manipulation
                        listString = str(recommendList).replace('[','{').replace(']','}').replace('\'','"')
                        insertSql = f"""INSERT INTO content_recommendations 
                            (segment,target_audience,product_recommendation)
                            VALUES ('{segment}','{target}','{listString}')"""
                        cursor.execute(insertSql)
                        recommendList = []
    


def content_recommendations():
    pass