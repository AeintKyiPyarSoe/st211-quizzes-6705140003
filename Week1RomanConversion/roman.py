def roman_to_integer(roman):
    # 1. Base numeral mapping: define the decimal value for each Roman symbol
    values = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }

    roman = roman.upper()

    # Reject empty inputs immediately
    if not roman:
        raise ValueError("Roman numeral cannot be empty.")


    # 2. Character validity: ensure every character is a recognized Roman numeral
    for char in roman:
        if char not in values:
            raise ValueError("Invalid Roman numeral character.")

    # 3. Repetition rules:
    # - V, L, and D represent 5-based values and can never be repeated
    if "VV" in roman or "LL" in roman or "DD" in roman:
        raise ValueError("V, L, and D cannot be repeated.")


    # - I, X, C, and M cannot repeat more than 3 consecutive times (e.g., IIII is invalid)
    if "IIII" in roman or "XXXX" in roman or "CCCC" in roman or "MMMM" in roman:
        raise ValueError("A Roman numeral cannot repeat more than 3 times.")

    # 4. Subtraction rules:
    # Standard Roman notation only permits these 6 specific subtractive pairs
    valid_subtractions = {
        "IV", "IX",
        "XL", "XC",
        "CD", "CM"
    }

    # Look ahead by 1 character: if a smaller numeral precedes a larger one,
    # verify it is one of the 6 allowed pairs (e.g., reject 'VX' or 'IL')
    for i in range(len(roman) - 1):
        current = roman[i]
        next_char = roman[i + 1]

        if values[current] < values[next_char]:
            pair = current + next_char

            if pair not in valid_subtractions:
                raise ValueError(
                    f"Invalid subtraction: {pair}"
                )


    total = 0

    # 5. Value calculation:
    # If the current symbol is less than the next, subtract it; otherwise, add it
    # e.g., XIV = x (10) is added, I (1) is followed by V(5), so I is subtracted: 10 + (5 - 1) = 14
    for i in range(len(roman)):
        # If the current numeral is less than the next, subtract it; otherwise, add it
        if (
            i + 1 < len(roman)
            and values[roman[i]] < values[roman[i + 1]]
        ):
            total -= values[roman[i]]
        else:
            total += values[roman[i]]

    if total < 1 or total > 3999:
        raise ValueError("Roman numeral must represent a number from 1 to 3999.")

    # Re-encode the total back to Roman to catch non-standard orders (e.g., 'IIV', 'CMCC')
    if integer_to_roman(total) != roman:
        raise ValueError("Invalid Roman numeral format.")

    return total


def integer_to_roman(number):
    # Greedy mapping sorted from highest to lowest, including subtractive combinations
    values = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I")
    ]

    result = ""

    # Greedily subtract the highest possible value until number hits 0
    for value, symbol in values:
        while number >= value:
            result += symbol
            number -= value

    return result


if __name__ == "__main__":
    # Interactive CLI loop for testing and live user interaction
    while True:
        roman = input("Enter a Roman numeral: ")

        try:
            result = roman_to_integer(roman)
            print("Integer:", result)

        except ValueError as error:
            print("Invalid input:", error)
            continue

        while True:
            again = input("Do you want to continue? (yes/no): ").lower()

            if again == "yes" or again == "y":
                break

            elif again == "no" or again == "n":
                print("Goodbye!")
                exit()

            else:
                print("Please enter yes or no.")