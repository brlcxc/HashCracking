import hashlib
from multiprocessing import Process, current_process
import time
from itertools import product

with open('passwords.txt', 'r') as file:
    raw_hashed_passwords = file.read().splitlines()
    hashed_passwords = {}
    for key_value in raw_hashed_passwords:
        key, value = key_value.split()
        hashed_passwords[int(key)] = value

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

#D
def digit_combinations():
    start_time = time.time()
    with open("digit_combinations_results.txt", "a") as file:
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
    with open("word_combinations_results.txt", "a") as file:
        for word in words:
            hashed_value = compute_hash(word)
            if hashed_value in hashed_passwords_set:
                response_time = time.time() - start_time
                record_data(word, hashed_value, file, response_time)

#WD
def trailing_digit_combinations():
    start_time = time.time()
    with open("trailing_digit_combinations_results.txt", "a") as file:
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
    with open("leading_digit_combinations_results.txt", "a") as file:
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
    with open("two_word_combinations_results.txt", "a") as file:
        for combination in product(words, repeat=2):
            combination_string = ''.join(combination)
            hashed_value = compute_hash(combination_string)
            if hashed_value in hashed_passwords_set:
                response_time = time.time() - start_time
                record_data(combination_string, hashed_value, file, response_time)

#WWD
def two_word_trailing_digit_combinations():
    start_time = time.time()
    with open("two_word_trailing_digit_results.txt", "a") as file:
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
    with open("two_word_leading_digit_results.txt", "a") as file:
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
    with open("three_word_combinations_results.txt", "a") as file:
        for combination in product(words, repeat=3):
            combination_string = ''.join(combination)
            hashed_value = compute_hash(combination_string)
            if hashed_value in hashed_passwords_set:
                response_time = time.time() - start_time
                record_data(combination_string, hashed_value, file, response_time)

#WWW chunked
def process_combinations(words_chunk):
    start_time = time.time()
    with open(f"results_{current_process().name}.txt", "a") as file:
        for word1 in words_chunk:
            for word2 in words:
                for word3 in words:
                    combination_string = word1 + word2 + word3
                    hashed_value = compute_hash(combination_string)
                    if hashed_value in hashed_passwords_set:
                        response_time = time.time() - start_time
                        record_data(combination_string, hashed_value, file, response_time)

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

def processHashBreaking():
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
    processHashBreaking()
    # leading_digit_combinations()
    # p1 = multiprocessing.Process(target=digit_combinations)
    # p2 = multiprocessing.Process(target=word_combinations)
    # p3 = multiprocessing.Process(target=trailing_digit_combinations)
    # p4 = multiprocessing.Process(target=leading_digit_combinations)
    # p5 = multiprocessing.Process(target=two_word_combinations)
    # p6 = multiprocessing.Process(target=two_word_trailing_digit_combinations)
    # p7 = multiprocessing.Process(target=two_word_leading_digit_combinations)
    # p8 = multiprocessing.Process(target=three_word_combinations)

    # p1.start()
    # p2.start()
    # p3.start()
    # p4.start()
    # p5.start()
    # p6.start()
    # p7.start()
    # p8.start()

    # p1.join()
    # p2.join()
    # p3.join()
    # p4.join()
    # p5.join()
    # p6.join()
    # p7.join()
    # p8.join()


# yes, WD and DW can be both combined by checking the reverse
# W can also be checked by checking the initial with no digit

#might be more efficient to reverse the loops - more likely to have less num
#DW






# print(hashed_passwords)
# trailing_digit_combinations()
# digit_max = 0
# test = 123
# number_string = f"{test:0{digit_max}d}"
# print (number_string)
# 10 digits for each
# print(hashed_passwords_set)
# number_string = "123456"
# test = compute_hash(number_string)
# print(number_string)
# print(test)
# if (test in hashed_passwords_set):
#     print(number_string)
#     print(test)
# D
# maybe just work can be inlcuded within number but have a 0 for no string?
# W
# DW
# WD
# WW
# DWW
# WWD
# WWW

# have an if in thing for every hash result

# I can multithread each of my different functions I guess

# I am thinking check each word for each digit to speed it all up
# going to 10 is too expensive otherwise

# maybe have each write to their own file and then compile them at the end
# I can also consider breaking up the number searches into seperate functions to further break it down

# dictionary for hashed passwords

# dont have the one write to a file but rather have an outside thing to do it 