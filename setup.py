import databaseSetup as db_su
import generateCSV_trash as gen_csv
import fillDatabase as fill_sb

db_su.run()
gen_csv.generateCSV()
fill_sb.fill()