import random
import sqlite3
import pytest

database = "./robots.db"
ROBOT_COMPONENT_VALUE_MAX_RANGE = 20


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def get_table_columns_and_values(table_name):
    cursor = pytest.temp_conn.cursor()
    items = cursor.execute(f'SELECT * FROM {table_name}').fetchall()
    column_names = items[0].keys()
    return column_names, items


def randomize_parameter_value(items, table_name, columns, column_values, parameter_value_by_randomize=False):
    pk_column_name = columns[0]
    del columns[0]

    for item in items:
        randomize_column = random.choice(columns)

        if not parameter_value_by_randomize:
            randomize_column_value = random.choice(column_values)
        else:
            randomize_column_value = random.choice(column_values[randomize_column])

        pytest.temp_conn.execute(
            f'UPDATE {table_name} SET {randomize_column}="{randomize_column_value}" WHERE {pk_column_name}="{item[0]}"'
        )


def get_main_db_data():
    (robots_dict, weapons_dict, hulls_dict, engines_dict) = get_robots_with_relations(pytest.conn)

    robots_with_relations = ({
        'robot': robot,
        'weapon': weapons_dict[robot['weapon']],
        'hull': hulls_dict[robot['hull']],
        'engine': engines_dict[robot['engine']]
    } for robot in robots_dict.values())

    return robots_with_relations


def get_robots_with_relations(conn):
    robots = conn.execute(f"SELECT * FROM robots order by robot asc;").fetchall()
    weapons = conn.execute(f"SELECT * FROM weapons order by weapon asc;").fetchall()
    hulls = conn.execute(f"SELECT * FROM hulls order by hull asc;").fetchall()
    engines = conn.execute(f"SELECT * FROM engines order by engine asc;").fetchall()

    robots_dict = {robot['robot']: dict(robot) for robot in robots}
    weapons_dict = {weapon['weapon']: dict(weapon) for weapon in weapons}
    hulls_dict = {hull['hull']: dict(hull) for hull in hulls}
    engines_dict = {engine['engine']: dict(engine) for engine in engines}

    return robots_dict, weapons_dict, hulls_dict, engines_dict


