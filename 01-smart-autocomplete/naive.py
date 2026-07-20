def naive_search(word_list,prefix):
    results=[]
    for word in word_list:
        if word.startswith(prefix):
            results.append(word) 
    return results

words=["apple","application","apply","banana","appatizer"]
prefix=input("Enter prefix : ")

matches=naive_search(words,prefix)
print(f"Words starting with '{prefix}' : ")
for word in matches:
    print(f" - {word}")