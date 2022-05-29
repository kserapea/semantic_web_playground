from src.python.semantic_web_playground.simplegraph import SimpleGraph


def run() -> None:
    g = SimpleGraph()
    g.add(("blade_runner", "name", "Blade Runner"))
    g.add(("blade_runner", "name", "Blade Runner"))
    g.add(("blade_runner", "release_date", "June 25, 1982"))
    g.add(("blade_runner", "directed_by", "Ridley Scott"))

    print(list(g.triples((None, None, None))))
    print(list(g.triples(("blade_runner", None, None))))
    print(list(g.triples(("blade_runner", "name", None))))
    print(list(g.triples(("blade_runner", "name", "Blade Runner"))))
    print(list(g.triples(("blade_runner", None, "Blade Runner"))))
    print(list(g.triples((None, "name", "Blade Runner"))))
    print(list(g.triples((None, None, "Blade Runner"))))

    print(list(g.triples(("foo", "name", "Blade Runner"))))
    print(list(g.triples(("blade_runner", "foo", "Blade Runner"))))
    print(list(g.triples(("blade_runner", "name", "foo"))))


if __name__ == "__main__":
    print("Starting")
    run()
