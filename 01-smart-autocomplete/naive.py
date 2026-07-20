def naive_search(word_list, prefix):
    results = []
    for word in word_list:
        if word.startswith(prefix):
            results.append(word)
    return results