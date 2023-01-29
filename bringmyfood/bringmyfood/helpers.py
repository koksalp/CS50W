def proper_string(wrong: str):
    arr = [each.strip().upper() for each in wrong.strip().split(" ") if each] 
    return " ".join(arr) 

