#!/usr/bin/env python3
import argparse
import imp
import requests

#maps game name to triples of [url name, html id, cap size]
url_map =   {'mortal_coil': ['coil', 'FlashVars', 18],          \
             'crossflip': ['cross', 'boardinit', 13],           \
             'oneofus': ['oneofus', 'FlashVars', 18],           \
             'runaway_robot': ['runaway', 'FlashVars', 17]      \
            }

#internal game names
name_map =  {'mc': 'mortal_coil',               \
             'mortal_coil': 'mortal_coil',      \
             'cf': 'crossflip',                 \
             'crossflip': 'crossflip',          \
             'oou': 'oneofus',                  \
             'oneofus': 'oneofus',              \
             'rr': 'runaway_robot',             \
             'runaway_robot': 'runaway_robot'   \
            }        


def get_raw_board(username, password, game, level):
    payload = {'name': username, 'password': password}
    if level!=None:
        payload['gotolevel'] = str(level)
        payload['go'] = 'Go+To+Level'
    html_code = str(requests.get('http://www.hacker.org/' + url_map[game][0] + '/', \
        params=payload).content)
    raw_board_start = html_code.find(url_map[game][1]) + url_map[game][2]
    raw_board_end = html_code[raw_board_start:].find('"')
    raw_board = html_code[raw_board_start:raw_board_start + raw_board_end]
    return raw_board


def send_solution(args, sol_payload):
    id_payload = {'name': args.username, 'password': args.password}
    payload = dict(list(id_payload.items()) + list(sol_payload.items()))
    r = requests.post('http://www.hacker.org/' + url_map[args.game][0] + '/', params=payload)
    if r.status_code != 200:
        print("Solution could not be sent!\n")
    elif 'your solution sucked' not in r.text:
        print("Solution was sent and is CORRECT!\n")
    else:
        print("Solution was sent but is NOT CORRECT!\n")


def solve(args, game_mod):
    raw_board = get_raw_board(args.username, args.password, args.game, args.level)
    sol_payload = game_mod.solve(raw_board)
    print("Solution found!")
    send_solution(args, sol_payload)
    if args.follow:
        args.level += 1
        solve(args, game_mod)


def main():
    #argument parsing
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    #user specific data
    parser.add_argument("-u", "--username", default="SpaceMonkey", \
        help="specific username, default is \'SpaceMonkey\'")
    parser.add_argument("-p", "--password", default="schlurps123", \
        help="specific password, default is \'schlurps123\'")

    #game to solve (required)
    parser.add_argument("-g", "--game", default=None, \
        help="specific game to solve; the following games are available: \n\
    - Mortal Coil (\'mc\' or \'mortal_coil\') \n\
    - Runaway Robot (\'rr\' or \'runaway_robot\') \n\
    - Crossflip (\'cf\' or \'crossflip\') \n\
    - OneOfUs (\'oou\' or \'oneofus\')")
    
    #level control
    parser.add_argument("-l", "--level", type=int, \
        help="specific level to solve, default is the highest available level")
    parser.add_argument("-f", "--follow", action="store_true", default=False, \
        help="solve all levels starting from a specific level, turned off by default")

    parser.add_argument("-d", "--debug", action="store_true", default=False, \
        help="show additional debug information")

    args = parser.parse_args()

    if args.game==None:
        print("An available game is required!") 
        return
    elif args.game not in [ 'mc', 'mortal_coil', \
                            'rr', 'runaway_robot', \
                            'cf', 'crossflip', \
                            'oou', 'oneofus']:
        print("You requested an invalid game, see --help for available games.")
        return

    args.game = name_map[args.game]
    game_mod = imp.load_source(args.game, args.game + '/' + args.game + '.py')

    print("Solving " + args.game.upper() + " ...\n")
    solve(args, game_mod)
    
    print("Finished successfully!") 


if __name__ == "__main__":
    main()
