NUMBERS = {
    "ноль": 0, "один": 1, "два": 2, "три": 3, "четыре": 4,
    "пять": 5, "шесть": 6, "семь": 7, "восемь": 8, "девять": 9,
    "десять": 10, "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13,
    "четырнадцать": 14, "пятнадцать": 15, "шестнадцать": 16, "семнадцать": 17,
    "восемнадцать": 18, "девятнадцать": 19, "двадцать": 20,
    "тридцать": 30, "сорок": 40, "пятьдесят": 50, "шестьдесят": 60,
    "семьдесят": 70, "восемьдесят": 80, "девяносто": 90
}

REVERSE_NUMBERS = {v: k for k, v in NUMBERS.items()}

def parse_number(text):
    parts = text.split()
    result = 0
    for part in parts:
        result += NUMBERS[part]
    return result

def to_text(num):
    if num == 0:
        return "ноль"
    result = []
    if num >= 20:
        result.append(REVERSE_NUMBERS[num // 10 * 10])
        num %= 10
    if num > 0:
        result.append(REVERSE_NUMBERS[num])
    return " ".join(result)

def tokenize(expression):
    tokens = []
    parts = expression.split()
    buffer = []
    for part in parts:
        if part in ("плюс", "минус", "умножить", "(", ")"):
            if buffer:
                tokens.append(" ".join(buffer))
                buffer = []
            tokens.append(part)
        elif part == "на":
            continue
        else:
            buffer.append(part)
    if buffer:
        tokens.append(" ".join(buffer))
    return tokens

def to_postfix(tokens):
    precedence = {"плюс": 1, "минус": 1, "умножить": 2}
    output = []
    operators = []
    for token in tokens:
        if token in precedence:
            while (operators and operators[-1] != "(" and
                   precedence[token] <= precedence[operators[-1]]):
                output.append(operators.pop())
            operators.append(token)
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            operators.pop()
        else:
            output.append(token)
    while operators:
        output.append(operators.pop())
    return output

def evaluate_postfix(tokens):
    stack = []
    for token in tokens:
        if token in ("плюс", "минус", "умножить"):
            b = stack.pop()
            a = stack.pop()
            if token == "плюс":
                stack.append(a + b)
            elif token == "минус":
                stack.append(a - b)
            elif token == "умножить":
                stack.append(a * b)
        else:
            stack.append(parse_number(token))
    return stack[0]

def calc(expression):
    expression = expression.replace("скобка открывается", "(").replace("скобка закрывается", ")")
    tokens = tokenize(expression)
    postfix = to_postfix(tokens)
    result = evaluate_postfix(postfix)
    return to_text(result)

print(calc("пять плюс два умножить на три минус один"))  # "десять"
print(calc("скобка открывается пять плюс два скобка закрывается умножить на три минус один"))  # "двадцать"
