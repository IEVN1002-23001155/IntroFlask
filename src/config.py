class DevelopmentConfig():
    DEBUG=True
    MYSQL_HOST='localhost'
    MYSQL_USER='lang'
    MYSQL_PASSWORD='Contrest123'
    MYSQL_DB='api_utl'
    MYSQL_CURSORCLASS= 'Cursor'
    

config={
    'development':DevelopmentConfig
}