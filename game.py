#!/usr/bin/env python
"""
Main program for the Avalam game.
Author: Cyrille Dejemeppe <cyrille.dejemeppe@uclouvain.be>
Copyright (C) 2014, Université catholique de Louvain
Modified by the teaching team of the course INF8215 - 2022, Polytechnique Montréal

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
import signal

import logging
import time
import socket
import xmlrpc.client
import pickle
import subprocess
import threading

# from MCTS.MonteCarlo import MonteCarlo
# from MCTS.simulate_functions import one_action_heuristic, random_play

from avalam import *
from genetic_player import GeneticAgent
from secret_agent import SecretAgent


from stats.stats import generate_board_history_fig, generate_summary_file

# Agent classes for multithreading
from greedy_player import GreedyAgent
from random_player import RandomAgent
from alpha_beta_genetic_agent import AlphaBetaGeneticAgent
from monte_carlo_player import MonteCarloAgent
from step_analyst_player import StepAnalystPlayer

from alpha_beta_genetic_agent_IDS import AlphaBetaIDSGeneticAgent
from best_move_genetic_agent import BestMoveGeneticAgent

from strategies.simulate_functions import best_score, one_action_heuristic, one_action_heuristic_iso, random_play


class TimeCreditExpired(Exception):
    """An agent has expired its time credit."""

def register_history_available_actions(history):
    f = open(f"stats/available_actions.csv", "a")
    for i in range(50):
        if i < len(history):
            f.write(f"{history[i]},")
        else:
            f.write(f"0,")
    f.write(f"0\n")
    f.close()

class Viewer(EvolvedAgent):

    """Interface for an Avalam viewer and human agent."""

    def init_viewer(self, board, game=None):
        """Initialize the viewer.

        Arguments:
        board -- initial board

        """
        pass

    def playing(self, step, player):
        """Player player is currently playing step step."""
        pass

    def update(self, step, action, player):
        """Update the viewer after an action has been played.

        Arguments:
        step -- current step number
        action -- action played
        player -- player that has played

        """
        pass

    def replay(self, trace, speed=1.0):
        """Replay a game given its saved trace."""
        step = 0
        self.init_viewer(trace.get_initial_board(), [])
        for player, action, t in trace.actions:
            step += 1
            self.playing(step, player)
            if speed < 0:
                time.sleep(-t / speed)
            else:
                time.sleep(speed)
            self.update(step, action, player)
        self.finished(step, trace.winner, trace.reason)


class ConsoleViewer(Viewer):

    """Simple console viewer."""

    def init_viewer(self, board, game=None):
        self.board = board
        self.game = game
        print(self.board)

    def playing(self, step, player):
        print("Step", step, "- Player", 1 if player == 1 else 2, "is playing")

    def update(self, step, action, player):
        print("Step", step, "- Player", 1 if player == 1 else 2, "has played", action,"Score", self.board.get_score())
        self.board.play_action(action)
        print(self.board)

    def play(self, percepts, player, step, time_left):
        while True:
            try:
                p = 1 if player == 1 else 2
                line = input("Player %d plays (i1, j1, i2, j2): " %
                             p)
            except EOFError:
                exit(1)
            try:
                i1, j1, i2, j2 = [x.strip() for x in line.split(",")]
                print("action " + str((int(i1),
                                       int(j1), int(i2), int(j2))))
                return (int(i1), int(j1), int(i2), int(j2))
            except (ValueError, AssertionError):
                pass

    def finished(self, steps, winner, reason=""):
        if winner == 0:
            print("Draw game")
        else:
            print("Player 1" if winner > 0 else "Player 2", "has won!")
        if reason:
            print("Reason:", reason)


class Trace:

    """Keep track of a played game.

    Attributes:
    time_limits -- a sequence of 2 elements containing the time limits in
        seconds for each agent, or None for a time-unlimitted agent
    initial_board -- the initial board
    actions -- list of tuples (player, action, time) of the played action.
        Respectively, the player number, the action and the time taken in
        seconds.
    winner -- winner of the game
    reason -- specific reason for victory or "" if standard

    """

    def __init__(self, board, time_limits):
        """Initialize the trace.

        Arguments:
        board -- the initial board
        time_limits -- a sequence of 2 elements containing the time limits in
            seconds for each agent, or None for a time-unlimitted agent

        """
        self.time_limits = [t for t in time_limits]
        self.initial_board = board
        self.actions = []
        self.winner = 0
        self.reason = ""

    def add_action(self, player, action, t):
        """Add an action to the trace.

        Arguments:
        player -- the player
        action -- the played action, a tuple as specified by
            avalam.Board.play_action
        t -- a float representing the number of seconds the player has taken
            to generate the action

        """
        self.actions.append((player, action, t))

    def set_winner(self, winner, reason):
        """Set the winner.

        Arguments:
        winner -- the winner
        reason -- the specific reason of victory

        """
        self.winner = winner
        self.reason = reason

    def get_initial_board(self):
        """Return a Board instance representing the initial board."""
        return self.initial_board.clone()

    def write(self, f):
        """Write the trace to a file."""
        pickle.dump(self, f)


def load_trace(f):
    """Load a trace from a file."""
    return pickle.load(f)


class Game:

    """Main Avalam game class."""

    def __init__(self, agents, board, viewer=None, credits=[None, None], game_id=None, pool_id=None):
        """New Avalam game.

        Arguments:
        agents -- a sequence of 2 elements containing the agents (instances
            of Agent)
        board -- the board on which to play
        viewer -- the viewer or None if none should be used
        credits -- a sequence of 2 elements containing the time credit in
            seconds for each agent, or None for a time-unlimitted agent

        """
        self.agents = agents
        self.board = board.clone()
        self.viewer = viewer if viewer is not None else Viewer()
        self.credits = credits
        self.step = 0
        self.player = 1
        self.trace = Trace(board, credits)
        self.game_id = game_id
        self.pool_id = pool_id
        self.available_actions = []

    def startPlaying(self):
        self.viewer.init_viewer(self.board.clone(), game=self)
        logging.info("Starting to play")
        self.play()

    def play(self):
        """Play the game."""
        logging.info("Starting new game")
        try:
            while not self.board.is_finished():
                self.step += 1
                self.available_actions.append(sum(1 for _ in self.board.get_actions()))
                logging.debug("Asking player %d to play step %d",
                              self.player, self.step)
                self.viewer.playing(self.step, self.player)
                board_dict = {
                    'm': self.board.m,
                    'rows': self.board.rows,
                    'max_height': self.board.max_height,
                }
                action, t = self.timed_exec("play",
                                            board_dict,
                                            self.player,
                                            self.step)
                
                self.board.play_action(action)
                self.viewer.update(self.step, action, self.player)
                self.trace.add_action(self.player, action, t)
                self.player = -self.player
        except (TimeCreditExpired, InvalidAction) as e:
            if isinstance(e, TimeCreditExpired):
                logging.debug("Time credit expired")
                reason = "Opponent's time credit has expired."
            else:
                logging.debug("Invalid action: %s", e.action)
                reason = "Opponent has played an invalid action."
            if self.player == 1:
                winner = -1
            else:
                winner = 1
            self.step += 1
        else:
            reason = ""
            winner = self.board.get_score()
            logging.info("Score: %d", winner)
        if winner > 0:
            logging.info("Winner: Player 1")
        elif winner < 0:
            logging.info("Winner: Player 2")
        else:
            logging.info("Winner: draw game")
        self.trace.set_winner(winner, reason)
        self.viewer.finished(self.step, winner, reason)
        # print(f"Game finished in {self.step} steps")
        # print(f"Credits: {self.credits}")
        for i in range(2):
            if self.agents[i].hasEvolved():
                self.agents[i].finished(self.step, winner, reason, 1 if i==0 else -1, self.game_id, self.pool_id)
        register_history_available_actions(self.available_actions)
           
    def timed_exec(self, fn, *args, agent=None):
        """Execute self.agents[agent].fn(*args, time_left) with the
        time limit for the current player.

        Return a tuple (result, t) with the function result and the time taken
        in seconds. If agent is None, the agent will be computed from
        self.player.

        """
        if agent is None:
            agent = 0 if self.player > 0 else 1
        if self.credits[agent] is not None:
            logging.debug("Time left for agent %d: %f",
                          agent,
                          self.credits[agent])
            if self.credits[agent] < 0:
                raise TimeCreditExpired
            socket.setdefaulttimeout(self.credits[agent] + 1)
        start = time.time()
        try:
            if self.agents[agent].hasEvolved():
                result = self.agents[agent].play(*args + (self.credits[agent],) + (self.game_id,) + (self.pool_id,))
            else:
                result = self.agents[agent].play(*args + (self.credits[agent],))
        except socket.timeout:
            self.credits[agent] = -1.0  # ensure it is counted as expired
            raise TimeCreditExpired
        except (socket.error, xmlrpc.client.Fault) as e:
            logging.error("Player %d was unable to play step %d." +
                          " Reason: %s", agent + 1, self.step, e)
            raise InvalidAction
        except Exception as e:
            logging.error("Player %d was unable to play step %d." +
                          " Reason: %s", agent + 1, self.step, e)
            raise InvalidAction
        end = time.time()
        t = end - start
        logging.info("Step %d: received result %s in %fs",
                     self.step, result, t)
        if self.credits[agent] is not None:
            self.credits[agent] -= t
            logging.debug("New time credit for agent %d: %f",
                          agent,
                          self.credits[agent])
            if self.credits[agent] < -0.5:  # small epsilon to be sure
                raise TimeCreditExpired
        return (result, t)


def connect_agent(uri):
    """Connect to a remote player and return a proxy for the Player object."""
    return xmlrpc.client.ServerProxy(uri, allow_none=True)

class GameThread(threading.Thread):
    def __init__(self, agents, viewer=None, credits=[None, None], game_id=None, pool_id=None, nb_games_to_finish=None):
        self.board = Board()
        self.agents = agents
        self.viewer = viewer if viewer is not None else Viewer()
        self.step = 0
        self.player = 1
        self.game_id=game_id
        self.pool_id=pool_id
        self.nb_games_to_finish = nb_games_to_finish
        self.available_actions = []
        self.action_history = []
        self.credits = credits
        self.winner = None
        threading.Thread.__init__(self)

    def run(self):
        self.play()

    def play(self):
        winner = None
        try:
            while not self.board.is_finished():
                self.step += 1
                self.available_actions.append(sum(1 for _ in self.board.get_actions()))
                agent = 0 if self.player > 0 else 1
                board_dict = {
                    'm': self.board.m,
                    'rows': self.board.rows,
                    'max_height': self.board.max_height,
                }
                start = time.time()
                if self.agents[agent].hasEvolved():
                    action = self.agents[agent].play(board_dict, self.player, self.step, self.credits[agent], self.game_id, self.pool_id)
                else:
                    action = self.agents[agent].play(board_dict, self.player, self.step, self.credits[agent])
                end = time.time()
                t = end - start
                if self.credits[agent] != None:
                    self.credits[agent] -= t
                    if self.credits[agent] < -0.5:
                        winner = -self.player
                        break
                self.board.play_action(action)
                self.action_history.append(action)
                self.player = -self.player
        except e:
            winner = -self.player
            pass
        reason = ""
        if winner == None:
            winner = self.board.get_score()
            
        for i in range(2):
            if self.agents[i].hasEvolved():
                agents[i].finished(self.step, winner, reason, 1 if i==0 else -1, self.game_id, self.pool_id)
        register_history_available_actions(self.available_actions)
        self.nb_games_to_finish['nb'] -= 1
        self.winner = winner
        print(f"Game progression: {int(100*(self.nb_games_to_finish['nb_games']-self.nb_games_to_finish['nb'])/self.nb_games_to_finish['nb_games'])}%\t\tPool progression: {progress_bar(self.pool_id, self.nb_games_to_finish['nb_pool'])}   ", end='\r')
           
    def get_scores(self):
        return self.winner

    def get_steps(self):
        return self.step

    def get_history(self):
        return self.action_history

    def get_id(self):
        return self.game_id

if __name__ == "__main__":
    import argparse

    def posfloatarg(string):
        value = float(string)
        if value <= 0:
            raise argparse.ArgumentTypeError("%s is not strictly positive" %
                                             string)
        return value

    parser = argparse.ArgumentParser(
        usage="%(prog)s [options] AGENT1 AGENT2\n" +
              "       %(prog)s [options] -r FILE")
    parser.add_argument("agent1", nargs='?', default=None,
                        help="path to the first agent (Player 1) or" +
                             " keyword 'human' (default: human)",
                        metavar="AGENT1")
    parser.add_argument("agent2", nargs='?', default=None,
                        help="path to the second agent (Player 2) or" +
                             " keyword 'human' (default: human)",
                        metavar="AGENT2")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="be verbose")
    parser.add_argument("-M", "--multithreading", action="store_true", default=False,
                        help="Run using multithreading")
    parser.add_argument("-P", "--pool", type=int, default=1,
                        help="generate N pool competitions (default: 1)",
                        metavar="N")
    parser.add_argument("-S", "--stats", action="store_true", default=False,
                        help="store stats about winners")
    parser.add_argument("-f", "--gif", action="store_true", default=False,
                        help="generate gifs of the games")
    parser.add_argument("-G", "--games", type=int, default=1,
                        help="repeat the game N times in each pool (default: 1)",
                        metavar="N")
    parser.add_argument("--no-gui",
                        action="store_false", dest="gui", default=True,
                        help="do not try to load the graphical user interface")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--headless", action="store_true", default=False,
                   help="run without user interface (players cannot be" +
                   " human)")
    g.add_argument("-r", "--replay", type=argparse.FileType('rb'),
                   help="replay the trace written in FILE",
                   metavar="FILE")
    parser.add_argument("-w", "--write", type=argparse.FileType('wb'),
                        help="write the trace to FILE for replay with -r" +
                             " (no effect on replay)",
                        metavar="FILE")
    g = parser.add_argument_group("Rule options (no effect on replay)")
    g.add_argument("-t", "--time", type=posfloatarg,
                   help="set the time credit per player (default: untimed" +
                        " game)",
                   metavar="SECONDS")
    g = parser.add_argument_group("Replay options")
    g.add_argument("-s", "--speed", type=posfloatarg,
                   help="set the duration of each step in seconds or scale" +
                        " if realtime (default: %(default)s)",
                   metavar="SECONDS", default=2.0)
    g.add_argument("--realtime", action="store_true", default=False,
                   help="replay with the real durations")
    args = parser.parse_args()

    if args.realtime:
        args.speed = -args.speed

    level = logging.WARNING
    if args.verbose:
        level = logging.DEBUG
    logging.basicConfig(format="%(asctime)s -- %(levelname)s: %(message)s",
                        level=level)

    # Create initial board
    if args.replay is not None:
        # replay mode
        logging.info("Loading trace '%s'", args.replay.name)
        try:
            trace = load_trace(args.replay)
            args.replay.close()
        except (IOError, pickle.UnpicklingError) as e:
            logging.error("Unable to load trace. Reason: %s", e)
            exit(1)
        board = trace.get_initial_board()
    else:
        # default board
        board = Board()

    # Create viewer
    if args.headless:
        args.gui = False
        viewer = None
    else:
        if args.gui:
            try:
                import gui
                subprocess.Popen(["python3",
                                    "SimpleHTTPServer.py"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
                viewer = gui.WebViewer()
                signal.signal(signal.SIGINT, viewer.close_sig_handler)
                signal.signal(signal.SIGTERM, viewer.close_sig_handler)
                logging.info("Using the web viewer." +
                             " Please open a web browser at" +
                             " http://localhost:8000/.")
            except Exception as e:
                logging.warning("Unable to load GUI, falling back to" +
                                " console. Reason: %s", e)
                args.gui = False
        if not args.gui:
            viewer = ConsoleViewer()

    if args.replay is None:
        # Normal play mode
        credits = [None, None]
        agents = []
        agents = [args.agent1, args.agent2]
        for i in range(2):
            if agents[i] == 'human':
                agents[i] = viewer
            elif agents[i] != None:
                agents[i] = connect_agent(agents[i])
                credits[i] = args.time
            else:
                agents[i] = RandomAgent()

        genetic_agent1 = AlphaBetaIDSGeneticAgent()
        genetic_agent2 = AlphaBetaIDSGeneticAgent()
        paramsTrain = { 'mode': "train", 'save': "test", 'generation':141 }
        paramsEvaluate1 = {
            "mode": "evaluate",
            "save": "test",
            "generation": 179, }
        paramsEvaluate2 = {
            "mode": "evaluate",
            "save": "test",
            "generation": 140, }
        paramsEvaluatefullObsInit = { 'mode': "evaluate", 'save': "fullObsInit", 'generation': 40 }
        paramsTrainHeuristic = { 'mode': "train", 'save': "IDSimproved", 'generation': 1 }
        paramsEvaluateMCTSHeuristic = { 'mode': "evaluate", 'save': "mctsSimulation", 'generation': 99 }
        paramsEvaluateMCTSisoHeuristic = { 'mode': "evaluate", 'save': "mctsSimulationIso", 'generation': 34 }
        paramsEvaluateGetScoreHeuristic = { 'mode': "evaluate", 'save': "bestScore", 'generation': 1 }
        paramsEvaluateIDS = { 'mode': "evaluate", 'save': "IDSimproved", 'generation': 1 }
        paramsTrainLinks = { 'mode': "train", 'save': "links", 'generation': 251 }
        # paramsEvaluateLinks = { 'mode': 'evaluate', 'save': 'links', 'generation': 117 }
        paramsEvaluateLinks = { 'mode': 'evaluate', 'save': 'links', 'generation': 117 }

        genetic_agent1.setup(None, None, paramsTrainLinks)
        # genetic_agent1.setup(None, None, paramsEvaluateIDS)
        genetic_agent2.setup(None, None, paramsEvaluatefullObsInit)
        # agents = [genetic_agent2, RandomAgent()]
        # //MonteCarloAgent(play_fn=one_action_heuristic)
        # agents = [genetic_agent2, MonteCarloAgent(play_fn=best_score)]
        # agents = [RandomAgent(), GreedyAgent()]
        # agents = [StepAnalystPlayer(MonteCarloAgent()), StepAnalystPlayer(MonteCarloAgent())]        
        agents = [RandomAgent(), genetic_agent1]
        # agents = [genetic_agent1, genetic_agent2]
        
        def get_agent_names():
            if agents[0].hasEvolved():
                agent_p1 = agents[0].get_agent_id()
            else:
                agent_p1 = "Agent +1"
            if agents[1].hasEvolved():
                agent_m1 = agents[1].get_agent_id()
            else:
                agent_m1 = "Agent -1"
            
            return [agent_p1, agent_m1]

        def compute_pool_results(history):
            winners=[-1 if score<0 else 1 if score>0 else 0 for score in history]
            if len(winners) == 0:
                return [0, 0, 0]
            return [winners.count(-1)/len(winners),winners.count(0)/len(winners),winners.count(1)/len(winners)]

        def play(game):
            try:
                game.startPlaying()
            except KeyboardInterrupt:
                exit()
            
            if args.write is not None:
                logging.info("Writing trace to '%s'", args.write.name)
                try:
                    game.trace.write(args.write)
                    args.write.close()
                except IOError as e:
                    logging.error("Unable to write trace. Reason: %s", e)
            if args.gui:
                logging.debug("Replaying trace.")
                viewer.replay(game.trace, args.speed, show_end=True)
            game_history['scores'].append(game.trace.winner)
            game_history['steps'].append(game.step)
            if args.gif:
                actions_history = [a[1] for a in game.trace.actions]
                time_to_play_history = [a[2] for a in game.trace.actions]
                generate_board_history_fig(ImprovedBoard(compute_isolated_towers=True), actions_history, time_to_play_history, get_agent_names(), "stats/", p, game.game_id)

        def progress_bar(i, n):
            return"[%-20s] %d%%" % ('='*int(20*i/n), 100*i/n)

        pool_history = []
        if args.stats:
            f = open(f"stats/game_results.csv", "w")
            f.write(f"Pool id;Agent -1;Agent 1;Scores;Steps\n")
            f.close()

            f = open(f"stats/pool_results.csv", "w")
            f.write(f"Pool id;Agent -1;Agent 1;Pct Agent -1;Pct Draw;Pct Agent 1\n")
            f.close()
        for p in range(args.pool):
            game_history = dict()
            game_history['scores'] = []
            game_history['steps'] = []
            
            if args.multithreading:
                nb_games_to_finish = { 'nb': args.games, 'nb_games': args.games, 'nb_pool': args.pool }
                threads = []
                for i in range(args.games):
                    credits = [args.time, args.time]
                    t = GameThread(agents, viewer, credits, i, p, nb_games_to_finish)
                    threads.append(t)
                    t.start()
                for t in threads:
                    t.join()
                for t in threads:
                    game_history['scores'].append(t.get_scores())
                    game_history['steps'].append(t.get_steps())
                    if args.gif:
                        if agents[0].hasEvolved():
                            agent_p1 = agents[0].get_agent_id()
                        else:
                            agent_p1 = "Agent +1"
                        if agents[1].hasEvolved():
                            agent_m1 = agents[1].get_agent_id()
                        else:
                            agent_m1 = "Agent -1"
                        generate_board_history_fig(ImprovedBoard(compute_isolated_towers=True), t.get_history(), get_agent_names(), "stats/", p, t.get_id())

            else:
                for i in range(args.games):
                    board = Board()
                    credits = [args.time, args.time]
                    game = Game(agents, board, viewer, credits, i, p)

                    if args.gui:
                        threading.Thread(target=play, args=[game]).start()
                    else:
                        play(game)
                    print(f"Game progression: {int(100*(i+1)/args.games)}%\t\tPool progression: {progress_bar(p+1, args.pool)}   ", end='\r')
            if not args.gui:
                pool_results = compute_pool_results(game_history['scores'])
                pool_history.append(pool_results)
                if args.stats:
                    [agent_p1, agent_m1] = get_agent_names()
                    f = open("stats/game_results.csv", "a")
                    f.write(f"{p};{agent_m1};{agent_p1};{game_history['scores']};{game_history['steps']}\n")
                    f.close()
                    f = open("stats/pool_results.csv", "a")
                    f.write(f"{p};{agent_m1};{agent_p1};{';'.join([str(r) for r in pool_results])}\n")
                    f.close()
                print(f"Game progression: --%_\t\tPool progression: {progress_bar(p+1, args.pool)}", end='\r')


            if not args.gui:
                for i in range(2):
                    if agents[i].hasEvolved():
                        agents[i].pool_ended(pool_results, 1 if i==0 else -1, p)
        if not args.gui and args.stats:
            generate_summary_file('stats/')
    else:
        # Replay mode
        viewer.replay(trace, args.speed)
