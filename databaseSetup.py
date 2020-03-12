import psycopg2


""" Run this file to generate the whole database, you only need to personify the parameters of the postgresql database to acces your database """

def run():

    connection = psycopg2.connect(user="postgres",
                                password="root",
                                host="localhost",
                                port="5432",
                                database="OpisOp")
    cursor = connection.cursor()

    cursor.execute(
                """DROP TABLE IF EXISTS brand CASCADE;

                CREATE  TABLE IF NOT EXISTS brand (
                id SERIAL ,
                name VARCHAR(255) NOT NULL ,
                PRIMARY KEY (id) )"""
    )

    cursor.execute(
                """DROP TABLE IF EXISTS products CASCADE;

                    CREATE TABLE IF NOT EXISTS products (
                        id INT NOT NULL ,
                        name VARCHAR(255) NULL ,
                        gender VARCHAR(255) NULL ,
                        category VARCHAR(255) NULL ,
                        subcategory VARCHAR(255) NULL ,
                        subsubcategory VARCHAR(255) NULL ,
                        brand_id INT,

                        PRIMARY KEY (id),
                        CONSTRAINT fk_products_brand1
                        FOREIGN KEY (brand_id)
                        REFERENCES brand (id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE)"""
    )

    cursor.execute(
                """DROP TABLE IF EXISTS profiles CASCADE;

                    CREATE TABLE IF NOT EXISTS profiles (
                        id INT NOT NULL ,
                        order_amount INT NOT NULL DEFAULT 0 ,
                PRIMARY KEY (id) );
    """
    )

    cursor.execute(
                """DROP TABLE IF EXISTS sessions CASCADE;

                    CREATE TABLE IF NOT EXISTS sessions (
                        id SERIAL ,
                        browser_id VARCHAR(255) NOT NULL ,
                        segment VARCHAR(255) NULL ,
                        orders text NULL,
                        profiles_id INT NULL ,
                PRIMARY KEY (id));
    """
    )

    cursor.execute(
                """DROP TABLE IF EXISTS cart_has_products CASCADE;

                    CREATE TABLE IF NOT EXISTS cart_has_products (
                        products_id INT NOT NULL ,
                        sessions_id INT NOT NULL ,
                        bought BOOLEAN NOT NULL ,
                PRIMARY KEY (products_id, sessions_id) ,
                FOREIGN KEY (products_id )
                REFERENCES products (id )
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
                FOREIGN KEY (sessions_id )
                REFERENCES sessions (id )
                ON DELETE NO ACTION
                ON UPDATE NO ACTION)
    """
    )


    connection.commit()
    cursor.close()
    connection.close()
    print("PostgreSQL datebase is generated")