import json


def read_json(path: str) -> list[dict[str, str]]:
    with open(path, "r") as f:
        doc = json.loads(f.read())
    return doc


def extract_instruction_from_json(json_: list[dict[str, str]]) -> list[str]:
    instructions: list[str] = []
    for dict_ in json_:
        try:
            instructions.append(dict_["instruction"])
        except KeyError:
            instructions.append(dict_["Instruction"])
        except Exception:
            raise ValueError
    return instructions


def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)]
