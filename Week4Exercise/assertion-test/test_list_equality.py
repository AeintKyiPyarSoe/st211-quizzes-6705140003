def test_list_equality():
    assert [1, 2, 3] == [1, 2, 3]
    
def test_list_contents():
    result = [3, 2, 1]
    assert sorted(result) == [1, 2, 3]
    
def test_dict_equality(): 
    expected = {"Name": "Alice", "Age": 30}
    actual = {"Age": 30, "Name": "Alice"}
    assert actual == expected

def test_set_operations():
    assert {1,2,3} & {2,3,4} == {2,3} #intersection
    assert {1,2,3} | {2,3,4} == {1,2,3,4} #union
    assert {1,2,3} - {2,3,4} == {1} #difference