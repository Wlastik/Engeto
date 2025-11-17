import random
import time
from typing import List, Tuple

DIGITS: int = 4  # length of the secret number; **do not** hardcode anywhere else


def pluralize(n: int, singular: str, plural: str) -> str:
    # pluralization helper for output
    return f"{n} {singular if n == 1 else plural}"


def generate_secret(length: int) -> str:    # generates the number, first digit cannot be 0
    digits = list("0123456789")
    first = random.choice(digits[1:])
    digits.remove(first)
    secret_rest = random.sample(digits, length - 1)
    return first + "".join(secret_rest)


def validate_guess(guess: str, length: int) -> List[str]:  # input validation
    errors: List[str] = []

    if len(guess) != length:
        errors.append(f"Your tip must have {length} digits.")

    if not guess.isdigit():
        errors.append("Your tip can contain only 0–9.")

    if guess and guess[0] == "0":
        errors.append("Your tip cannot start with 0")

    if len(set(guess)) != len(guess):
        errors.append("Your tip cannot have duplicate numbers.")

    return errors


def count_bulls_cows(secret: str, guess: str) -> Tuple[int, int]:  # counts correct digits in correct & wrong positions
    bulls = sum(s == g for s, g in zip(secret, guess))
    common = sum(min(secret.count(d), guess.count(d)) for d in set(guess))
    cows = common - bulls
    return bulls, cows


def print_intro() -> None:
    print("Hi there!")
    print("-----------------------------------------------")
    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print("-----------------------------------------------")


def play_one_round() -> int:
    secret = generate_secret(DIGITS)
    attempts = 0
    start = time.monotonic()

    while True:
        print("-----------------------------------------------")
        guess = input("Enter a number: ").strip()
        errors = validate_guess(guess, DIGITS)

        if errors:
            print("\nWrong tip:")
            for e in errors:
                print(f"- {e}")
            continue

        attempts += 1
        bulls, cows = count_bulls_cows(secret, guess)

        if bulls == DIGITS:
            duration = time.monotonic() - start
            print("-----------------------------------------------")
            print("Correct, you've guessed the right number")
            print(f"in {attempts} { 'guess' if attempts == 1 else 'guesses' }!")
            print("-----------------------------------------------")
            print("Nice!")
            print(f"(Time: {duration:.1f} s)")
            return attempts

        print(f"{pluralize(bulls, 'bull', 'bulls')}, {pluralize(cows, 'cow', 'cows')}")


def ask_yes_no(prompt: str) -> bool:  # yes/no question for repeating the game
    ans = input(f"{prompt} [y/n]: ").strip().lower()
    return ans in {"y", "yes", "a", "ano"}


def print_stats(games: List[int]) -> None:  # game statistics
    if not games:
        return
    total = len(games)
    best = min(games)
    worst = max(games)
    avg = sum(games) / total
    print("\n=== Statistics ===")
    print(f"Games played: {total}")
    print(f"Best game:   {best} { 'guess' if best == 1 else 'guesses' }")
    print(f"Worst game:  {worst} { 'guess' if worst == 1 else 'guesses' }")
    print(f"Average:     {avg:.2f} guesses")
    print("==================\n")


def main() -> None:  # runs the program, repeats rounds, shows statistics
    print_intro()
    results: List[int] = []

    while True:
        results.append(play_one_round())
        print_stats(results)
        if not ask_yes_no("Play again"):
            print("Thanks for playing. Bye!")
            break


if __name__ == "__main__":    # prevents auto-start when imported as a module
    main()
