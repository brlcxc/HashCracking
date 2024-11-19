import hashlib
from multiprocessing import Process, current_process
import time
from itertools import product

with open('passwords.txt', 'r') as file:
    raw_hashed_passwords = file.read().splitlines()

    # A dictionary is used to identify which number each password is
    hashed_passwords = {}
    for key_value in raw_hashed_passwords:
        key, value = key_value.split()
        hashed_passwords[int(key)] = value

    # A set is created out of the dictionary values for efficient hash lookup
    hashed_passwords_set = set(hashed_passwords.values())


with open('dictionary.txt', 'r') as file:
    words = file.read().splitlines()

def compute_hash(input_string):
    data = input_string.encode('utf-8')
    sha1_hash = hashlib.sha1(data).hexdigest()
    return sha1_hash

def record_data(password, hashed_value, file, time_found):
        row = next((key for key, value in hashed_passwords.items() if value == hashed_value), None)
        file.write(f"#{row}: {password},{hashed_value} ({time_found})\n")

# The hash cracking is divided up into multiple smaller functions so that they can be run in parallel on multiple cores
# Note: many of these functions can be combined into one but it is better to separate them out to run in parallel

#D
def digit_combinations():
    start_time = time.time()
    with open("rackedHashes/digit_combinations_results.txt", "a") as file:
        for digit_max in range(1, 11):
            for num in range(10 ** digit_max):
                number_string = f"{num:0{digit_max}d}"
                hashed_value = compute_hash(number_string)
                if hashed_value in hashed_passwords_set:
                    response_time = time.time() - start_time
                    record_data(number_string, hashed_value, file, response_time)

#W
def word_combinations():
    start_time = time.time()
    with open("rackedHashes/word_combinations_results.txt", "a") as file:
        for word in words:
            hashed_value = compute_hash(word)
            if hashed_value in hashed_passwords_set:
                response_time = time.time() - start_time
                record_data(word, hashed_value, file, response_time)

#WD
def trailing_digit_combinations():
    start_time = time.time()
    with open("rackedHashes/trailing_digit_combinations_results.txt", "a") as file:
        for digit_max in range(1, 11):
            for num in range(10 ** digit_max):
                number_string = f"{num:0{digit_max}d}"
                for word in words:
                    password_attempt = word + number_string
                    hashed_value = compute_hash(password_attempt)
                    if (hashed_value in hashed_passwords_set):
                        response_time = time.time() - start_time
                        record_data(password_attempt, hashed_value, file, response_time)

#DW
def leading_digit_combinations():
    start_time = time.time()
    with open("rackedHashes/leading_digit_combinations_results.txt", "a") as file:
        for digit_max in range(1, 11):
            for num in range(10 ** digit_max):
                number_string = f"{num:0{digit_max}d}"
                for word in words:
                    password_attempt = number_string + word
                    hashed_value = compute_hash(password_attempt)
                    print(password_attempt)
                    if hashed_value in hashed_passwords_set:
                        response_time = time.time() - start_time
                        record_data(password_attempt, hashed_value, file, response_time)


#WW
def two_word_combinations():
    start_time = time.time()
    with open("rackedHashes/two_word_combinations_results.txt", "a") as file:
        for combination in product(words, repeat=2):
            combination_string = ''.join(combination)
            hashed_value = compute_hash(combination_string)
            if hashed_value in hashed_passwords_set:
                response_time = time.time() - start_time
                record_data(combination_string, hashed_value, file, response_time)

#WWD
def two_word_trailing_digit_combinations():
    start_time = time.time()
    with open("rackedHashes/two_word_trailing_digit_results.txt", "a") as file:
        for digit_max in range(1, 11):
            for num in range(10 ** digit_max):
                number_string = f"{num:0{digit_max}d}"
                for combination in product(words, repeat=2):
                    combination_string = ''.join(combination)
                    password_attempt = combination_string + number_string
                    hashed_value = compute_hash(password_attempt)
                    if hashed_value in hashed_passwords_set:
                        response_time = time.time() - start_time
                        record_data(password_attempt, hashed_value, file, response_time)

#DWW
def two_word_leading_digit_combinations():
    start_time = time.time()
    with open("rackedHashes/two_word_leading_digit_results.txt", "a") as file:
        for digit_max in range(1, 11):
            for num in range(10 ** digit_max):
                number_string = f"{num:0{digit_max}d}"
                for combination in product(words, repeat=2):
                    combination_string = ''.join(combination)
                    password_attempt = number_string + combination_string
                    hashed_value = compute_hash(password_attempt)
                    print(password_attempt)
                    if hashed_value in hashed_passwords_set:
                        response_time = time.time() - start_time
                        record_data(password_attempt, hashed_value, file, response_time)

#WWW
def three_word_combinations():
    start_time = time.time()
    with open("rackedHashes/three_word_combinations_results.txt", "a") as file:
        for combination in product(words, repeat=3):
            combination_string = ''.join(combination)
            hashed_value = compute_hash(combination_string)
            if hashed_value in hashed_passwords_set:
                response_time = time.time() - start_time
                record_data(combination_string, hashed_value, file, response_time)

#WWW chunked
def process_combinations(words_chunk):
    start_time = time.time()
    with open(f"crackedHashes/results_{current_process().name}.txt", "a") as file:
        for word1 in words_chunk:
            for word2 in words:
                for word3 in words:
                    combination_string = word1 + word2 + word3
                    hashed_value = compute_hash(combination_string)
                    if hashed_value in hashed_passwords_set:
                        response_time = time.time() - start_time
                        record_data(combination_string, hashed_value, file, response_time)

# Function that chunks up the WWW function
# Note: This is needed due to the long search time
def chunked_combinations():
    # Split words into 4 roughly equal chunks
    chunk_size = len(words) // 4
    chunks = [
        words[0:chunk_size],
        words[chunk_size:2 * chunk_size],
        words[2 * chunk_size:3 * chunk_size],
        words[3 * chunk_size:]
    ]

    processes = []
    for i in range(4):
        process = Process(target=process_combinations, args=(chunks[i],))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

# Function that contains all of the main processes
def process_hash_breaking():
    functions = [
        digit_combinations,
        word_combinations,
        trailing_digit_combinations,
        leading_digit_combinations,
        two_word_combinations,
        two_word_trailing_digit_combinations,
        two_word_leading_digit_combinations,
        three_word_combinations,
    ]

    # Create and start all processes
    processes = [Process(target=func) for func in functions]
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

if __name__ == '__main__':
    chunked_combinations()
    # process_hash_breaking()