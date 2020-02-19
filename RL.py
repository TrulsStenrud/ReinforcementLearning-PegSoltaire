from Actor import Actor
from Boards.Triangle import TriangleBoard
from Critic import Critic
import matplotlib.pyplot as plt


class RL:

    @staticmethod
    def do_actor_critic(actor, critic, init_state, n_episodes):
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

                critic.update_from_td_error(current_episode, td_error)
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

            if ep % 10 == 0:
                print(ep)
        #  for state in current_episode:

        RL.plot(remaining_pegs)
        return winning_game

    @staticmethod
    def plot(remaining_pegs):
        plt.plot(remaining_pegs)
        plt.ylabel('Remaining pegs')
        plt.show()
