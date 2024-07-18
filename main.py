from collections import defaultdict


class AhoCorasick:

    def __init__(self, words):
        self.max_characters = 26
        self.out = []
        self.fail = []
        self.goto = []

        for i in range(len(words)):
            words[i] = words[i].lower()

        self.words = words
        self.states_count = self.__build_matching_machine()

    def __build_matching_machine(self):
        k = len(self.words)
        states = 1

        for i in range(k):
            word = self.words[i]
            current_state = 0

            while len(self.out) <= states:
                self.out.append(0)
                self.fail.append(-1)
                self.goto.append([-1] * self.max_characters)

            for character in word:
                ch = ord(character) - 97

                if self.goto[current_state][ch] == -1:
                    self.goto[current_state][ch] = states
                    states += 1

                    while len(self.out) <= states:
                        self.out.append(0)
                        self.fail.append(-1)
                        self.goto.append([-1] * self.max_characters)

                current_state = self.goto[current_state][ch]

            self.out[current_state] |= (1 << i)

        for ch in range(self.max_characters):
            if self.goto[0][ch] == -1:
                self.goto[0][ch] = 0

        queue = []

        for ch in range(self.max_characters):
            if self.goto[0][ch] != 0:
                self.fail[self.goto[0][ch]] = 0
                queue.append(self.goto[0][ch])

        while queue:
            state = queue.pop(0)

            for ch in range(self.max_characters):
                if self.goto[state][ch] != -1:
                    failure = self.fail[state]

                    while self.goto[failure][ch] == -1:
                        failure = self.fail[failure]

                    failure = self.goto[failure][ch]
                    self.fail[self.goto[state][ch]] = failure

                    self.out[self.goto[state][ch]] |= self.out[failure]

                    queue.append(self.goto[state][ch])

        return states

    def __find_next_state(self, current_state, next_input):
        if 'a' <= next_input <= 'z':
            ch = ord(next_input) - 97
        else:
            return current_state

        answer = current_state

        while self.goto[answer][ch] == -1:
            answer = self.fail[answer]

        return self.goto[answer][ch]

    def search_words(self, text):
        text = text.lower()

        current_state = 0
        result = defaultdict(list)

        i = 0
        while i < len(text):
            current_state = self.__find_next_state(current_state, text[i])

            if self.out[current_state] != 0:
                for j in range(len(self.words)):
                    if (self.out[current_state] & (1 << j)) > 0:
                        word = self.words[j]
                        start_index = i - len(word) + 1

                        if start_index >= 0:
                            if not result[word] or start_index > result[word][
                                    -1] + len(word) - 1:
                                result[word].append(start_index)

            i += 1

        return result


if __name__ == "__main__":
    words = ["ele", "ela", "feio", "fede"]
    text = "ele disse que o oculos era feio, ela disse que o local fede"

    aho_corasick = AhoCorasick(words)
    result = aho_corasick.search_words(text)

    for word in result:
        for i in result[word]:
            print("Palavra", word, "aparece do caractere", i, "ate",
                  i + len(word) - 1)
