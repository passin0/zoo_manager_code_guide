"""A small zoo feeding program for Python beginners."""


def find_animal(name, animals):
    """Find an animal by name. Return None if it is not in the list."""
    for animal in animals:
        if animal["name"] == name:
            return animal
    return None


def feed_animal(name, animals):
    """Feed an animal and return a message describing what happened."""
    animal = find_animal(name, animals)

    if animal is None:
        return "找不到這隻動物。"

    if animal["hunger"] <= 30:
        return "這隻動物已經吃飽了。"

    animal["hunger"] = animal["hunger"] - 60

    if animal["hunger"] < 0:
        animal["hunger"] = 0

    return "餵食成功。"


def main():
    animals = [
        {"name": "Leo", "species": "Lion", "hunger": 80},
        {"name": "Mia", "species": "Cat", "hunger": 20},
    ]

    message = feed_animal("Leo", animals)
    print(message)

    animal = find_animal("Leo", animals)
    if animal is not None:
        print("{} ({}) hunger: {}".format(
            animal["name"], animal["species"], animal["hunger"]
        ))


if __name__ == "__main__":
    main()
