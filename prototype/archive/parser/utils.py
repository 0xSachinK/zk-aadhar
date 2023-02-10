def find_sub_array_return_first_index(_in, sub_array):
    # _in is a list
    # sub_array is a list
    # returns the index of the first element of the sub_array in _in
    # returns None if not found
    #
    # Example:
    # _in = [1,2,3,4,5,6,7,8,9,10]
    # sub_array = [4,5,6]
    # returns 3
    #
    for i in range(len(_in)):
        if _in[i] == sub_array[0]:
            # Found the first element of sub_array
            # Check if the rest of the elements match
            found = True
            for j in range(1, len(sub_array)):
                if _in[i+j] != sub_array[j]:
                    found = False
                    break
            if found:
                return i


def find_sub_array_return_last_index(_in, sub_array):
    # _in is a list
    # sub_array is a list
    # returns the index of the last element of the sub_array in _in
    # returns None if not found
    #
    # Example:
    # _in = [1,2,3,4,5,6,7,8,9,10]
    # sub_array = [4,5,6]
    # returns 5
    #
    for i in range(len(_in)):
        if _in[i] == sub_array[0]:
            # Found the first element of sub_array
            # Check if the rest of the elements match
            found = True
            for j in range(1, len(sub_array)):
                if _in[i+j] != sub_array[j]:
                    found = False
                    break
            if found:
                return i + len(sub_array) - 1


def find_sub_array_return_values_in_between(_in, sub_array_1, sub_array_2):
    # _in is a list
    # sub_array_1 is a list
    # sub_array_2 is a list
    # returns the values in between sub_array_1 and sub_array_2
    # returns None if not found
    #
    # Example:
    # _in = [1,2,3,4,5,6,7,8,9,10]
    # sub_array_1 = [4,5,6]
    # sub_array_2 = [8,9,10]
    # returns [7]
    #
    index_1 = find_sub_array_return_last_index(_in, sub_array_1)
    index_2 = find_sub_array_return_first_index(_in, sub_array_2)
    if index_1 is None or index_2 is None:
        return None
    else:
        return _in[index_1+1:index_2]
