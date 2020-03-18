-- -----------------------------------------------------
-- Table brand
-- -----------------------------------------------------

DROP SEQUENCE IF EXISTS brand_seq CASCADE;
CREATE SEQUENCE brand_seq;

DROP TABLE IF EXISTS brand CASCADE;
CREATE TABLE IF NOT EXISTS brand (
  id INT NOT NULL DEFAULT NEXTVAL ('brand_seq'),
  name VARCHAR(255) NULL,
  PRIMARY KEY (id));

-- -----------------------------------------------------
-- Table products
-- -----------------------------------------------------
DROP TABLE IF EXISTS products CASCADE;

CREATE TABLE IF NOT EXISTS products (
  id VARCHAR(255) NOT NULL,
  brand_id INT NOT NULL,
  name VARCHAR(255) NULL,
  targetaudience VARCHAR(255) NULL,
  category VARCHAR(255) NULL,
  sub_category VARCHAR(255) NULL,
  sub_sub_category VARCHAR(255) NULL,
  msrp VARCHAR(45) NULL,
  discount VARCHAR(45) NULL,
  sellingprice VARCHAR(45) NULL,
  deal VARCHAR(255) NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_products_brand1
    FOREIGN KEY (brand_id)
    REFERENCES brand (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table profiles
-- -----------------------------------------------------
DROP TABLE IF EXISTS profiles CASCADE;

CREATE TABLE IF NOT EXISTS profiles (
  id VARCHAR(255) NOT NULL,
  order_amount INT NULL DEFAULT 0,
  latest TIMESTAMP(0) NULL,
  segment VARCHAR(45) NULL,
  PRIMARY KEY (id));


-- -----------------------------------------------------
-- Table sessions
-- -----------------------------------------------------
DROP TABLE IF EXISTS sessions CASCADE;

CREATE TABLE IF NOT EXISTS sessions (
  browser_id VARCHAR(255) NOT NULL,
  profiles_id VARCHAR(255) NOT NULL,
  segment VARCHAR(45) NULL,
  starttime TIMESTAMP(0) NULL,
  endtime TIMESTAMP(0) NULL,
  devicetype VARCHAR(45) NULL,
  PRIMARY KEY (profiles_id),
  CONSTRAINT fk_sessions_profiles1
    FOREIGN KEY (profiles_id)
    REFERENCES profiles (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table cart
-- -----------------------------------------------------
DROP TABLE IF EXISTS cart CASCADE;

CREATE TABLE IF NOT EXISTS cart (
  products_id VARCHAR(255) NOT NULL,
  sessions_profiles_id VARCHAR(255) NOT NULL,
  bought SMALLINT NOT NULL,
  PRIMARY KEY (products_id, sessions_profiles_id),
  CONSTRAINT fk_products_has_sessions_products
    FOREIGN KEY (products_id)
    REFERENCES products (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_cart_sessions1
    FOREIGN KEY (sessions_profiles_id)
    REFERENCES sessions (profiles_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);