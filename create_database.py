import random

from src.db_helpers import ROBOT_COMPONENT_VALUE_MAX_RANGE, create_connection, database

ROBOT_COUNT = 200
WEAPON_COUNT = 20
HULL_COUNT = 5
ENGINE_COUNT = 6


def random_value():
    return random.choice(range(1, ROBOT_COMPONENT_VALUE_MAX_RANGE))


def select_from_table(conn, select_table_sql):
    c = conn.cursor()
    c.execute(select_table_sql)
    return c.fetchall()


def fill_in_engines_table(conn):
    engines = create_name('Engine', ENGINE_COUNT)
    for name in engines:
        sql = f"INSERT OR IGNORE INTO engines (engine, power, type) " \
              f"VALUES ('{name}', {random_value()}, {random_value()});"
        conn.cursor().execute(sql)


def fill_in_weapons_table(conn):
    weapons = create_name('Weapon', WEAPON_COUNT)
    for name in weapons:
        sql = f"INSERT OR IGNORE INTO weapons (weapon, reload_speed, rotational, diameter, power, count) " \
              f"VALUES ('{name}', {random_value()}, {random_value()}, {random_value()}, " \
              f"{random_value()}, {random_value()});"
        conn.cursor().execute(sql)


def fill_in_hulls_table(conn):
    hulls = create_name('Hull', HULL_COUNT)
    for name in hulls:
        sql = f"INSERT OR IGNORE INTO hulls (hull, armor, type, capacity)" \
              f"VALUES ('{name}', {random_value()}, {random_value()}, {random_value()})"
        conn.cursor().execute(sql)


def fill_in_robots_table(conn):
    robots = create_name('Robot', ROBOT_COUNT)
    weapons = select_from_table(conn, f"SELECT weapon FROM weapons;")
    hulls = select_from_table(conn, f"SELECT hull FROM hulls;")
    engines = select_from_table(conn, f"SELECT engine FROM engines;")
    for name in robots:
        sql = f"INSERT OR IGNORE INTO robots (robot, weapon, hull, engine)" \
              f"VALUES ('{name}', '{random.choice(weapons)[0]}', '{random.choice(hulls)[0]}'," \
              f" '{random.choice(engines)[0]}');"
        conn.cursor().execute(sql)


def create_name(prefix, count):
    return [f'{prefix}-{i}' for i in range(1, count + 1, 1)]


def main():

    sql_create_robots_table = """ CREATE TABLE IF NOT EXISTS robots (
                                        robot text PRIMARY KEY,
                                        weapon text,
                                        hull text,
                                        engine text,
                                        FOREIGN KEY (weapon) REFERENCES weapons(weapon),
                                        FOREIGN KEY (hull) REFERENCES hulls(hull),
                                        FOREIGN KEY (engine) REFERENCES engines(engine)
                                    ); """

    sql_create_weapons_table = """CREATE TABLE IF NOT EXISTS weapons (
                                    weapon text PRIMARY KEY,
                                    reload_speed integer NOT NULL,
                                    rotational speed integer NOT NULL,
                                    diameter integer NOT NULL,
                                    power volley integer NOT NULL,
                                    count integer NOT NULL
                                );"""

    sql_create_hulls_table = """CREATE TABLE IF NOT EXISTS hulls (
                                    hull text PRIMARY KEY,
                                    armor integer NOT NULL,
                                    type integer NOT NULL,
                                    capacity integer NOT NULL
                                );"""

    sql_create_engines_table = """CREATE TABLE IF NOT EXISTS engines (
                                    engine text PRIMARY KEY,
                                    power integer NOT NULL,
                                    type integer NOT NULL    
                                );"""

    conn = create_connection(database)

    if conn is not None:
        conn.cursor().execute(sql_create_robots_table)
        conn.cursor().execute(sql_create_weapons_table)
        conn.cursor().execute(sql_create_hulls_table)
        conn.cursor().execute(sql_create_engines_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        fill_in_engines_table(conn)
        fill_in_hulls_table(conn)
        fill_in_weapons_table(conn)
        fill_in_robots_table(conn)

    conn.close()


if __name__ == '__main__':
    main()
