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
        return result_transofrms

    def __repr__(self):
        lines = []

        for name, params, _ in self.steps:
            lines.append(f" {name}({params})")

        return "Pipline(\n" + "\n".join(lines) + "\n)"


if __name__ == "__main__":

    nlp_pipeline = Pipeline([
        ("remove_urls", {}),
        ("expand_contractions", {}),
        ("remove_stopwords", {"custom_words": ["check"]}),
        ("remove_punctuation", {"keep_emojis": False}),
        ("lower_case", {}),
    ])

    raw_text = "I don't like spam emails! Visit https://test.com right NOW."
    processed_text = nlp_pipeline.transform(raw_text)

    print("Raw:      ", raw_text)
    print("Processed:", processed_text)
    # Processed: not like spam email visit right

    arabic = Pipeline([("normalize_arabic", {}), ("remove_punctuation", {})])
    print(arabic.transform("أَهْلاً بِكُم في الـــمـعهد!!") == "اهلا بكم في المعهد")

    pipe = Pipeline([]).transform("  Hi  ")
    print(pipe)
    pipe2 = Pipeline([("lower_case", {})]).transform_batch(["a", "", "b"])
    print(pipe2)
    pipe3 = Pipeline([("remove_url", {})]) 
    print(pipe3)