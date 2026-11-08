from .registry import REGISTRY
from .exceptions import UnknownStepError, InvalidStepParamsError
from pytextprep import word_tokenize
import difflib

def validate(name, kwargs):
    if name not in REGISTRY:
        hint = difflib.get_close_matches(name, REGISTRY, n=1)
        msg = f"'{name}' is not a step."
        if hint:
            msg += f" Did you mean '{hint[0]}'?"
        raise UnknownStepError(msg)

    spec = REGISTRY[name]

    unknown = set(kwargs) - spec["params"]
    if unknown:
        bad = sorted(unknown)[0]
        hint = difflib.get_close_matches(bad, spec["params"], n=1)
        msg = f"Step '{name}' got unknown parameter '{bad}'."
        if hint:
            msg += f" Did you mean '{hint[0]}'?"
        raise InvalidStepParamsError(msg + f" Allowed: {sorted(spec['params'])}")

    missing = spec["required"] - set(kwargs)
    if missing:
        raise InvalidStepParamsError(
            f"Step '{name}' is missing required parameter(s): {sorted(missing)}"
        )

class Pipeline:

    def __init__(self, steps):

        self.steps = []
        for name, params in steps:
            validate(name, params)
            func = REGISTRY[name]["func"]
            self.steps.append((name, dict(params), func))

    def transform(self, text, return_tokens=False):
        for name, params, func in self.steps:
            text = func(text, **params)
            if return_tokens:
                return word_tokenize(text)
            return text

    def transform_batch(self, texts, return_tokens = False):

        result_transofrms = []

        for text in texts:
            result_transofrms.append(self.transform(text, return_tokens = return_tokens))

    def __repr__(self):
        lines = []

        for name, params in self.steps:
            lines.append(f" {name}({params})")

        return "Pipline(\n" + "\n".join(lines) + "\n)"


if __name__ == "__main__":
    pass