def convert_to_number(string):
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            return string  # or handle the case where the string cannot be converted
        
if __name__ == "__main__":
    print(convert_to_number("10"))
    print(convert_to_number("10.9"))
    print(convert_to_number("abc"))