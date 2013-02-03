import os

# find the 2nd most popular female name in the US in 1995

path = os.path.join(os.path.dirname(__file__), "yob1995.txt")
names = []
with open(path, "r") as f:
    for line in f:
        (name, gender, num_occurrences_str) = line.split(",")
        if gender == "F":
            num_occurrences = int(num_occurrences_str.strip())
            names.append(((name.strip(), gender.strip(), num_occurrences)))

names.sort(key=lambda x: x[2])
print names[-2][0]