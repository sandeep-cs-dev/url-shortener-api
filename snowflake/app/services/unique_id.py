from app.snowflake.snowflake import SnowFlake
def generate_uniq_id():
    snowflake = SnowFlake(0, 0, None)
    return snowflake.generate_id()
