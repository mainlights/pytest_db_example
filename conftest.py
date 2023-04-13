import sqlite3
import pytest

from src.db_helpers import \
    create_connection, \
    get_table_columns_and_values, \
    randomize_parameter_value, \
    get_robots_with_relations, database, ROBOT_COMPONENT_VALUE_MAX_RANGE


def pytest_sessionstart():
    pytest.conn = create_connection(database)
    pytest.conn.row_factory = sqlite3.Row

    pytest.temp_conn = create_connection(':memory:')
    pytest.conn.backup(pytest.temp_conn)
    pytest.temp_conn.row_factory = sqlite3.Row

    pytest.memory_db_robots = {}


def pytest_sessionfinish():
    pytest.conn.close()
    pytest.temp_conn.close()


@pytest.fixture(scope='session', autouse=True)
def shuffle_memory_db():
    (robot_column_names, robots) = get_table_columns_and_values('robots')
    (weapon_column_names, weapons) = get_table_columns_and_values('weapons')
    (hull_column_names, hulls) = get_table_columns_and_values('hulls')
    (engine_column_names, engines) = get_table_columns_and_values('engines')

    robot_components = {
        'weapon': [n[0] for n in weapons],
        'hull': [n[0] for n in hulls],
        'engine': [n[0] for n in engines],
    }

    component_parameters_value_list = list(range(1, ROBOT_COMPONENT_VALUE_MAX_RANGE + 1, 1))

    randomize_parameter_value(robots, 'robots', robot_column_names, robot_components, True)
    randomize_parameter_value(weapons, 'weapons', weapon_column_names, component_parameters_value_list)
    randomize_parameter_value(hulls, 'hulls', hull_column_names, component_parameters_value_list)
    randomize_parameter_value(engines, 'engines', engine_column_names, component_parameters_value_list)

    pytest.temp_conn.commit()


@pytest.fixture(scope='session')
def get_memory_data(shuffle_memory_db):
    (robots_dict, weapons_dict, hulls_dict, engines_dict) = get_robots_with_relations(pytest.temp_conn)
    print("!!!!!!!!1call memory data!!!!!!!!")
    memory_db_robots = {
        robot['robot']: {
            'robot': robot,
            'weapon': weapons_dict[robot['weapon']],
            'hull': hulls_dict[robot['hull']],
            'engine': engines_dict[robot['engine']]
        } for robot in robots_dict.values()
    }
    return memory_db_robots
