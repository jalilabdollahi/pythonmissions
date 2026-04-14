import pytest, sys
sys.path.insert(0, ".")
from broken import DockerClient
from unittest.mock import MagicMock

def test_list_containers_url():
    sess = MagicMock()
    resp = MagicMock()
    resp.json.return_value = []
    sess.get.return_value = resp
    client = DockerClient(sess)
    client.list_containers()
    url = sess.get.call_args[0][0]
    assert "/containers/json" in url

def test_short_id():
    client = DockerClient(MagicMock())
    full_id = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"
    assert len(client.short_id(full_id)) == 12
