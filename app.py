from typing import Union
from data import options, valid_actions
from calculator import Calculator
import sys
from string import ascii_lowercase

def set_up() -> Calculator:
    try:
        calculator = Calculator()
        return calculator
    except TypeError:
        raise TypeError('Wrong calculator instance')

def dispatch(calculator: Calculator, action: str, payload: dict) -> Union[int | float, str]:
    match action:
        case "Exit":
            return "Exit"
        case "Add":
            return calculator.add(payload['x'], payload['y'])
        case "Subtract":
            return calculator.subtract(payload['x'], payload['y'])
        case "Multiply":
            return calculator.multiply(payload['x'], payload['y'])
        case "Divide":
            return  calculator.divide(payload['x'], payload['y'])
        case _:
            return "Wrong action!"

def process_input(calculator, request_body: dict):
    # get the result
    result = dispatch(calculator, request_body["action"], {"x": request_body["x"], "y": request_body["y"]})
    print(f"Successful operation! The result of {request_body['x']} {request_body['action']} {request_body['y']} is {result}")

def read_input() -> dict | list:
    """This function reads the input from user"""

    # initialize to empty
    request_body: str = ""
    queue = []

    if not sys.stdin.isatty():
        request_body = sys.stdin.read().strip()
        if not request_body:
            return {"error": "Docker did not send any data, sorry!"}

        chunks = request_body.split()
        iterator = iter(chunks)
        try:
            while True:
                x = next(iterator)
                if x == "Exit":
                    queue.append(x)
                    break

                y = next(iterator)
                action = next(iterator)
                queue.append((x, y, action))
        except StopIteration:
            pass

        # return the queue and process data
        return queue
    else:
        request_body: str = str(input())

        # handle exit immediately
        if request_body == "Exit":
            print("You confirm the exit! Exiting....")
            exit()

    try:
        x, y, action = request_body.split()
        if action not in valid_actions:
            return {"error": "Invalid action"}

        return {"x": float(x), "y": float(y), "action": action }
    except ValueError:
        raise ValueError("Wrong data provided to the application!")


def print_options():
    print(options if options is not None else "")

def app():
    # set up
    calculator = set_up()

    while True:
        # print the options
        print_options()

        # read and scan the user request
        request_body = read_input()

        if isinstance(request_body, dict):
            # check if the key exists (default value is empty)
            if request_body.get("error", "") != "":
                if "Docker" in request_body["error"]:
                    break
                elif "Invalid" in request_body["error"]:
                    continue
            else:
                # proceed as normal
                process_input(calculator, request_body)
        else:
            # we can get a list instead
            if isinstance(request_body, list):
                for data in request_body:
                    # if tuple
                    # then we process it
                    # if string, then we perform exit
                    if isinstance(data, tuple):
                        process_input(calculator, {"x": float(data[0]), "y": float(data[1]), "action": data[2]})
                    elif data == "Exit":
                        exit()

