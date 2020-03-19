import random
from util import Stack, Queue  # These may come in handy

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            # print("WARNING: You cannot be friends with yourself")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            # print("WARNING: Friendship already exists")
            return False
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        # write a for loop that calls create user the right amount of times
        for i in range(num_users):
            self.add_user(f"User {i+1}")

        # Create friendships
        # To create N random friendships
        # you could create a list with all possible friendship combinations
        # shuffle the list, then grab the first N elements from the list
        possible_friendships = []
        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        random.shuffle(possible_friendships)

        # create n friendships where n = avg_friendships * num_users // 2
        # avg_friendships = total_friendships / num_users
        # total_Friendships = avg_friendships * num_users
        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

    def populate_graph_linear(self, num_users, avg_friendships):
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        
        # Add users
        # Write a for loop that calls create user the right amount of times
        for i in range(num_users):
            self.add_user(f"User {i+1}")
            
        target_friendships = num_users * avg_friendships
        total_friendships = 0
        collisions = 0
        while total_friendships < target_friendships:
            # Pick a random user
            user_id = random.randint(1, num_users)
            # Pick another random user
            friend_id = random.randint(1, num_users)
            # Try to create the friendship
            if self.add_friendship(user_id, friend_id):
                # If it works, increment a counter
                total_friendships += 2
            else:
                # If not, try again
                collisions += 1
        print(f"NUM COLLISIONS: {collisions}")

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # create a queue
        q = Queue()
        # enqueue a path to the starting user_id
        q.enqueue([user_id])
        visited = {}  # Note that this is a dictionary, not a set
        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue the first path
            path = q.dequeue()
            # grab the last id form the path
            current_id = path[-1]
            # check if it's been visited
            # If not ...
            if current_id not in visited:
                # add it to visited along with the path
                visited[current_id] = path
                # enqueue the path to each friend to the queue
                for friend_id in self.friendships[current_id]:
                    # copy the path
                    path_copy = path.copy()
                    # append each neighbor
                    path_copy.append(friend_id)
                    # enqueue
                    q.enqueue(path_copy)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    # 10 people, 2 friends on average
    sg.populate_graph(10, 2)
    # 1000 people, 5 friends on average
    sg.populate_graph(1000, 5)

    # see example friendships and social paths for user id 1
    # print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    # print(connections)

    # TEST for average length of path for just one user
    total = 0
    for path in connections.values():
        total += len(path)
    print(f"Average path length for user with id '1': {total / len(connections)}") # 5.1 to 5.3

    # TEST for average length of path by checking all users
    total = 0
    for user_id in sg.users.keys():
        user_total = 0
        connections = sg.get_all_social_paths(user_id)
        for path in connections.values():
            user_total += len(path)
        user_average = user_total / len(connections)
        total += user_average
    final_average = total / len(sg.users)
    print(f"Average path length for ALL users: {final_average}")

    import time
    
    # TEST for linear vs quadratic runtime
    num_users = 2000
    avg_friendships = 10
    sg = SocialGraph()
    start_time = time.time()
    sg.populate_graph(num_users, avg_friendships)
    end_time = time.time()
    print("\n\n-----")
    print(f"Quadratic populate: {end_time - start_time} seconds")
    print("-----\n\n")
    sg = SocialGraph()
    start_time = time.time()
    sg.populate_graph_linear(num_users, avg_friendships)
    end_time = time.time()
    print(f"Linear populate: {end_time - start_time} seconds")


