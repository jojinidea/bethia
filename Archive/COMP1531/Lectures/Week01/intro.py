word = input("Enter a string ")
new_word = ""

for i in range(len(word) -1, 0, -1):
    new_word += i
    print(new_word)
    
// Lists in python do not have to be in the same data type
// e.g. my_list = [2, 3, "apples", "oranges"]
// my_list.append("mandarin")
// print(my_list) - prints my_list with mandarins at the end
// item = my_list.pop()
// print(item) 
// lists behaves like a stack in python
