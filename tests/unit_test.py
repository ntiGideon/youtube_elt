def test_api_key(api_key):
    assert api_key == "MOCK_KEY123"


def test_channel_handler(channel_handle):
    assert channel_handle == "MrCheese"


def test_postgres_conn(mock_postgres_conn_vars):
    conn = mock_postgres_conn_vars
    assert conn.login == "mock_username"
    assert conn.password == "mock_password"
    assert conn.host == "mock_host"
    assert conn.port == 1234
    assert conn.schema == "mock_db_name"


def test_dagbag_integrity(dagbag):
    assert dagbag.import_errors == {}, f"Import errors found: {dagbag.import_errors}"
    print("==============")
    print(dagbag.import_errors)

    expected_dag_ids = ["produce_json", "update_db", "data_quality"]
    loaded_dag_ids = list(dagbag.dags.keys())
    print("==============")
    print(dagbag.import_errors)

    for dag_id in expected_dag_ids:
        assert dag_id in loaded_dag_ids, f"DAG {dag_id} is missing."

    assert dagbag.size() == 3
    print("==============")
    print(dagbag.size())

    expected_task_counts = {
        "produce_json": 4,
        "update_db": 2,
        "data_quality": 2
    }
    print("==============")
    for dag_id, dag in dagbag.dags.items():
        expected_count = expected_task_counts[dag_id]
        actual_count = len(dag.tasks)
        assert (
            expected_count == actual_count
        ), f"DAG {dag_id} has {actual_count} tasks, expected {expected_count}."
        print(dag_id, len(dag.tasks))