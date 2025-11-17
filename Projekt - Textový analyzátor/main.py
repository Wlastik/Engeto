# text
TEXTS = [
    '''Situated about 10 miles west of Kemmerer,
    Fossil Butte is a ruggedly impressive
    topographic feature that rises sharply
    some 1000 feet above Twin Creek Valley
    to an elevation of more than 7500 feet
    above sea level. The butte is located just
    north of US 30 and the Union Pacific Railroad,
    which traverse the valley.''',
    '''At the base of Fossil Butte are the bright
    red, purple, yellow and gray beds of the Wasatch
    Formation. Eroded portions of these horizontal
    beds slope gradually upward from the valley floor
    and steepen abruptly. Overlying them and extending
    to the top of the butte are the much steeper
    buff-to-white beds of the Green River Formation,
    which are about 300 feet thick.''',
    '''The monument contains 8198 acres and protects
    a portion of the largest deposit of freshwater fish
    fossils in the world. The richest fossil fish deposits
    are found in multiple limestone layers, which lie some
    100 feet below the top of the butte. The fossils
    represent several varieties of perch, as well as
    other freshwater genera and herring similar to those
    in modern oceans. Other fish such as paddlefish,
    garpike and stingray are also present.'''
]

# Registered users
USERS = {
    "bob": "123",
    "ann": "pass123",
    "mike": "password123",
    "liz": "pass123",
}

SEPARATOR = "-" * 60

# Logged in users
username = input("username:").strip()
password = input("password:").strip()

if USERS.get(username) != password:
    print("\nunregistered user, terminating the program..")
    raise SystemExit()

print(f"\n{SEPARATOR}")
print(f"Welcome to the app, {username}")
print(f"We have {len(TEXTS)} texts to be analyzed.")
print(f"{SEPARATOR}")

# Select text
choice = input(f"Enter a number btw. 1 and {len(TEXTS)} to select: ").strip()
if not choice.isdigit():
    print("Invalid input, terminating the program..")
    raise SystemExit()
idx = int(choice)
if not (1 <= idx <= len(TEXTS)):
    print("Invalid text number, terminating the program..")
    raise SystemExit()

text = TEXTS[idx - 1]

# Clean word
def clean_word(w: str) -> str:
    return w.strip(".,;:!?()[]{}\"'")

words_raw = text.split()
words = [clean_word(w) for w in words_raw if clean_word(w)]

# total counts
total_words = len(words)
titlecase = sum(1 for w in words if w.istitle())
uppercase = sum(1 for w in words if w.isupper() and w.isalpha())
lowercase = sum(1 for w in words if w.islower())
numeric_strs = [w for w in words if w.isdigit()]
numbers_sum = sum(int(n) for n in numeric_strs)

# Print section
print("\n" + "=" * 60)
print(f"There are {total_words} words in the selected text.")
print(f"There are {titlecase} titlecase words.")
print(f"There are {uppercase} uppercase words.")
print(f"There are {lowercase} lowercase words.")
print(f"There are {len(numeric_strs)} numeric strings.")
print(f"The sum of all the numbers {numbers_sum}")
print("=" * 60 + "\n")

# Length counts
length_counts = {}
for w in words:
    l = len(w)
    length_counts[l] = length_counts.get(l, 0) + 1

# Table header
print("LEN| OCCURRENCES |NR")
print("-" * 60)

for length in sorted(length_counts):
    count = length_counts[length]
    stars = "*" * count
    print(f"{length:>3}| {stars:<15} |{count}")

