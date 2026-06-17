import sys

# Helper Functions
def removeAll(lst, x):
    return [y for y in lst if y != x]

# Tokenizer
def tokenize(code):
    code = list(code); output = []; delimeters = ["+", "-", "/", "*", "@", " ", ";", "(", ")", "{", "}", '"', "\n", ".", ","]; processing = ""
    for c in code:
        found_delimeter = ""
        for delimeter in delimeters:
            if delimeter == c: found_delimeter = delimeter
        if found_delimeter != "":
            output.append(processing); output.append(found_delimeter); processing = ""
        else:
            processing = processing + c
    output = removeAll(output, ""); output = removeAll(output, " "); output = removeAll(output, "\n")
    return output

# Handling 'Fancy' VS Code Junk Stuff
def readFile(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("File Not Found")

# Parser (AKA #ILoveBadCode >:)
class Parser:
    def __init__(self, tokens):
        self.pointer = 0
        self.tokens = tokens
    
    def current(self):
        return self.tokens[self.pointer]
    
    def eat(self, expd=None):
        token = self.current()
        if expd != None and token != expd:
            print(f"Was expecting {expd}, but got {token}")
        self.pointer += 1
        return token
    
    def parse_set_var(self):
        self.eat("set")
        type = self.eat()
        name = self.eat()
        self.eat("=")
        value = self.eat()
        self.eat(";")
        vars[name] = {"type": type, "value": value}

    def parse_print(self):
            self.eat("print")
            self.eat("(")
            is_var = self.eat()
            if is_var == '"':
                to_print = self.eat()
                self.eat('"')
                self.eat(")")
                self.eat(";")
                print(to_print)
            else:
                is_special = self.eat()
                if is_special == ".":
                    print(vars[is_var][str(self.eat())])
                    self.eat(")")
                    self.eat(";")
                elif is_special == ")":
                    print(vars[is_var]["value"])
                    self.eat(";")
    
    def parse_create_function(self):
        self.eat("function")
        self.eat()
        name = self.eat()
        self.eat("(")
        args = []
        while True:
            to_add = self.eat()
            if to_add == ")":
                break
            elif to_add == ",":
                pass
            else:
                args.append(str(to_add))
        self.eat("{")
        body = []
        while True:
            to_add = self.eat()
            if to_add == "}":
                break
            body.append(to_add)
        functions[name] = {"body":body, "args":args}
        self.eat(";")

    def parse_run_function(self):
        self.eat("run")
        function = functions[self.eat()]
        tokens = function["body"]
        self.eat("(")
        a = 0
        string = False
        while a < len(function["args"]):
            arg = str(self.eat())
            if arg == ",":
                pass
            elif arg != '"':
                try:
                    int(arg)
                except ValueError:
                    arg = vars[arg]["value"] if string != True else arg
                type = function["args"][a]
                name = function["args"][a+1]
                add_var = ["set", type, name, "=", arg, ";"]
                tokens = add_var + tokens
                a += 2
            else:
                string = True
        if string == True:
            self.eat('"')
        self.eat(")")
        self.eat(";")
        Interpreter(tokens, Parser(tokens))
        a = 1
        while a < len(function["args"]):
            if function["args"][a] in vars:
                del vars[function["args"][a]]
            a += 2
    
    def parse_change_var(self):
        self.eat("change")
        var = self.eat()
        operation = self.eat()
        value = self.eat()
        try:
            value = int(value)
        except ValueError:
            value = int(vars[value]["value"])
        self.eat(";")
        var_value = vars[var]["value"]
        if operation == "+":
            vars[var]["value"] = int(var_value) + value
        elif operation == "-":
            vars[var]["value"] = int(var_value) - value
        elif operation == "/":
            vars[var]["value"] = int(var_value) / value
        elif operation == "*":
            vars[var]["value"] = int(var_value) * value
            
    def parse_return(self):
        self.eat("return")
        name = self.eat()
        self.eat("as")
        type = self.eat()
        value = self.eat()
        if value == '"':
            value = self.eat()
            self.eat('"')
            self.eat(";")
        elif value == ";":
            value = vars[type]["value"]
            type = vars[type]["type"]
        else:
            self.eat(";")
        vars[name] = {"type": type, "value": value}

# "Interpreter"... Not really... Same with the "Parser"... Not like normal but works ;)
class Interpreter:
    def __init__(self, tokens, parser):
        while parser.pointer < len(tokens):
            current = parser.current()
            if current == "set":
                parser.parse_set_var()
            elif current == "print":
                parser.parse_print()
            elif current == "function":
                parser.parse_create_function()
            elif current == "run":
                parser.parse_run_function()   
            elif current == "change" :
                parser.parse_change_var()
            elif current == "return":
                parser.parse_return()

# Main

vars = {
}

functions = {
}

file_path = sys.argv[1]
code = readFile(file_path)

tokens = tokenize(code)

parser = Parser(tokens)
Interpreter(tokens, parser)
