from Actor import Actor
from Boards.Triangle import TriangleBoard
from Critic import Critic
import matplotlib.pyplot as plt


class Engine:

    @staticmethod
    def reinforcement_learning():
        n_episodes = 500
        gamma = 0.9  # discount rate γ
        learning_rate_a = 0.8  # α
        learning_rate_c = 0.8  # α
        trace_decay = 0.8
        epsilon = 0.5
        epsilon_decay = 0.95

        actor = Actor(learning_rate_a, trace_decay, gamma, epsilon, epsilon_decay)

        layers = (15, 20, 1)
        critic = Critic(gamma, learning_rate_c, trace_decay)
        # critic = NCritic(gamma, learning_rate_c, trace_decay, layers)

        free_cells = list()
        free_cells.append((2, 1))

        init_state = TriangleBoard(5, free_cells)
        # init_state = SortOfDiamondBoard()

        # init_state = DummyBoard()

        return Engine.do_reinforcement_learning(actor, critic, init_state, n_episodes)

    @staticmethod
    def do_reinforcement_learning(actor, critic, init_state, n_episodes):
        remaining_pegs = list()

        winning_game = ()

        for ep in range(0, n_episodes):
            new_state = init_state
            old_state = new_state
            current_episode = list()

            while not old_state.is_terminate_state():
                action = actor.get_action(old_state)
                current_episode.append((old_state, action))

                (new_state, r) = old_state.do_action(action)

                td_error = critic.calculate_td_error(r, new_state, old_state)

                critic.update_stuff(current_episode, td_error)
                actor.update_td_error(current_episode, td_error)

                old_state = new_state

            # print(old_state.reward())
            actor.new_episode()
            critic.new_episode()
            peg_count = old_state.peg_count()
            remaining_pegs.append(peg_count)

            if peg_count == 1:
                current_episode.append((new_state, None))
                winning_game = tuple(current_episode)
        #  for state in current_episode:

        Engine.plot(remaining_pegs)
        return winning_game

    @staticmethod
    def plot(remaining_pegs):
        plt.plot(remaining_pegs)
        plt.ylabel('Remaining pegs')
        plt.show()
