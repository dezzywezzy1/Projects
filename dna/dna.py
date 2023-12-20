import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Incorrect number of command-line arguments!")
        sys.exit(1)

    # TODO: Read database file into a variable
    people = []
    with open(sys.argv[1], "r") as database_file:
        database_reader = csv.DictReader(database_file)
        fieldnames = database_reader.fieldnames
        for name in database_reader:
            for i in fieldnames:
                if i != "name":
                    name[i] = int(name[i])
            people.append(name)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as sequence_file:
        sequence_reader = sequence_file.read()

    # TODO: Find longest match of each STR in DNA sequence
    DNA_subsequences = fieldnames[1:]
    match = dict()
    for i in DNA_subsequences:
        match.update({i: longest_match(sequence_reader, i)})

    # TODO: Check database for matching profiles
    check_list = []
    for i in range(len(people)):
        for k in DNA_subsequences:
            if people[i][k] == match[k]:
                check_list.append(True)
            else:
                check_list.append(False)
        if False not in check_list:
            return print(people[i]["name"])
        check_list.clear()
    return print("No Match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
