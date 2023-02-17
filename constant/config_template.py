#db_login_info

login =''
password = ''
db_url = ''
schema = ''
path_to_ssl =''


#db_login_info
db_login= {
    'root':'mysql+pymysql://root:root@localhost:3307/db',
    'azure':f'mysql+pymysql://{login}'
            f':{password}'
            f'@{db_url}/{schema}'
            f'?ssl_ca={path_to_ssl}'
}