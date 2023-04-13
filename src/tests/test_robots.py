import pytest

from src.db_helpers import get_main_db_data


@pytest.mark.parametrize('main_db_data', get_main_db_data())
def test_robot_engine(main_db_data, get_memory_data):
    main_data = main_db_data
    memory_db_data = get_memory_data[main_data['robot']['robot']]
    assert compare('robot', main_data, memory_db_data), \
        compare_error_message('robot', main_data, memory_db_data)
    assert compare('engine', main_data, memory_db_data), \
        compare_error_message('engine', main_data, memory_db_data)


@pytest.mark.parametrize('main_db_data', get_main_db_data())
def test_robot_weapon(main_db_data, get_memory_data):
    memory_db_data = get_memory_data[main_db_data['robot']['robot']]
    assert compare('robot', main_db_data, memory_db_data), \
        compare_error_message('robot', main_db_data, memory_db_data)
    assert compare('weapon', main_db_data, memory_db_data), \
        compare_error_message('weapon', main_db_data, memory_db_data)


@pytest.mark.parametrize('main_db_data', get_main_db_data())
def test_robot_hulls(main_db_data, get_memory_data):
    main_data = main_db_data
    memory_db_data = get_memory_data[main_data['robot']['robot']]
    assert compare('robot', main_data, memory_db_data), \
        compare_error_message('robot', main_data, memory_db_data)
    assert compare('hull', main_data, memory_db_data), \
        compare_error_message('hull', main_data, memory_db_data)


def compare(compare_component, main_data, tmp_data):
    items_diff = list(set(main_data[compare_component].items()) ^ set(tmp_data[compare_component].items()))

    if not len(items_diff):
        return True

    return False


def compare_error_message(compare_component, main_data, tmp_data):
    items_diff = list(set(main_data[compare_component].items()) ^ set(tmp_data[compare_component].items()))

    if not len(items_diff):
        return True

    if compare_component == 'robot':
        first_row = f"{tmp_data['robot']['robot']}, {items_diff[1][1]}"
        second_row = f"expected {items_diff[0][1]}, was {items_diff[1][1]}"
    else:
        first_row = f"{tmp_data['robot']['robot']}, {tmp_data['robot'][compare_component]}"
        second_row = f"{items_diff[0][0]}: expected {items_diff[0][1]}, was {items_diff[1][1]}"
    return f'{first_row}\n\t{second_row}'
