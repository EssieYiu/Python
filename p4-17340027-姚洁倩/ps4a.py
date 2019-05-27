# Problem Set 4A
# Name: 17340027 姚洁倩
# Collaborators:None
# Time Spent:

def get_permutations(sequence):
    permutation_of_current_string = []
    if len(sequence) == 0:
        return permutation_of_current_string
    if len(sequence) == 1:
        permutation_of_current_string.append(sequence)
        return permutation_of_current_string
    else:
        permutation_of_substring = []
        substring = sequence[1:len(sequence)]
        first_char = sequence[0]
        permutation_of_substring = get_permutations(substring)
        for string in permutation_of_substring:
            for i in range(len(string)+1):
                new_string = list(string)
                new_string.insert(i,first_char)
                new_string = "".join(new_string)
                if new_string not in permutation_of_current_string:
                    permutation_of_current_string.append(new_string)
        return permutation_of_current_string

if __name__ == '__main__':

    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    print('')
    
    example_input1 = ''
    print('Input:',example_input1)
    print('Expected Output:',[])
    print('Actual Output:',get_permutations(example_input1))
    print('')

    example_input2 = 'aaa'
    print('Input:',example_input2)
    print('Expected Output:',['aaa'])
    print('Actual Output:',get_permutations(example_input2))
    print('')

    example_input3 = 'bbc'
    print('Input:',example_input3)
    print('Expected Output:',['bbc','bcb','cbb'])
    print('Actual Output:',get_permutations(example_input3))
    print('')

