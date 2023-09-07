import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    # 如果 sys.argv 中的参数数量大于 2，说明提供了太多的参数，程序会使用 sys.exit() 来退出，并打印一条错误消息："Usage: python degrees.py [directory]"。
    # 这是一种用于表示使用错误或参数错误的方式。
    # 否则，如果参数数量等于 2，它会将第二个参数（sys.argv[1]）赋值给变量 directory，表示指定了一个目录作为参数。
    # 如果参数数量等于 1（即没有提供参数），它会将默认目录名称 "large" 赋值给变量 directory。

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))  # source、target是Id
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO

    frontier = QueueFrontier()
    frontier.add(Node(source, None, None))
    # state:person_id, parent:node, action:(movie_id, person_id)

    explored = set()
    while not frontier.empty():
        node = frontier.remove()
        explored.add(node.state)
        neighbors = neighbors_for_person(node.state)
        for neighbor in neighbors:
            _, person_id = neighbor

            if person_id == target:
                path = [neighbor]
                while node.parent is not None:
                    path.append(node.action)
                    node = node.parent
                path.reverse()
                return path

            if person_id not in explored and not frontier.contains_state(person_id):
                frontier.add(Node(person_id, node, neighbor))

    return None


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    # names.get(name.lower(), set()) 是一个字典操作，它尝试从 names 字典中获取与给定名称的小写版本相关联的值（即人员 ID 集合）。
    # 如果字典中没有这个名称，它会返回一个空集合（set()）作为默认值。
    # 总之，这行代码的作用是根据给定的名称（不区分大小写）从 names 字典中获取与之相关的人员 ID，并将这些人员 ID 存储在一个列表中。
    # 如果该名称没有与之相关的人员 ID，那么列表将为空。这种操作通常用于数据查找或检索，以根据给定的名称查找相关的数据。
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
#第一次做这种题，非常不熟练，借鉴了一位大佬的：[github:PKUFlyingPig](https://github.com/PKUFlyingPig/cs50_ai/blob/master/lab/degrees/degrees.py)
